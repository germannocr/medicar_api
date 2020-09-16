from django.contrib.postgres.fields import ArrayField
from django.db import models


class Especialidade(models.Model):
    """
    The Especialidade represents a task.
    """

    class Meta:

        db_table = 'especialidade'

    id = models.AutoField(primary_key=True, unique=True)
    nome = models.CharField(max_length=60)


class Medico(models.Model):
    """
    The Especialidade represents a task.
    """

    class Meta:

        db_table = 'medico'

    id = models.AutoField(primary_key=True, unique=True)
    nome = models.CharField(max_length=60)
    crm = models.IntegerField()
    email = models.CharField(max_length=120)
    telefone = models.CharField(max_length=60)
    especialidade = models.ForeignKey(Especialidade, on_delete=models.CASCADE)


class Agenda(models.Model):
    """
    The Especialidade represents a task.
    """

    class Meta:

        db_table = 'agenda'

    id = models.AutoField(primary_key=True, unique=True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    dia = models.DateField(auto_now=False, auto_now_add=False)
    horarios = ArrayField(models.CharField(max_length=5))
