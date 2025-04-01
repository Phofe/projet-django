from django.contrib.auth.models import User
from django.db import models
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.urls import reverse

class Gestionnaire(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

class Conducteur(models.Model):
    gestionnaire = models.ForeignKey(Gestionnaire, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenoms = models.CharField(max_length=100)
    date_naissance = models.DateField()
    numero_identification = models.CharField(max_length=50, unique=True)
    numero_assurance = models.CharField(max_length=50)
    type_assurance = models.CharField(max_length=50)
    numero_droit_taxi = models.CharField(max_length=50)
    adresse = models.TextField()
    telephone = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='photos_conducteurs/')
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    def __str__(self):
        return f"{self.nom} {self.prenoms}"

    def get_absolute_url(self):
        return reverse('conducteur_detail', args=[str(self.id)])

    def generate_qr_code(self):
        qr_data = f"Nom: {self.nom} {self.prenoms}\nAdresse: {self.adresse}\nTéléphone: {self.telephone}"
        qr = qrcode.make(qr_data)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        self.qr_code.save(f"qr_{self.id}.png", ContentFile(buffer.getvalue()), save=False)

    def save(self, *args, **kwargs):
        self.generate_qr_code()
        super().save(*args, **kwargs)

class Moto(models.Model):
    conducteur = models.OneToOneField(Conducteur, on_delete=models.CASCADE)
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    annee_fabrication = models.IntegerField()
    immatriculation = models.CharField(max_length=50, unique=True)
    couleur = models.CharField(max_length=50)
    numero_chassis = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.marque} {self.modele} - {self.immatriculation}"

class AgentControle(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gestionnaire = models.ForeignKey(Gestionnaire, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


# Create your models here.
