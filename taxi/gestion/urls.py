from django.urls import path
from django.contrib.auth import views as auth_views
from .views import conducteur_create, agent_create, conducteur_detail, dashboard, conducteur_api, conducteur_update, conducteur_delete, ajouter_gestionnaire

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('conducteur/ajouter/', conducteur_create, name='conducteur_create'),
    path('agent/ajouter/', agent_create, name='agent_create'),
    path('conducteur/<int:pk>/modifier/', conducteur_update, name='conducteur_update'),
    path('conducteur/<int:pk>/supprimer/', conducteur_delete, name='conducteur_delete'),
    path('conducteur/<int:pk>/', conducteur_detail, name='conducteur_detail'),

    path('api/conducteur/<int:pk>/', conducteur_api, name='conducteur_api'),
    path('admin/ajouter-gestionnaire/', ajouter_gestionnaire, name='ajouter_gestionnaire'),
path('accounts/login/', auth_views.LoginView.as_view(
        redirect_authenticated_user=True,
        template_name='registration/login.html'
    ), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]
