from django.db import models


class Roles(models.Model):
    id = models.IntegerField(primary_key=True, serialize=True)
    name = models.CharField(max_length=255)
    is_admin = models.BooleanField(null=False, default=False)


class User(models.Model):
    id = models.IntegerField(primary_key=True, serialize=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    role = models.ForeignKey(Roles, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
