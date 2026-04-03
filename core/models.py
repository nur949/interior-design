from django.db import models

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=120, default='Atelier Habitat')
    tagline = models.CharField(max_length=200, default='Interior stories, furniture curation, and spatial elegance.')
    hero_title = models.CharField(max_length=200, default='Curated interiors for modern living')
    hero_subtitle = models.TextField(default='A premium editorial platform blending interior design insights, furniture selections, and portfolio-driven storytelling for discerning homeowners and boutique hospitality brands.')
    about_text = models.TextField(default='Atelier Habitat is a Dhaka-rooted interior design editorial brand focused on warm minimalism, layered textures, and functional luxury across residential and boutique commercial spaces.')
    contact_email = models.EmailField(default='hello@atelierhabitat.com')
    phone = models.CharField(max_length=50, default='+880 1700-000000')
    address = models.CharField(max_length=255, default='Gulshan Avenue, Dhaka, Bangladesh')
    map_embed = models.TextField(blank=True)
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    meta_description = models.CharField(max_length=255, default='Luxury interior design and furniture blog with portfolio case studies and contact-ready lead generation.')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.site_name
