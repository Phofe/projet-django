from django import forms
from .models import Conducteur, Moto, AgentControle

class ConducteurForm(forms.ModelForm):
    class Meta:
        model = Conducteur
        fields = '__all__'
        exclude = ['qr_code', 'gestionnaire']

class MotoForm(forms.ModelForm):
    class Meta:
        model = Moto
        fields = '__all__'

class AgentControleForm(forms.ModelForm):
    class Meta:
        model = AgentControle
        fields = ['user']