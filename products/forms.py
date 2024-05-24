from django import forms

from .models import Product, Comment
from profiles.models import StoreProfile, StoreBranch
from parts.models import Part, Category, Brand, Car

 
class AddProductForm(forms.ModelForm):
    # store = forms.ModelMultipleChoiceField(
    #     queryset=StoreBranch.objects.none(),  # Use the queryset for stores
    #     label="Stores",
    #     widget=forms.SelectMultiple,  # Use CheckboxSelectMultiple widget
    # )

    brand = forms.ModelChoiceField(
                        queryset=Brand.objects.none(),
                        label="Brands",
                        # widget=forms.CheckboxSelectMultiple
                        )
    car = forms.ModelChoiceField(
                        queryset=Car.objects.none(),
                        label="Model",
                        # widget=forms.CheckboxSelectMultiple
                        )
    category = forms.ModelChoiceField(
                        queryset=Category.objects.none(),
                        label="Categories",
                        # widget=forms.CheckboxSelectMultiple
                        )
    # create meta class
    class Meta:
        # specify model to be used
        model = Product
 
        # specify fields to be used
        fields = [
            'store',
            'brand',
            'car',
            'category',
            'part', 
            'status',
            'price',
            'max_quantity',
            'min_quantity',
            'is_available',
        ]

    def __init__(self,*args, **kwargs):
        self.user = kwargs.pop('user')
        super(AddProductForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['required'] = 'required'
        self.fields['is_available'].widget.attrs['class'] += 'ml-5 h-50'
        

        self.fields['brand'].queryset = Brand.objects.filter(storeprofile=self.user.storeprofile).order_by('name')
        self.fields['category'].queryset = Category.objects.filter(storeprofile=self.user.storeprofile).order_by('name')    
        self.fields['store'].queryset = StoreBranch.objects.filter(store=self.user.storeprofile)
        self.fields['part'].queryset = Part.objects.none()

        if 'part' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['part'].queryset = Part.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['part'].queryset = self.instance.part.category.part_set.order_by('name')

        if 'car' in self.data:
            try:
                brand_id = int(self.data.get('brand'))
                self.fields['car'].queryset = Car.objects.filter(brand_id=brand_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        # elif self.instance.pk:
        #     self.fields['car'].queryset = self.instance.car.brand.car_set.order_by('name')




class AddCommentForm(forms.ModelForm):
    
    class Meta:
        # specify model to be used
        model = Comment
 
        # specify fields to be used
        fields = [
            'content',
            ]
       
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your comment', 'rows':"3",'required': 'required'}),
        }