from django.contrib import admin

from .models import (
    BlogPost,
    HomePage,
    LinkItem,
    NavigationItem,
    PhotoPost,
    SiteSettings,
    VideoPost,
)


class SingletonAdminMixin:
    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdminMixin, admin.ModelAdmin):
    list_display = ("site_title", "default_background_color", "default_text_color", "default_font_size")


@admin.register(HomePage)
class HomePageAdmin(SingletonAdminMixin, admin.ModelAdmin):
    list_display = ("title", "source_format")
    fieldsets = (
        (None, {"fields": ("title", "profile_image", "intro_markdown")}),
        ("Future source import", {"fields": ("source_format", "source_body")}),
    )


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "published_at", "is_published", "updated_at")
    list_filter = ("is_published", "published_at", "source_format")
    search_fields = ("title", "body_markdown", "tags")
    ordering = ("-published_at", "-created_at")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (None, {"fields": ("title", "slug", "body_markdown", "tags")}),
        ("Publishing", {"fields": ("is_published", "published_at")}),
        ("Future source import", {"fields": ("source_format", "source_body", "rendered_html")}),
    )


@admin.register(VideoPost)
class VideoPostAdmin(admin.ModelAdmin):
    list_display = ("title", "published_at", "is_published", "youtube_video_id", "updated_at")
    list_filter = ("is_published", "published_at", "source_format")
    search_fields = ("title", "description_markdown", "youtube_url", "tags")
    ordering = ("-published_at", "-created_at")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("youtube_video_id",)
    fieldsets = (
        (None, {"fields": ("title", "slug", "description_markdown", "tags")}),
        ("Video", {"fields": ("youtube_url", "youtube_video_id", "thumbnail")}),
        ("Publishing", {"fields": ("is_published", "published_at")}),
        ("Future source import", {"fields": ("source_format", "source_body", "rendered_html")}),
    )


@admin.register(PhotoPost)
class PhotoPostAdmin(admin.ModelAdmin):
    list_display = ("title", "published_at", "is_published", "updated_at")
    list_filter = ("is_published", "published_at", "source_format")
    search_fields = ("title", "caption_markdown", "tags")
    ordering = ("-published_at", "-created_at")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (None, {"fields": ("title", "slug", "image", "caption_markdown", "tags")}),
        ("Publishing", {"fields": ("is_published", "published_at")}),
        ("Future source import", {"fields": ("source_format", "source_body", "rendered_html")}),
    )


@admin.register(LinkItem)
class LinkItemAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "display_order", "is_active", "opens_in_new_tab", "updated_at")
    list_editable = ("display_order", "is_active", "opens_in_new_tab")
    list_filter = ("is_active", "opens_in_new_tab")
    search_fields = ("title", "url", "description")
    ordering = ("display_order", "title")


@admin.register(NavigationItem)
class NavigationItemAdmin(admin.ModelAdmin):
    list_display = ("label", "url_name", "external_url", "display_order", "is_active", "opens_in_new_tab")
    list_editable = ("display_order", "is_active", "opens_in_new_tab")
    list_filter = ("is_active", "opens_in_new_tab")
    search_fields = ("label", "url_name", "external_url")
    ordering = ("display_order", "label")

