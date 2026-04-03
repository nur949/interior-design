from django.shortcuts import get_object_or_404, render
from .models import PortfolioProject
from core.remote_assets import PROJECT_IMAGE_URLS, attach_image_url, attach_many


def portfolio_list(request):
    projects = list(PortfolioProject.objects.filter(published=True))
    attach_many(projects, PROJECT_IMAGE_URLS, 'cover_image')
    return render(request, 'portfolio/list.html', {'projects': projects})


def portfolio_detail(request, slug):
    project = get_object_or_404(PortfolioProject, slug=slug, published=True)
    attach_image_url(project, PROJECT_IMAGE_URLS, 'cover_image')
    related = list(PortfolioProject.objects.exclude(pk=project.pk)[:3])
    attach_many(related, PROJECT_IMAGE_URLS, 'cover_image')
    return render(request, 'portfolio/detail.html', {'project': project, 'related': related})
