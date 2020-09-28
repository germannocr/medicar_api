from django.db import models
from django.contrib.postgres.fields import ArrayField


class Especialidade(models.Model):
    """
    The Especialidade represents a medical specialty.
    """
    id = models.AutoField(primary_key=True, unique=True)
    nome = models.CharField(max_length=60)

    class Meta:
        db_table = 'especialidade'


class Medico(models.Model):
    """
    The Medico represents a doctor.
    """
    id = models.AutoField(primary_key=True, unique=True)
    nome = models.CharField(max_length=60)
    crm = models.IntegerField()
    email = models.CharField(max_length=120)
    telefone = models.CharField(max_length=60)
    especialidade = models.ForeignKey(Especialidade, on_delete=models.CASCADE)

    class Meta:
        db_table = 'medico'


class Agenda(models.Model):
    """
    The Agenda represents a medical schedule.
    """
    id = models.AutoField(primary_key=True, unique=True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    dia = models.DateField(auto_now=False, auto_now_add=False)
    horarios = ArrayField(models.TimeField(auto_now_add=False))

    class Meta:
        db_table = 'agenda'


class Consulta(models.Model):
    """
    The Consulta represents a medical appointment.
    """
    id = models.AutoField(primary_key=True, unique=True)
    dia = models.DateField(auto_now=False, auto_now_add=False)
    horario = models.TimeField(auto_now=False, auto_now_add=False)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    data_agendamento = models.DateTimeField(auto_now_add=True)
    created_by_user = models.IntegerField()

    class Meta:
        db_table = 'consulta'
