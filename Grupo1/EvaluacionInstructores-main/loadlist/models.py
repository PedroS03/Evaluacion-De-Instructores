from django.db import models


class Instructor(models.Model):

    FICHA = models.CharField(max_length=9, null=False)
    PROGRAMA_DE_FORMACION = models.CharField(max_length=200, null=True)
    TIPO_DOCUMENTO = models.CharField(max_length=4, null=True)
    NUMERO_DE_DOCUMENTO_INSTRUCTOR = models.CharField(max_length=10, null=False)
    NOMBRE = models.CharField(max_length=150, null=False)
    APELLIDOS = models.CharField(max_length=150, null=False)
    PERFIL_DEL_INSTRUCTOR = models.CharField(max_length=200, null=True)
    GRUPO = models.CharField(max_length=20, null=False)
    HASH = models.CharField(max_length=50, null=False)
    HASH_SEND = models.DateTimeField(null=False)
    PICTURE = models.CharField(max_length=200, null=True)
    FECHA_DE_UPLOAD = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.NOMBRE


class Aprendiz(models.Model):

    FICHA = models.CharField(max_length=9, null=False)
    TIPO_DE_DOCUMENTO = models.CharField(max_length=4, null=True)
    NUMERO_DE_DOCUMENTO = models.CharField(max_length=10, null=False)
    NOMBRE = models.CharField(max_length=150, null=False)
    APELLIDOS = models.CharField(max_length=150, null=False)
    CELULAR = models.CharField(max_length=10, null=True)
    CORREO_ELECTRONICO = models.CharField(max_length=200, null=False)
    ESTADO = models.CharField(max_length=50, null=True)
    GRUPO = models.CharField(max_length=20, null=False)
    HASH = models.CharField(max_length=50, null=False)
    HASH_SEND = models.DateTimeField(null=False)
    FECHA_DE_UPLOAD = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.NOMBRE


class Evaluacion(models.Model):

    REGIONAL = models.CharField(max_length=50, null=True)
    CENTRO = models.CharField(max_length=50, null=True)
    FECHA_LISTAS = models.DateTimeField(null=False)
    FECHA_EVALUACION = models.DateTimeField(null=False)
    FECHA_DE_SOLICITUD = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.CENTRO


class Coordinador(models.Model):

    REGIONAL = models.CharField(max_length=50, null=True)
    CENTRO = models.CharField(max_length=50, null=True)
    COORDINACION = models.CharField(max_length=50, null=True)
    NOMBRE = models.CharField(max_length=150, null=False)
    APELLIDOS = models.CharField(max_length=150, null=False)
    EMAIL = models.CharField(max_length=200, null=True)
    GRUPO = models.CharField(max_length=20, null=False)
    HASH = models.CharField(max_length=50, null=False)
    HASH_SEND = models.DateTimeField(null=False)
    FECHA_DE_UPLOAD = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.COORDINACION
