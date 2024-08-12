from django.db import models


class Testings(models.Model):
    ficha = models.CharField(max_length=9, null=False)
    aprendiz = models.CharField(max_length=10, null=False)
    instructor = models.CharField(max_length=10, null=False)
    p01 = models.CharField(max_length=1, null=False)
    p02 = models.CharField(max_length=1, null=False)
    p03 = models.CharField(max_length=1, null=False)
    p04 = models.CharField(max_length=1, null=False)
    p05 = models.CharField(max_length=1, null=False)
    p06 = models.CharField(max_length=1, null=False)
    p07 = models.CharField(max_length=1, null=False)
    p08 = models.CharField(max_length=1, null=False)
    p09 = models.CharField(max_length=1, null=False)
    p10 = models.CharField(max_length=1, null=False)
    p11 = models.CharField(max_length=1, null=False)
    p12 = models.CharField(max_length=1, null=False)

    def __str__(self):
        return self.ficha
