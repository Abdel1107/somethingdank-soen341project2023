"""connect_u URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from student_portal.views import home, RegisterView

from django.contrib.auth import views as auth_views
from student_portal.views import CustomLoginView, profile, job_postings
from student_portal.forms import LoginForm

from django.conf import settings
from django.conf.urls.static import static

from employer_portal.views import employer_home, EmployerRegisterView, EmployerCustomLoginView, manage_job_postings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('student_portal.urls')),
    path('register/', RegisterView.as_view(), name='student_portal-register'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='student_portal/login.html',
                                           authentication_form=LoginForm), name='student_portal-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='student_portal/logout.html'),
         name='student_portal-logout'),
    path('profile/', profile, name='student_portal-profile'),
    path('job_postings/', job_postings, name='student_portal-job_postings'),

    path('employer_home/', employer_home, name='employer_portal-home'),
    path('employer_register/', EmployerRegisterView.as_view(), name='employer_portal-register'),
    path('employer_login/', EmployerCustomLoginView.as_view(redirect_authenticated_user=True, template_name='employer_portal/login.html',
                                           authentication_form=LoginForm), name='employer_portal-login'),
    path('employer_logout/', auth_views.LogoutView.as_view(template_name='employer_portal/logout.html'),
         name='employer_portal-logout'),
    path('manage_job_postings/', manage_job_postings, name='employer_portal-manage_job_postings'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
