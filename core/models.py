from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone

from .youtube import extract_youtube_video_id

SOURCE_FORMAT_CHOICES = [
    ("markdown", "Markdown"),
    ("latex", "LaTeX"),
]

FONT_SIZE_CHOICES = [
    ("small", "Small"),
    ("medium", "Medium"),
    ("large", "Large"),
]


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _created = cls.objects.get_or_create(pk=1)
        return obj


class SiteSettings(SingletonModel):
    site_title = models.CharField(max_length=120, default="Chris Berry")
    default_background_color = models.CharField(max_length=7, default="#2B213A")
    default_text_color = models.CharField(max_length=7, default="#F6F0FF")
    default_font_size = models.CharField(
        max_length=12,
        choices=FONT_SIZE_CHOICES,
        default="medium",
    )

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return self.site_title


class HomePage(SingletonModel):
    title = models.CharField(max_length=160, default="Chris Berry")
    profile_image = models.ImageField(upload_to="profile/", blank=True)
    intro_markdown = models.TextField(
        blank=True,
        default="Welcome. This is a local-first personal site for writing, videos, photos, and links.",
    )
    source_format = models.CharField(
        max_length=12,
        choices=SOURCE_FORMAT_CHOICES,
        default="markdown",
    )
    source_body = models.TextField(blank=True)

    class Meta:
        verbose_name = "Home page"
        verbose_name_plural = "Home page"

    def __str__(self):
        return self.title


class PublishedQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True, published_at__lte=timezone.now())


class PublishedManager(models.Manager):
    def get_queryset(self):
        return PublishedQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


class BaseContentModel(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=160, unique=True)
    source_format = models.CharField(
        max_length=12,
        choices=SOURCE_FORMAT_CHOICES,
        default="markdown",
    )
    source_body = models.TextField(blank=True)
    rendered_html = models.TextField(blank=True)
    published_at = models.DateTimeField(default=timezone.now, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False, db_index=True)
    tags = models.CharField(max_length=255, blank=True)

    objects = PublishedManager()

    class Meta:
        abstract = True
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title


class BlogPost(BaseContentModel):
    body_markdown = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse("blog_detail", kwargs={"slug": self.slug})


class VideoPost(BaseContentModel):
    description_markdown = models.TextField(blank=True)
    youtube_url = models.URLField(max_length=500, blank=True)
    youtube_video_id = models.CharField(max_length=32, blank=True)
    thumbnail = models.ImageField(upload_to="video_thumbnails/", blank=True)

    def save(self, *args, **kwargs):
        extracted_id = extract_youtube_video_id(self.youtube_url)
        if extracted_id:
            self.youtube_video_id = extracted_id
            update_fields = kwargs.get("update_fields")
            if update_fields is not None:
                kwargs["update_fields"] = set(update_fields) | {"youtube_video_id"}
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("video_detail", kwargs={"slug": self.slug})

    @property
    def embed_url(self):
        if not self.youtube_video_id:
            return ""
        return f"https://www.youtube.com/embed/{self.youtube_video_id}?feature=oembed"


class PhotoPost(BaseContentModel):
    image = models.ImageField(upload_to="photos/")
    caption_markdown = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse("photo_detail", kwargs={"slug": self.slug})


class LinkItem(models.Model):
    title = models.CharField(max_length=120)
    url = models.URLField(max_length=500)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to="link_icons/", blank=True)
    display_order = models.PositiveIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    opens_in_new_tab = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "title"]

    def __str__(self):
        return self.title


class NavigationItem(models.Model):
    label = models.CharField(max_length=80)
    url_name = models.CharField(
        max_length=120,
        blank=True,
        help_text="Internal Django route name, for example: blog_latest.",
    )
    external_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="Use this instead of url_name for external destinations.",
    )
    display_order = models.PositiveIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    opens_in_new_tab = models.BooleanField(default=False)

    class Meta:
        ordering = ["display_order", "label"]

    def clean(self):
        if self.url_name and self.external_url:
            raise ValidationError("Use either url_name or external_url, not both.")
        if not self.url_name and not self.external_url:
            raise ValidationError("Set either url_name or external_url.")

    def __str__(self):
        return self.label
