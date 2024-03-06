from django.http import HttpResponse, HttpRequest
from django.template import loader
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic


from django.shortcuts import render

# def index(request):
#     template = loader.get_template('login/templates/index.html')
#     context = {'text': ['ahoj', 'nazdar']}
#
#     return HttpResponse(template.render(context, request))


# def index(request: HttpRequest) -> HttpResponse:
#     context = {'text': ['ahoj', 'nazdar']}
#
#     return render(request, './index.html', context)

class IndexView(generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self):
        return {'text': ['ahoj', 'nazdar', 'bazar']}
    # def get_queryset(self):
    #     return ['ahoj', 'nazdar']
