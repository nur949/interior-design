from django.shortcuts import get_object_or_404, render
from .models import FurnitureItem, FurnitureCategory
from core.remote_assets import FURNITURE_IMAGE_URLS, attach_image_url, attach_many


def furniture_list(request):
    items = list(FurnitureItem.objects.filter(published=True))
    category = request.GET.get('category')
    if category:
        items = [item for item in items if item.category.slug == category]
    attach_many(items, FURNITURE_IMAGE_URLS, 'cover_image')
    return render(request, 'furniture/list.html', {'items': items, 'categories': FurnitureCategory.objects.all(), 'selected_category': category})


def furniture_detail(request, slug):
    item = get_object_or_404(FurnitureItem, slug=slug, published=True)
    attach_image_url(item, FURNITURE_IMAGE_URLS, 'cover_image')
    related = list(FurnitureItem.objects.filter(category=item.category).exclude(pk=item.pk)[:3])
    attach_many(related, FURNITURE_IMAGE_URLS, 'cover_image')
    return render(request, 'furniture/detail.html', {'item': item, 'related': related})
