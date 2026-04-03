from django.db import models
from django.urls import reverse

class FurnitureCategory(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)
    def __str__(self): return self.name

class FurnitureItem(models.Model):
    category = models.ForeignKey(FurnitureCategory, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    subtitle = models.CharField(max_length=180)
    description = models.TextField()
    material = models.CharField(max_length=150)
    dimensions = models.CharField(max_length=150)
    price_label = models.CharField(max_length=80, default='Custom Quote')
    cover_image = models.ImageField(upload_to='furniture/')
    gallery_image = models.ImageField(upload_to='furniture/gallery/', blank=True)
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title
    def get_absolute_url(self): return reverse('furniture_detail', args=[self.slug])
