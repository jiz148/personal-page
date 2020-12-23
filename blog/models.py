from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings


# Create your models here.
class Category(models.Model):

    name = models.CharField(max_length=50)

    # Shows up in the admin list
    def __str__(self):
        return self.name


class Article(models.Model):

    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(1, "Title must be at least 1 character long")]
    )
    text = models.TextField(
        validators=[MinLengthValidator(1, "Text must be at least 1 character long")]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # medias
    picture = models.FileField(upload_to="article_pic")

    # foreign keys
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    # Many-to-many Fields
    favorites = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Favorite',
        related_name='favorite_article'
    )
    comments = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Comment',
        related_name='comment_owned'
    )

    # Shows up in the admin list
    def __str__(self):
        return self.title


class Comment(models.Model):

    text = models.TextField(
        validators=[MinLengthValidator(1, "Comment must be at least 1 character long")]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # foreign keys
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Shows up in the admin site
    def __str__(self):
        if len(self.text) < 15:
            return self.text
        return self.text[:11] + '...'


class Favorite(models.Model):

    # foreign keys
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # https://docs.djangoproject.com/en/3.0/ref/models/options/#unique-together
    class Meta:
        unique_together = ('article', 'owner')

    def __str__(self):
        return '%s likes %s'%(self.owner.username, self.article.title)
