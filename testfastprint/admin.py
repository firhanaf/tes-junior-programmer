from django.contrib import admin
from django.contrib.auth.models import User

from .models import *
# Register your models here.
admin.site.register(Produk)
admin.site.register(Kategori)
admin.site.register(Status)