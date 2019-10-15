from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

# from craigslist import CraigslistHousing
from craigslist import CraigslistHousing

from .GetRentalHouse import getRentalHouse
from .forms import ZillowSearchForm
from .models import CraigslistLocation, LastRetrievedData
import json
import datetime


class CraigslistIndexView(generic.ListView):
    template_name = "search/clist_results.html"
    context_object_name = "cl_results"


def search(request):
    if request.method == "POST" and "zillow" in request.POST:
        form = ZillowSearchForm(request.POST)
        if form.is_valid():
            address = request.POST["address"]
            cityStateZip = request.POST["cityStateZip"]
            rentZestimate = "true"

            jsonData = json.loads(getRentalHouse(address, cityStateZip, rentZestimate))
            results = jsonData["SearchResults:searchresults"]["response"]["results"][
                "result"
            ]
            return render(request, "search/result.html", {"z_results": results})
    else:
        ## render an error
        form = ZillowSearchForm()
        return render(request, "search/search.html", {"form": form})


# TODO: Display data beautifully
def result(request):
    return HttpResponse("Result Page")


def error(request):
    return HttpResponse("This is index of Error")


def clist_results(request):
    doUpdate = False
    if LastRetrievedData.objects.filter(model="CraigslistLocation").exists():
        last = LastRetrievedData.objects.get(model="CraigslistLocation")
        timediff = timezone.make_aware(datetime.datetime.now()) - last.time
        if timediff.days > 2:
            doUpdate = True
            last.time = timezone.now()
            last.save()
    results = []
    if doUpdate is True:
        cl_h = CraigslistHousing(
            site="newyork", category="apa", filters={"max_price": 2000}
        )
        results = cl_h.get_results()

    for r in results:
        if not CraigslistLocation.objects.filter(c_id=r["id"]).exists():
            q = CraigslistLocation(
                c_id=r["id"],
                name=r["name"],
                url=r["url"],
                date_time=r["datetime"],
                price=r["price"],
                where=(r["where"] if r["where"] is not None else ""),
                has_image=r["has_image"],
            )
            q.save()
    result_list = CraigslistLocation.objects.all()
    context = {"clist_results": result_list}
    return render(request, "search/clist_results.html", context)
