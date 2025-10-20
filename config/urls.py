"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.shortcuts import redirect
# Redirect root ("/") to register page
def redirect_to_register(request):
    return redirect("users:register_page")

urlpatterns = [
    # admin site
    path('admin/', admin.site.urls),
    # Default route redirects to register page
    path('', redirect_to_register, name='home'),
    # Mount the users app under /api/users/
    path('api/users/', include('users.urls')),

    # Users (register, login, dashboard, etc.)
    path('users/', include('users.urls', namespace='users')),
    # Events (list, add, details, etc.)
    path('events/', include(('events.urls', 'events'), namespace='events')),

    # Registration API
    path('api/registrations/', include(('registration.urls', 'registration'), namespace='registration')),
]

