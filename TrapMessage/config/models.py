from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Config(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="Name")
    ip = models.GenericIPAddressField(verbose_name="IP Address")
    udp = models.IntegerField(verbose_name="UDP Port")
    community = models.CharField(max_length=20, verbose_name="Community")
    users = models.ManyToManyField(User, related_name="configs")

    def __str__(self):
        return f"Configuration: {self.name}"

    def get_absolute_url(self):
        return reverse('config:config_details', kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("config:config_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("config:config_delete", kwargs={"pk": self.pk})
