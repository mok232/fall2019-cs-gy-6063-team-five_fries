from django import forms
from localflavor.us import forms as us_forms
from django.core.validators import MinValueValidator
from .models import Location, Apartment


class ApartmentUploadForm(forms.Form):
    city = forms.CharField(label="City", max_length=100)
    state = us_forms.USStateField(label="State")
    address = forms.CharField(label="Address", max_length=255)
    zipcode = us_forms.USZipCodeField(label="Zip Code")
    rent_price = forms.DecimalField(
        label="Rent Price ($)", max_digits=20, decimal_places=2
    )
    number_of_bed = forms.IntegerField(
        label="Bedrooms", validators=[MinValueValidator(0)]
    )

    # Handling input files with Django
    # https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html
    image = forms.ImageField()
    suite_num = forms.CharField(label="Suite Number", max_length=30)

    def clean_rent_price(self):
        rent_price = self.cleaned_data.get("rent_price")
        if rent_price < 0:
            raise forms.ValidationError("Rental price cannot be negative!")

        return rent_price

    def clean_suite_num(self):
        """checks for apartments with duplicate suite numbers in the same location"""
        city = self.cleaned_data.get("city")
        state = self.cleaned_data.get("state")
        address = self.cleaned_data.get("address")
        zipcode = self.cleaned_data.get("zipcode")
        suite_num = self.cleaned_data.get("suite_num")
        try:  # If the apartment belongs to a location that already exists
            loc = Location.objects.get(
                city=city, state=state, address=address, zipcode=zipcode
            )
            try:
                Apartment.objects.get(suite_num=suite_num, location=loc)
                raise forms.ValidationError(
                    "An apartment with the same suite number already exists at this location! \
                    If you are the landlord, you can edit the apartment details by going to your account page."
                )
            except Apartment.DoesNotExist:
                return suite_num
        except Location.DoesNotExist:
            # if the apartment belongs to a location that does not exist, we can't have duplicate apartments
            return suite_num