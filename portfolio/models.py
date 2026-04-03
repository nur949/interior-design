from django.db import models
from django.urls import reverse

class PortfolioProject(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    client = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    scope = models.CharField(max_length=150)
    summary = models.TextField()
    challenge = models.TextField()
    solution = models.TextField()
    result = models.TextField()
    cover_image = models.ImageField(upload_to='portfolio/')
    completed_on = models.DateField()
    published = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    def __str__(self): return self.title
    def get_absolute_url(self): return reverse('portfolio_detail', args=[self.slug])

class ProjectImage(models.Model):
    project = models.ForeignKey(PortfolioProject, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='portfolio/gallery/')
    caption = models.CharField(max_length=180, blank=True)
