from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.models import Group

from .forms import EmployerRegisterForm, EmployerLoginForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


# Create your views here.
def employer_home(request):
    return render(request, 'employer_portal/home.html')


class EmployerRegisterView(View):
    form_class = EmployerRegisterForm
    initial = {'key': 'value'}
    template_name = 'employer_portal/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(EmployerRegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()

            # Add user to "employers" group
            user.groups.add(Group.objects.get(name='employers'))

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='employer_portal-login')

        return render(request, self.template_name, {'form': form})


class EmployerCustomLoginView(LoginView):
    form_class = EmployerLoginForm
    success_url = reverse_lazy('employer_portal-home')

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(EmployerCustomLoginView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('employer_portal-home')