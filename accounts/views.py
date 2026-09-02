from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_POST

from .forms import SignUpForm


def home(request):
    return HttpResponse('ok')


@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'GET':
        return HttpResponse(status=200)

    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return HttpResponseRedirect(reverse('home'))
    return HttpResponseBadRequest(form.errors.as_json(), content_type='application/json')


@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'GET':
        return HttpResponse(status=200)

    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        login(request, form.get_user())
        next_url = request.POST.get('next') or request.GET.get('next')
        if next_url:
            return HttpResponseRedirect(next_url)
        return HttpResponseRedirect(reverse('home'))
    return HttpResponseBadRequest(form.errors.as_json(), content_type='application/json')


@require_POST
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
