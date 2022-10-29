from django import forms
from django.core.exceptions import ValidationError
from .models import *
from django.db.models import Q


class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = '__all__'


class BomForm(forms.ModelForm):
    class Meta:
        model = BOM
        fields = '__all__'


class BlueprintFormChoice(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BlueprintFormChoice, self).__init__(*args, **kwargs)
        choices = Blueprint.objects.all()
        self.fields['blueprints'] = forms.ModelChoiceField(queryset=choices, empty_label='Choose blueprint')

    class Meta:
        model = Blueprint
        exclude = ['blueprint_name']


class AddBlueprintForm(forms.ModelForm):
    class Meta:
        model = Blueprint
        fields = '__all__'


class AddPartToBOM(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddPartToBOM, self).__init__(*args, **kwargs)

    def clean_part(self):
        blueprint_id = self.cleaned_data['blueprint']
        part_id = self.cleaned_data['part']
        query = BOM.objects.filter(Q(blueprint=blueprint_id) & Q(part=part_id))
        if query:
            raise ValidationError('Part already exists')
        return part_id

    class Meta:
        model = BOM
        fields = '__all__'
        widgets = {'blueprint': forms.HiddenInput()}


class FillInventoryForm(forms.ModelForm):

    class Meta:
        model = Inventory
        fields = '__all__'
        widgets = {'usage': forms.HiddenInput(),
                   'blueprint': forms.HiddenInput(attrs={'required': False}),
                   'device': forms.HiddenInput(attrs={'required': False})
                   }

