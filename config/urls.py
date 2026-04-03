from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.shortcuts import render

handler404 = 'core.views.custom_404'

urlpatterns = [
    path('', include('core.urls')),
    path('blog/', include('blog.urls')),
    path('furniture/', include('furniture.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('contact/', include('contact.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
