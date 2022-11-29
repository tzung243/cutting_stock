from django import forms


class FileUploadForm(forms.Form):
    file = forms.FileField(label="Import")  # creating file input

