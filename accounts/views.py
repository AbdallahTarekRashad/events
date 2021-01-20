from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:home')
    template_name = 'accounts/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:home')
        else:
            return super(SignUpView, self).get(request, *args, **kwargs)

    # overwrite form_valid function to login after save object
    def form_valid(self, form):
        response = super(SignUpView, self).form_valid(form)
        login(self.request, self.object)
        return response


def login_view(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                if request.GET:
                    if request.GET.get('next', None):
                        return redirect(request.GET.get('next'))
                else:
                    return redirect('accounts:home')
    if request.user.is_authenticated:
        return redirect('accounts:home')
    return render(request, 'accounts/login.html', {'form': AuthenticationForm})


@login_required
def home(request):
    return render(request, 'accounts/test.html')
