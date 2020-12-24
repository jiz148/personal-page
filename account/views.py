from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views import View

from .forms import SignUpForm

# Create your views here.


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
            user.profile.birth_date = form.cleaned_data.get('birth_date')
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
