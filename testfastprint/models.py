from django.db import models

# Create your models here.
class Kategori(models.Model):
    nama = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.nama

class Status(models.Model):
    nama = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.nama

class Produk(models.Model):
    nama = models.CharField(max_length=255, null=False, blank=False)
    harga = models.IntegerField(null=False, blank=False)
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    def __str__(self):
        return self.nama

