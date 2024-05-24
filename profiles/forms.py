from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException

from .models import CustomerProfile, StoreProfile, WorkshopProfile,\
    StoreBranch, WorkshopBranch


class CustomerProfileForm(forms.ModelForm):

    class Meta:
        model = CustomerProfile

        fields = [
            'image',
            'phone_num',
        ]
    
    # def clean_name(self):
    #     name = self.cleaned_data['name']
    #     instance = self.instance  # Get the current instance

    #     # Check if this is a new instance (creating) or an existing one (updating)
    #     if instance.pk is None:
    #         try:
    #             # Check if a StoreProfile with this name already exists
    #             store_profile = StoreProfile.objects.get(name=name)
    #             # If it exists, raise a validation error
    #             raise forms.ValidationError('A store with this name already exists. Please choose a different name.')
    #         except StoreProfile.DoesNotExist:
    #             # If it doesn't exist, it's a valid name
    #             return name
    #     else:
    #         # This is an existing instance, no need to check uniqueness
    #         return name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes and attributes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            if field_name not in ['logo', 'bio']:
                field.widget.attrs['required'] = 'required'


class AddStoreProfile(forms.ModelForm):

    class Meta:
        model = StoreProfile

        fields = [
            'name',
            'brands',
            'categories',
            'bio',
            'logo',
        ]
    
    def clean_name(self):
        name = self.cleaned_data['name']
        instance = self.instance  # Get the current instance

        # Check if this is a new instance (creating) or an existing one (updating)
        if instance.pk is None:
            try:
                # Check if a StoreProfile with this name already exists
                store_profile = StoreProfile.objects.get(name__iexact=name)
                # If it exists, raise a validation error
                raise forms.ValidationError('A store with this name already exists. Please choose a different name.')
            except StoreProfile.DoesNotExist:
                # If it doesn't exist, it's a valid name
                return name
        else:
            # This is an existing instance, no need to check uniqueness
            return name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes and attributes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            if field_name not in ['logo']:
                field.widget.attrs['required'] = 'required'


class AddWorkshopProfile(forms.ModelForm):

    class Meta:
        model = WorkshopProfile

        fields = [
            'name',
            'brands',
            'categories',
            'bio',
            'logo',
        ]
    
    def clean_name(self):
        name = self.cleaned_data['name']
        instance = self.instance  # Get the current instance

        # Check if this is a new instance (creating) or an existing one (updating)
        if instance.pk is None:
            try:
                # Check if a StoreProfile with this name already exists
                workshops_profile = WorkshopProfile.objects.get(name__iexact=name)
                # If it exists, raise a validation error
                raise forms.ValidationError('A workshop with this name already exists. Please choose a different name.')
            except WorkshopProfile.DoesNotExist:
                # If it doesn't exist, it's a valid name
                return name
        else:
            # This is an existing instance, no need to check uniqueness
            return name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes and attributes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            if field_name not in ['logo', 'bio']:
                field.widget.attrs['required'] = 'required'


class AddStoreBranchForm(forms.ModelForm):
    
    class Meta:
        # specify model to be used
        model = StoreBranch
 
        # specify fields to be used
        fields = [
            'branch_name',
            'phone_number',
        ]

    branch_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Branch Name *', 'required': 'required'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number *', 'required': 'required'}))

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_branch_name(self):
        branch_name = self.cleaned_data.get('branch_name')

        # Check if a WorkshopBranch with this name already exists
        if StoreBranch.objects.filter(store=self.request.user.storeprofile,branch_name=branch_name).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('A branch with this name already exists. Please choose a different name.')

        return branch_name
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if not phone_number:
            return phone_number
        # Validate the phone number using phonenumbers

        try:
            parsed_number = phonenumbers.parse(phone_number)
            if not phonenumbers.is_valid_number(parsed_number):
                raise forms.ValidationError('Invalid phone number.')
        except NumberParseException:
            raise forms.ValidationError('Invalid phone number format.')

        # Check if the phone number is already used
        if StoreBranch.objects.filter(phone_number=phone_number).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('This phone number is already used.')

        return phone_number


class AddWorkshopBranchForm(forms.ModelForm):
    
    class Meta:
        # specify model to be used
        model = WorkshopBranch
 
        # specify fields to be used
        fields = [
            'branch_name',
            'phone_number',
        ]

    branch_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Branch Name *', 'required': 'required'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number *', 'required': 'required'}))

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.request = request



    def clean_branch_name(self):
        branch_name = self.cleaned_data.get('branch_name')

        # Check if a WorkshopBranch with this name already exists
        if WorkshopBranch.objects.filter(workshop=self.request.user.workshopprofile,branch_name=branch_name).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('A branch with this name already exists. Please choose a different name.')

        return branch_name
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if not phone_number:
            return phone_number
        # Validate the phone number using phonenumbers
        try:
            parsed_number = phonenumbers.parse(phone_number)
            if not phonenumbers.is_valid_number(parsed_number):
                raise forms.ValidationError('Invalid phone number.')
        except NumberParseException:
            raise forms.ValidationError('Invalid phone number format.')

        # Check if the phone number is already used
        if WorkshopBranch.objects.filter(phone_number=phone_number).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('This phone number is already used.')
        
        return phone_number
    


    # branch_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Branch Name *', 'required': 'required'}))
    # _1st_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+21891*******', 'required': 'required'}))
