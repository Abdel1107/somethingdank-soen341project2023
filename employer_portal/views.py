from datetime import date

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.models import Group

from job_postings.models import JobPosting
from .forms import EmployerRegisterForm, EmployerLoginForm, JobPostingForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required

from django.db.models import Q


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
            # user.groups.add(Group.objects.get(name='employers'))

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


@login_required
def manage_job_postings(request):
    search_query = request.GET.get('search')
    job_type_filter = request.GET.get('job_type')
    today = date.today()

    # Retrieve the current user instance
    current_user = request.user

    if search_query:
        available_jobs = JobPosting.objects.filter(Q(title__icontains=search_query))
    elif job_type_filter:
        available_jobs = JobPosting.objects.filter(job_type=job_type_filter)
    else:
        available_jobs = JobPosting.objects.all()

    # Filter out job postings with application deadlines that have already passed
    available_jobs = available_jobs.filter(application_deadline__gte=today)

    # Filter job postings by employer user
    available_jobs = available_jobs.filter(employer=current_user)

    # Sort by earliest deadline
    available_jobs = available_jobs.order_by('application_deadline')

    return render(request, 'employer_portal/manage_job_postings.html', {'job_postings': available_jobs})

@login_required
def create_job_posting(request):
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job_posting = form.save(commit=False)
            job_posting.employer = request.user
            job_posting.save()
            messages.success(request, 'Job posting created successfully.')
            return redirect('employer_portal-manage_job_postings')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = JobPostingForm()
    return render(request, 'employer_portal/create_job_posting.html', {'form': form})