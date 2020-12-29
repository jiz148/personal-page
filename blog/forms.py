from django import forms

from .models import Article
from .humanize import naturalsize


# Create the form class.
class ArticleForm(forms.ModelForm):

    # picture

    upload_field_name = 'picture'
    # get max_upload_size from picture field
    max_upload_size = Article._meta.get_field('picture').max_upload_size
    max_upload_size_natural = naturalsize(max_upload_size)

    class Meta:
        model = Article
        fields = ['title', 'text', 'category', 'picture']


# https://docs.djangoproject.com/en/3.0/topics/http/file-uploads/
# https://stackoverflow.com/questions/2472422/django-file-upload-size-limit
# https://stackoverflow.com/questions/32007311/how-to-change-data-in-django-modelform
# https://docs.djangoproject.com/en/3.0/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other
class CommentForm(forms.Form):
    comment = forms.CharField(required=True, max_length=500, min_length=3, strip=True)
