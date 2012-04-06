from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from appgen.models import AppConfig
from appgen.forms import AppConfigForm

def main(request):
    try:
        app = AppConfig.objects.latest('pk')
        form = AppConfigForm(instance=app)
    except AppConfig.DoesNotExist:
        form = AppConfigForm()

    context = {}
    context.update({
        'form': form,
    })
    c = RequestContext(request, context)
    return render_to_response("form.html", c)

def reload(request, pk):
    try:
        app = AppConfig.objects.latest('pk')
    except AppConfig.DoesNotExist:
        return HttpReponse("Doesnt exist", status=404)

    return HttpResponse("Server restarted for %s; running on <a href='%s'>%s</a>." % (app.app, app.domain, app.domain) , status=200)
