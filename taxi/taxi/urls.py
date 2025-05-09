"""
URL configuration for taxi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from gestion import views as gestion_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', gestion_views.home, name='home'),  # Page d'accueil
    path('custom-login/', gestion_views.custom_login, name='custom_login'),  # Vue personnalisée
    path('dashboard/', gestion_views.dashboard, name='dashboard'),  # Dashboard
    path('accounts/', include('django.contrib.auth.urls')),  # Authentification Django
]

