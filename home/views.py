from django.shortcuts import render
from django.views import View
from django.conf import settings


# Create your views here.
class HomeView(View):
    template_name = 'home/main.html'

    def get(self, request):
        host = request.get_host()
        print(host)
        islocal = host.find('localhost') >= 0 or host.find('127.0.0.1') >= 0
        ctx = {
            'installed': settings.INSTALLED_APPS,
            'islocal': islocal,
        }
        return render(request, self.template_name, ctx)
