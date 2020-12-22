from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.http import HttpResponse


# Create your views here.
class BaseView(View):
    template_name = 'base_page.html'

    def get(self, request):
        host = request.get_host()
        print(host)
        islocal = host.find('localhost') >= 0 or host.find('127.0.0.1') >= 0
        ctx = {
            'installed': settings.INSTALLED_APPS,
            'islocal': islocal,
        }
        return render(request, self.template_name, ctx)


class HomeView(View):
    template_name = 'home/main.html'

    def get(self, request):
        return render(request, self.template_name)


class EducationDetailView(View):
    template_name = 'home/education.html'

    def get(self, request):
        print('here')
        return render(request, self.template_name)
