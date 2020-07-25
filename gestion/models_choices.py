from django.db import models
from django.contrib.auth.models import User


class ZonaComercial(models.Model):
  nombre = models.CharField(max_length=50)
  def __str__(self):
    return "{}".format(self.nombre)

class Departamento(models.Model):
  nombre = models.CharField(max_length=50)
  abreviatura = models.CharField(max_length=4)
  zona = models.ForeignKey(ZonaComercial, on_delete=models.CASCADE, default=None, null=True)

  def __str__(self):
    return "{}".format(self.nombre)

class Perfil(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  # zona_comercial = models.ManyToManyField(ZonaComercial, blank=True, null=True)
  celular = models.CharField(max_length=15)
  prefijo = models.CharField(max_length=3)
  bio = models.TextField()

  def __str__(self):
      return  "{}: {}".format(self.user.username, self.user.first_name)