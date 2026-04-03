from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from blog.models import BlogPost, Category, Tag
from furniture.models import FurnitureItem
from portfolio.models import PortfolioProject
from contact.forms import SubscriberForm
from contact.models import ContactMessage, Subscriber
from core.models import SiteSettings
from blog.forms import BlogPostForm
from furniture.forms import FurnitureItemForm
from portfolio.forms import PortfolioProjectForm
from core.remote_assets import attach_many, BLOG_IMAGE_URLS, FURNITURE_IMAGE_URLS, PROJECT_IMAGE_URLS


def home(request):
    featured_posts = list(BlogPost.objects.filter(published=True, featured=True)[:3])
    latest_posts = list(BlogPost.objects.filter(published=True)[:6])
    featured_furniture = list(FurnitureItem.objects.filter(published=True, featured=True)[:6])
    featured_projects = list(PortfolioProject.objects.filter(published=True, featured=True)[:4])
    attach_many(featured_posts, BLOG_IMAGE_URLS, 'featured_image')
    attach_many(latest_posts, BLOG_IMAGE_URLS, 'featured_image')
    attach_many(featured_furniture, FURNITURE_IMAGE_URLS, 'cover_image')
    attach_many(featured_projects, PROJECT_IMAGE_URLS, 'cover_image')
    context = {
        'featured_posts': featured_posts,
        'latest_posts': latest_posts,
        'featured_furniture': featured_furniture,
        'featured_projects': featured_projects,
        'subscriber_form': SubscriberForm(),
    }
    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html', {
        'team_stats': [
            ('Projects Styled', 48), ('Custom Furniture Lines', 16), ('Editorial Guides', 28), ('Lead Conversion Rate', '31%')
        ]
    })


def search(request):
    query = request.GET.get('q', '')
    posts = BlogPost.objects.filter(Q(title__icontains=query) | Q(content__icontains=query), published=True) if query else []
    furniture = FurnitureItem.objects.filter(Q(title__icontains=query) | Q(description__icontains=query), published=True) if query else []
    projects = PortfolioProject.objects.filter(Q(title__icontains=query) | Q(summary__icontains=query), published=True) if query else []
    return render(request, 'core/search.html', {'query': query, 'posts': posts, 'furniture': furniture, 'projects': projects})


def newsletter_subscribe(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            Subscriber.objects.get_or_create(email=form.cleaned_data['email'])
            messages.success(request, 'Thanks for subscribing to Atelier Habitat.')
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def custom_404(request, exception):
    return render(request, 'core/404.html', status=404)


def dashboard_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard_home')
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('dashboard_home')
    return render(request, 'dashboard/login.html', {'form': form})

@login_required

def dashboard_logout(request):
    logout(request)
    return redirect('dashboard_login')

@login_required

def dashboard_home(request):
    context = {
        'post_count': BlogPost.objects.count(),
        'furniture_count': FurnitureItem.objects.count(),
        'project_count': PortfolioProject.objects.count(),
        'lead_count': ContactMessage.objects.count(),
        'recent_messages': ContactMessage.objects.order_by('-created_at')[:5],
        'recent_posts': BlogPost.objects.order_by('-created_at')[:5],
    }
    return render(request, 'dashboard/index.html', context)

@login_required

def settings_edit(request):
    obj, _ = SiteSettings.objects.get_or_create(pk=1)
    from django.forms import modelform_factory
    SettingsForm = modelform_factory(SiteSettings, exclude=[])
    form = SettingsForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save(); messages.success(request, 'Site settings updated.'); return redirect('dashboard_settings')
    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Site Settings'})

@login_required

def post_manage(request):
    return render(request, 'dashboard/list.html', {'title':'Blog Posts', 'objects': BlogPost.objects.all(), 'create_url':'dashboard_post_create', 'edit_name':'dashboard_post_edit'})
@login_required

def post_create(request):
    form = BlogPostForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False); obj.author = request.user; obj.save(); form.save_m2m(); return redirect('dashboard_posts')
    return render(request, 'dashboard/form.html', {'form': form, 'title':'Create Blog Post'})
@login_required

def post_edit(request, pk):
    obj = get_object_or_404(BlogPost, pk=pk)
    form = BlogPostForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save(); return redirect('dashboard_posts')
    return render(request, 'dashboard/form.html', {'form': form, 'title':'Edit Blog Post'})

@login_required

def furniture_manage(request):
    return render(request, 'dashboard/list.html', {'title':'Furniture Items', 'objects': FurnitureItem.objects.all(), 'create_url':'dashboard_furniture_create', 'edit_name':'dashboard_furniture_edit'})
@login_required

def furniture_create(request):
    form = FurnitureItemForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid(): form.save(); return redirect('dashboard_furniture')
    return render(request, 'dashboard/form.html', {'form': form, 'title':'Create Furniture Item'})
@login_required

def furniture_edit(request, pk):
    obj = get_object_or_404(FurnitureItem, pk=pk)
    form = FurnitureItemForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST' and form.is_valid(): form.save(); return redirect('dashboard_furniture')
    return render(request, 'dashboard/form.html', {'form': form, 'title':'Edit Furniture Item'})

@login_required

def project_manage(request):
    return render(request, 'dashboard/list.html', {'title':'Portfolio Projects', 'objects': PortfolioProject.objects.all(), 'create_url':'dashboard_project_create', 'edit_name':'dashboard_project_edit'})
@login_required

def project_create(request):
    form = PortfolioProjectForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid(): form.save(); return redirect('dashboard_projects')
    return render(request, 'dashboard/form.html', {'form': form, 'title':'Create Portfolio Project'})
@login_required

def project_edit(request, pk):
    obj = get_object_or_404(PortfolioProject, pk=pk)
    form = PortfolioProjectForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST' and form.is_valid(): form.save(); return redirect('dashboard_projects')
    return render(request, 'dashboard/form.html', {'form': form, 'title':'Edit Portfolio Project'})
