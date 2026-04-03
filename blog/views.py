from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CommentForm
from .models import BlogPost, Category
from core.remote_assets import BLOG_IMAGE_URLS, attach_image_url, attach_many


def blog_list(request):
    posts = BlogPost.objects.filter(published=True)
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(request.GET.get('page'))
    attach_many(page_obj.object_list, BLOG_IMAGE_URLS, 'featured_image')
    return render(request, 'blog/list.html', {'page_obj': page_obj, 'categories': Category.objects.all(), 'selected_category': category_slug})


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    attach_image_url(post, BLOG_IMAGE_URLS, 'featured_image')
    related_posts = list(BlogPost.objects.filter(category=post.category, published=True).exclude(pk=post.pk)[:3])
    attach_many(related_posts, BLOG_IMAGE_URLS, 'featured_image')
    form = CommentForm()
    return render(request, 'blog/detail.html', {'post': post, 'related_posts': related_posts, 'form': form})


def add_comment(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False); comment.post = post; comment.save()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'ok': True, 'name': comment.name, 'message': comment.message, 'created_at': comment.created_at.strftime('%d %b %Y')})
    return redirect(post.get_absolute_url())
