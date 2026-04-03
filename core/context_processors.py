from .models import SiteSettings
from .remote_assets import HERO_IMAGE_URL


def site_settings(request):
    return {
        'site_settings': SiteSettings.objects.first(),
        'hero_image_url': HERO_IMAGE_URL,
    }
