from django.db import models

class GalleryImage(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Imagem {self.pk}"
