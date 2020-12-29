from django import forms

from .models import Article


# Create the form class.
class ArticleForm(forms.ModelForm):

    # picture
    upload_field_name = 'picture'

    class Meta:
        model = Article
        fields = ['title', 'text', 'category', 'picture']


# https://docs.djangoproject.com/en/3.0/topics/http/file-uploads/
# https://stackoverflow.com/questions/2472422/django-file-upload-size-limit
# https://stackoverflow.com/questions/32007311/how-to-change-data-in-django-modelform
# https://docs.djangoproject.com/en/3.0/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other
class CommentForm(forms.Form):
    comment = forms.CharField(required=True, max_length=500, min_length=3, strip=True)
