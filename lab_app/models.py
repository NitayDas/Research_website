from django.db import models

# Create your models here.
class BannerImage(models.Model):
    image = models.ImageField(upload_to='banner/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)