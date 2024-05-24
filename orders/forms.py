from django import forms

from .models import WorkshopReservation
from profiles.models import CustomerProfile, WorkshopBranch
from parts.models import Part, Category, Brand, Car

 
class RequestReservationForm(forms.ModelForm):
    brand= forms.ModelChoiceField(
        queryset=Brand.objects.all().order_by('name'),
        label="Brands",
        # widget=forms.CheckboxSelectMultiple
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.none(),  # We'll set this dynamically
        label="Categories",
        # widget=forms.CheckboxSelectMultiple
    )
    images = forms.ImageField(
        required=False,  # Users are not required to upload images
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        label='Car Images',
    )
    note = forms.CharField(
        required=False,  # 'note' field is not required
        widget=forms.Textarea(attrs={'rows': 4}),
        label='Note',
    )
    # create meta class
    class Meta:
        # specify model to be used
        model = WorkshopReservation
 
        # specify fields to be used
        fields = [
            'customer',
            'workshop',
            'brand',
            'car',
            'categories',
            'images',
            'note'
        ]

    def __init__(self,*args, **kwargs):
        self.branch_id = kwargs.pop('branch_id')
        self.workshop = kwargs.pop('workshop')
        self.customer_id = kwargs.pop('customer_id')
        super(RequestReservationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            if field_name not in ['note', 'images']:
                field.widget.attrs['required'] = 'required'

            
        self.fields['car'].queryset = Car.objects.none()
        self.fields['workshop'].queryset = WorkshopBranch.objects.filter(id=self.workshop.id)
        self.fields['customer'].queryset = CustomerProfile.objects.filter(id=self.customer_id)
        self.fields['categories'].queryset = self.workshop.workshop.categories.all()
        # self.fields['categories'].queryset = workshop.categories.all()

        if 'car' in self.data:
            try:
                brand_id = int(self.data.get('brand'))
                print('brandID', brand_id)
                # workshop = WorkshopBranch.objects.filter(id=self.branch_id).workshop
                self.fields['car'].queryset = Car.objects.filter(brand_id=brand_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['car'].queryset = self.instance.car.brand.car_set.order_by('name')

