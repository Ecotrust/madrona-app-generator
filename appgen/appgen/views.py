from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from appgen.models import AppConfig
from appgen.forms import AppConfigForm
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings

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

def active(request):
    ''' 
    determines which app is running
      ACTIVEAPP_DIR/.pk 
    '''
    pth = os.path.join(settings.ACTIVEAPP_DIR, '.pk')
    try:
        pk = int(open(pth).read().strip())
        return pk
    except:
        pass
    return None

def _call(cmd):
    from subprocess import Popen, PIPE, STDOUT, call
    proc = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    proc.wait()
    output = proc.stdout.read()
    returncode = proc.returncode
    return output, returncode

@login_required
def initialize(request, pk): 
    try:
        app = AppConfig.objects.get(pk=pk)
    except AppConfig.DoesNotExist:
        app.cleanup()
        return HttpReponse("Doesn't exist", status=404)

    cmd = app.db_command()
    output, returncode = _call(cmd)
    if len(output) > 0 or returncode == 1:
        app.cleanup()
        raise Exception("`"+ cmd + "` failed: \n" + output)

    cmd = app.create_command()
    output, returncode = _call(cmd)
    if returncode == 1:
        app.cleanup()
        raise Exception(cmd + " failed: " + output)

    return HttpResponseRedirect('/admin/appgen/appconfig/')

@login_required
def activate(request, pk):
    try:
        app = AppConfig.objects.get(pk=pk)
    except AppConfig.DoesNotExist:
        return HttpReponse("Doesn't exist", status=404)

    """
    Apps are in settings.USERAPP_DIR
    The symlinked app is in settings.ACTIVEAPP_DIR 
    The apache and wsgi setup needs to point to the active app dir
    Loading an app involves:
      removing the symlink active app dir
      symlinking to the appropriate folder in user app dir
      touching wsgi (for good measure)
    """
    src = os.path.join(settings.USERAPP_DIR, app.project)
    dest = settings.ACTIVEAPP_DIR
    try:
        os.remove(dest)
    except OSError:
        pass  #symlink doesn't exist

    os.symlink(src, dest)
    return HttpResponseRedirect('/admin/appgen/appconfig/')
