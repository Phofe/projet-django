import form
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Conducteur, Moto, AgentControle
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import ConducteurSerializer
from django.contrib.auth.decorators import login_required
from .forms import ConducteurForm, MotoForm, AgentControleForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


def conducteur_detail(request, pk):
    try:
        conducteur = Conducteur.objects.get(pk=pk)
    except Conducteur.DoesNotExist:
        messages.error(request, "Conducteur introuvable.")
        return redirect('dashboard')
    return render(request, 'gestion/conducteur_detail.html', {'conducteur': conducteur})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def conducteur_api(request, pk):
    conducteur = get_object_or_404(Conducteur, pk=pk)
    serializer = ConducteurSerializer(conducteur)
    return Response(serializer.data)


@login_required
def dashboard(request):
    # Vérifier si l'utilisateur fait partie du groupe "Gestionnaire"
    if not request.user.groups.filter(name='Gestionnaire').exists():
        messages.error(request, "Accès réservé aux gestionnaires")
        return redirect('home')

    # Récupérer les objets liés au gestionnaire
    try:
        gestionnaire = request.user.gestionnaire
    except AttributeError:
        messages.error(request, "Profil gestionnaire non configuré")
        return redirect('home')

    return render(request, 'gestion/dashboard.html', {
        'conducteurs': Conducteur.objects.filter(gestionnaire=gestionnaire),
        'agents': AgentControle.objects.filter(gestionnaire=gestionnaire)
    })


@login_required
def conducteur_create(request):
    if not hasattr(request.user, 'gestionnaire'):
        messages.error(request, "Accès refusé : Vous devez être un gestionnaire pour créer un conducteur.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = ConducteurForm(request.POST, request.FILES)
        if 'photo' in request.FILES:
            photo = request.FILES['photo']
            if photo.size > 5 * 1024 * 1024:
                messages.error(request, "Le fichier est trop volumineux (taille maximale : 5 Mo).")
                return render(request, 'gestion/conducteur_form.html', {'form': form})
            if not photo.content_type.startswith('image/'):
                messages.error(request, "Le fichier doit être une image.")
                return render(request, 'gestion/conducteur_form.html', {'form': form})

        conducteur = None  # Initialize conducteur as None
        form = ConducteurForm(request.POST, instance=conducteur)
        if form.is_valid():
            try:
                conducteur = form.save(commit=False)
                conducteur.gestionnaire = request.user.gestionnaire
                conducteur.save()
                messages.success(request, "Conducteur créé avec succès.")
            except Exception as e:
                messages.error(request, "Une erreur est survenue lors de la création du conducteur.")
            return redirect('dashboard')
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = ConducteurForm()

    return render(request, 'gestion/conducteur_form.html', {'form': form})


@login_required
def agent_create(request):
    if not hasattr(request.user, 'gestionnaire'):
        messages.error(request, "Accès refusé : Vous devez être un gestionnaire pour créer un agent.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = AgentControleForm(request.POST)
        if form.is_valid():
            try:
                agent = form.save(commit=False)
                agent.gestionnaire = request.user.gestionnaire
                agent.save()
                messages.success(request, "Agent de contrôle créé avec succès.")
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f"Erreur: {e}")
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = AgentControleForm()

    return render(request, 'gestion/agent_form.html', {'form': form})

@login_required
def conducteur_update(request, pk):
    conducteur = get_object_or_404(Conducteur, pk=pk)
    if not hasattr(request.user, 'gestionnaire') or conducteur.gestionnaire != request.user.gestionnaire:
        messages.error(request, "Accès refusé.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = ConducteurForm(request.POST, request.FILES, instance=conducteur)
        if form.is_valid():
            form.save()
            messages.success(request, "Conducteur mis à jour avec succès.")
            return redirect('conducteur_detail', pk=conducteur.pk)
        else:
            messages.error(request, "Veuillez corriger les erreurs.")
    else:
        form = ConducteurForm(instance=conducteur)

    return render(request, 'gestion/conducteur_form.html', {'form': form})

@login_required
def conducteur_delete(request, pk):
    try:
        conducteur = Conducteur.objects.get(pk=pk)
    except Conducteur.DoesNotExist:
        messages.error(request, "Conducteur introuvable ou déjà supprimé.")
        return redirect('dashboard')
    if request.method == 'POST':
        try:
            conducteur.delete()
            messages.success(request, "Conducteur supprimé avec succès.")
        except Exception as e:
            messages.error(request, "Erreur lors de la suppression du conducteur.")
        return redirect('dashboard')

    return render(request, 'gestion/conducteur_confirm_delete.html', {'conducteur': conducteur})


# Restriction : seul l'administrateur peut créer un gestionnaire
def is_admin(user):
    return user.is_superuser


@user_passes_test(is_admin)
def ajouter_gestionnaire(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            gestionnaire_group = Group.objects.get(name="Gestionnaire")
            user.groups.add(gestionnaire_group)
            messages.success(request, "Gestionnaire ajouté avec succès.")
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'gestion/ajouter_gestionnaire.html', {'form': form})


def home(request):
    return render(request, 'gestion/home.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirection vers le dashboard après une connexion réussie
            return redirect('dashboard')  # 'dashboard' doit être une URL valide dans votre application
        else:
            # Ajout d'un message d'erreur si la connexion échoue
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, 'login.html')
