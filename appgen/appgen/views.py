from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from appgen.models import AppConfig
from appgen.forms import AppConfigForm
from django.contrib.auth.decorators import login_required

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

@login_required
def load(request, pk):
    try:
        app = AppConfig.objects.latest('pk')
    except AppConfig.DoesNotExist:
        return HttpReponse("Doesn't exist", status=404)

    """
    Apps are in settings.USERAPP_DIR
    The symlinked app is in settings.ACTIVEAPP_DIR (/usr/local/apps/active) 
    The apache and wsgi setup needs to point to the active app dir
    Loading an app involves:
      removing the symlink active app dir
      symlinking to the appropriate folder in user app dir
      touching wsgi (for good measure)
      ACTIVEAPP_DIR/.pk is written containing the app's pk
    """
    src = os.path.join(settings.USERAPP_DIR, app.appslug)
    dest = settings.ACTIVEAPP_DIR

    if os.path.exists(dest):
        os.remove(dest)

    os.symlink(src, dest)
    if not os.path.exists(dest):
        raise Exception("symlink failed")
    
    return HttpResponse("Server restarted for %s; running on \
            <a href='%s'>%s</a>." % (app.app, app.domain, app.domain) , status=200)
