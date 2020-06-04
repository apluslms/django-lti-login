from django.shortcuts import render
from django_lti_login.models import LTIClient

def frontpage(request):
    authed = request.user.is_authenticated
    if callable(authed): authed = authed() # django 1.8

    if authed:
        context = {k: request.session[k] for k in ('course_lms', 'course_id', 'course_label', 'course_name')}
        context['user'] = request.user
        context['login_data'] = sorted(request.session['lti_data'].items())
        return render(request, 'frontpage.html', context)
    else:
        context = {'lti_keys': LTIClient.objects.all().order_by('description', 'key')}
        return render(request, 'frontpage_anon.html', context)
