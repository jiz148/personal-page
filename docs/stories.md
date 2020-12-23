# Personal Page Stories
> Here are stories about creating my personal page using Django, codes apply to Django 3.1.4 


## Basic Django Structure
![django structure image](Django_life_cycle.png)


## Content

* [Initiate Project](#initiate)
  - [Start a New Project](#start)
  - [Config the Django Project](#config-p)
    - [Static Files](#static)
    - [Media Files](#media)
* [Front-end](#front)
  - [Config App Settings](#config-a)
  - [Config Template Settings](#config-t)
  - [Download Bootstrap and jQuery to Local](#b-and-j)
  - [Create General Templates](#templates)
    - [Base Bootstrap](#base-boostrap)
    - [Base Page](#base-page)
        - [Build Ajax](#ajax)
  - [Create Home Page](#home-page)
* [Back-end](#back)
  - [Home Page Back-end](#home-back)
  - [Blog Back-end](#blog-back)
* [Deployment](#deploy)
  - [Secret Key](#secret)
  - [Config Deployment Settings](#config-d)


<a id="initiate"></a>
## Initiate Project


<a id="start"></a>
### Start a New Project

* Create a github repo, edit .gitignore
* Create virtual environment, mine:
  - `virtualenv -p python3.7 .venv`
  - `source .venv/bin/activate`
  - `pip install django`
  - `pip freeze > requirments.txt`
* Create new project called 'mysite': 
  - `Django-Admin startproject mysite`
  - Move the inside project folder to github folder if you like
  - `python manage.py check`
* Create first home app:
  - `python manage.py startapp home`
* First migrate to start the project: 
  - `python manage.py migrate`
  - In settings `INSTALLED_APPS` add `'home.apps.HomeConfig',`
    

<a id="config-p"></a>
### Config the Django Project


<a id="config-a"></a>
#### Config App Settings

* Config the `APP_NAME` to the webpage name


<a id="static"></a>
#### Static files

* [Django Document for Static Files](https://docs.djangoproject.com/en/3.1/howto/static-files/) as this may change as version evolves
* In settings.py, add `STATIC_URL = '/static/'`
* Set static directories like:
  - ```python
    STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'utils/static/'),
    os.path.join(BASE_DIR, 'home/templates/home/home_js/'),
    )```
* Set a static root for server end, for me: `STATIC_ROOT = 'static'`
* Set static url, according to Django document, in `mysite/urls.py`, add `urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)`
* Collect static files in static directories to server-side static root by: `python manage.py collectstatic`


<a id="media"></a>
#### Media Files

* [reference](https://www.cnblogs.com/harryTree/p/11865900.html)
* Config `MEDIA_ROOT = os.path.join( BASE_DIR  ,  "media"  )`
* In `mysite/url.py`, puste `urlpatterns += re_path(r"^media/(?P<path>.*)/", serve, {"document_root": settings.MEDIA_ROOT})`


<a id="front"></a>
## Front-end


<a id="config-t"></a>
### Config Template Settings

* Create ctx_processor.py and give:
  - ```python
    from django.conf import settings as django_settings
    
    def settings(request):
      return {
          'settings': django_settings,
      }
    ```
* Go to settings and add `'mysite.ctx_processor.settings',` to list `TEMPLATES`


<a id="b-and-j"></a>
### Download Bootstrap and jQuery to Local

> In this project I use Bootstrap v4.5.3 and jQuery 3.5.1
> It is also common to use React and Vanilla Javascript in front-end

* Download Boostrap and jQuery, 
* `mkdir utils`
* Copy the files to utils
* Put utils folder in `STATICFILES_DIRS`
* Collect


### Creating General Templates

> I create Django templates using bootstrap and jQuery


#### Base Bootstrap

> base_boostrap.html\
> First layer, just to import utils and create big structure

* According to [Django Document for Static Files](https://docs.djangoproject.com/en/3.1/howto/static-files/), `{% load static %}`
* Load first static resources
* In `<body>`, create needed blocks like `{% block navbar %} {% endblock %}`, `{% block content %} {% endblock %}` `{% block footer %} {% endblock %}`
* Some extra blocks: welcome, messages(alert)


<a id="base-page"></a>
#### Base Page

> base_page.html \
> Second layer, basically implementing the navbar and footer \
> For overall functionalities across the site \
> Also implementing Ajax in this page \
> [reference](https://codepen.io/joycousc/pen/RwrVBYe)


##### Navbar

* [Bootstrap Document](https://getbootstrap.com/docs/4.5/components/navbar/)
* Should use from settings for app name and urls
* Should use `class="navbar-toggler"` and `class="collapse navbar-collapse justify-content-end"` for navbar-toggle for mobile devices
* Should `fixed-top`


##### Header

* Should retain space for navbar 


##### Footer

* Should include a footer at the bottom in the `{% block footer %}`
* Should include copy right html entity and some external links to other personal spaces


<a id="ajax"></a>
##### Build Ajax
* Should put the ajax javascript in base_static/base_js folder and then add the root to `STATICFILES_DIRS`
* Should import js from static
* Implementing Ajax using jQuery
* Give the DOM ajax object with ajax functions after loading the page
* [base.js](../home/templates/base_static/base_js/base.js)


<a id="home-page"></a>
### Create Home Page

* Should include static file directory home_static
* Should include Education session
* Should include Experience session
* Should include Hobbies session


#### Write Home Details

* Should have Details for Education, Experience, Hobbies in 3 other templates


<a id="back"></a>
## Back-end


<a id="home-back"></a>
### Home Page Back-end

* Should have an url and a view to just render main.html


<a id="blog-back"></a>
### Blog Back-end


#### Create Blog Model

![blog structure](blog_structure.png)
* `python manage.py startapp blog`
* Add new app in settings
* [models.py](../blog/models.py)
* Follow the structure of blog,  for example `class Category(models.Model):`
* For pictures(single picture for now), use `picture = models.FileField(upload_to="article_pic")`
* Each model should implement `__str__` for showing in admin
* `favorites` and `comments` field in `Article` class should be `models.ManyToManyField`
* Should have `Favorite` and `Comment` helper Many-To-Many class for comments and favorites
* Add `Category` and `Article` class to [admin.py](../blog/admin.py)
* `python manage.py makemigrations`, `python manage.py migrate`


#### About Superuser

> Just for future as a cheat sheet:)
> Right now I'm using the Django built-in admin site for convenience
> It's because if I'm building my own, it's going to be thousands of extra lins of code
> and mostly it;s going to be functionally homogeneous to the built-in one

* Add `'django.contrib.admin',` to `INSTALLED_APPS`
* Add `path('admin/', admin.site.urls),` to `mysite/urls.py`
* Create a superuser by `python manage.py createsuperuser`
* Delete a superuser by:
  - ```
    > django-admin.py shell
    $ from django.contrib.auth.models import User
    $ User.objects.get(username="joebloggs", is_superuser=True).delete()
    ```


<a id="deploy"></a>
## Deployment


<a id="secret"></a>
### Secret Key

> The secret key is used for:
> * All sessions if you are using any other session backend than django.contrib.sessions.backends.cache, or are using the default get_session_auth_hash().
> * All messages if you are using CookieStorage or FallbackStorage.
> * All PasswordResetView tokens.
> * Any usage of cryptographic signing, unless a different key is provided.
> 
> * [reference](https://www.cnblogs.com/cpl9412290130/p/10431514.html)

* In settings, config `SECRET_KEY` to `os.environ["DJ_SECRET_KEY"]`
* In linux, do `export DJ_SECRET_KEY="xxxxxxxx"`, if not a server you can store it in rc
* In windows, do `$env:DJ_SECRET_KEY="xxxxxxxx"`, and if not a server you can store commends in `$profile` for powershell


<a id="config-d"></a>
### Config Deployment Settings

* Config the `ALLOWED_HOST` by adding `['*']`
