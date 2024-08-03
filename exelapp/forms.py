from django import forms
from .models import InputFile

class InputFileForm(forms.ModelForm):
    file1 = forms.FileField(label='Input File 1')
    file2 = forms.FileField(label='Input File 2')

    class Meta:
        model = InputFile
        fields = []

