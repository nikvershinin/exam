from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import *

class PostForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'