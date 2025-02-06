from django import forms
from account.models import User
from django.shortcuts import get_object_or_404
import jwt
from django.conf import settings


class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control' , 'rows': 3}))