from django import forms

class UploadFileForm(forms.Form):
    word_file = forms.FileField(required=True)
    data_file = forms.FileField(required=True)
    variable_names = forms.CharField(required=True, initial='name, role, series, pronoun')