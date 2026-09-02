from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_POST

from .forms import SignUpForm


def home(request):
    return render(request, 'home.html')


@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return HttpResponseRedirect(next_url)
            return HttpResponseRedirect(reverse('home'))
    else:
        form = AuthenticationForm(request)

    return render(request, 'accounts/login.html', {'form': form})


@require_POST
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
