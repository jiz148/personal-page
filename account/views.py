from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .forms import SignUpForm, UpdateForm
from blog.views import _get_favorites
from blog.models import Article


class SignUp(View):
    template_name = 'registration/signup.html'

    def get(self, request):
        form = SignUpForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal

            # save extra info for profile
            user.profile.email = form.cleaned_data.get('email')
            user.profile.bio = form.cleaned_data.get('bio')
            user.profile.location = form.cleaned_data.get('location')
            user.save()

            # login use
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return redirect('/')

        else:
            form = SignUpForm(request.POST)
        return render(request, self.template_name, {'form': form})


class Update(View):
    template_name = 'registration/update.html'

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        if request.user != user:
            return redirect('/')
        form = UpdateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        if request.user != user:
            return redirect('/')
        form = UpdateForm(request.POST)
        if form.is_valid():
            # update info for profile
            user.profile.email = form.cleaned_data.get('email')
            user.profile.bio = form.cleaned_data.get('bio')
            user.profile.location = form.cleaned_data.get('location')
            user.save()

            return redirect('/')

        else:
            form = SignUpForm(request.POST)
        return render(request, self.template_name, {'form': form})


class Profile(View):

    template_name = 'profile/profile.html'

    def get(self, request):
        # favorites
        favorites = list()
        if request.user.is_authenticated:
            favorites = _get_favorites(request)
        favorite_articles = []
        for article_id in favorites:
            favorite_articles.append(get_object_or_404(Article, pk=article_id))
        my_articles = Article.objects.filter(owner=request.user)
        ctx = {
            'favorite_articles': favorite_articles,
            'my_articles': my_articles
        }
        return render(request, self.template_name, ctx)
