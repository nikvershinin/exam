from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import *

class PostForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['author']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), label='Содержимое')
