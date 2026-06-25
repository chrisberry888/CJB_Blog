from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .markdown_utils import render_markdown_safe
from .models import BlogPost, HomePage, LinkItem, PhotoPost, VideoPost

PAGE_SIZE = 8


def home(request):
    home_page = HomePage.load()
    return render(
        request,
        "core/home.html",
        {
            "page_title": home_page.title,
            "home_page": home_page,
            "intro_html": render_markdown_safe(home_page.intro_markdown),
        },
    )


def _paginate(request, queryset, per_page=PAGE_SIZE):
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(request.GET.get("page"))


def blog_latest(request):
    post = BlogPost.objects.published().first()
    return render(
        request,
        "core/blog_detail.html",
        {
            "page_title": "Blog",
            "post": post,
            "body_html": render_markdown_safe(post.body_markdown) if post else "",
            "is_latest": True,
        },
    )


def blog_archive(request):
    page_obj = _paginate(request, BlogPost.objects.published())
    return render(
        request,
        "core/blog_archive.html",
        {
            "page_title": "Blog Archive",
            "page_obj": page_obj,
        },
    )


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost.objects.published(), slug=slug)
    return render(
        request,
        "core/blog_detail.html",
        {
            "page_title": post.title,
            "post": post,
            "body_html": render_markdown_safe(post.body_markdown),
            "is_latest": False,
        },
    )


def video_latest(request):
    video = VideoPost.objects.published().first()
    return render(
        request,
        "core/video_detail.html",
        {
            "page_title": "Videos",
            "video": video,
            "description_html": render_markdown_safe(video.description_markdown) if video else "",
            "is_latest": True,
        },
    )


def video_archive(request):
    page_obj = _paginate(request, VideoPost.objects.published())
    return render(
        request,
        "core/video_archive.html",
        {
            "page_title": "Video Archive",
            "page_obj": page_obj,
        },
    )


def video_detail(request, slug):
    video = get_object_or_404(VideoPost.objects.published(), slug=slug)
    return render(
        request,
        "core/video_detail.html",
        {
            "page_title": video.title,
            "video": video,
            "description_html": render_markdown_safe(video.description_markdown),
            "is_latest": False,
        },
    )


def photo_latest(request):
    photo = PhotoPost.objects.published().first()
    return render(
        request,
        "core/photo_detail.html",
        {
            "page_title": "Photos",
            "photo": photo,
            "caption_html": render_markdown_safe(photo.caption_markdown) if photo else "",
            "is_latest": True,
        },
    )


def photo_archive(request):
    page_obj = _paginate(request, PhotoPost.objects.published())
    return render(
        request,
        "core/photo_archive.html",
        {
            "page_title": "Photo Archive",
            "page_obj": page_obj,
        },
    )


def photo_detail(request, slug):
    photo = get_object_or_404(PhotoPost.objects.published(), slug=slug)
    return render(
        request,
        "core/photo_detail.html",
        {
            "page_title": photo.title,
            "photo": photo,
            "caption_html": render_markdown_safe(photo.caption_markdown),
            "is_latest": False,
        },
    )


def links(request):
    link_items = LinkItem.objects.filter(is_active=True).order_by("display_order", "title")
    return render(
        request,
        "core/links.html",
        {
            "page_title": "Links",
            "link_items": link_items,
        },
    )

