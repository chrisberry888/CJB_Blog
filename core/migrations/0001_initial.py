# Generated for the local-only Chris Berry personal site MVP.
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BlogPost",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("slug", models.SlugField(max_length=160, unique=True)),
                ("source_format", models.CharField(choices=[("markdown", "Markdown"), ("latex", "LaTeX")], default="markdown", max_length=12)),
                ("source_body", models.TextField(blank=True)),
                ("rendered_html", models.TextField(blank=True)),
                ("published_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_published", models.BooleanField(db_index=True, default=False)),
                ("tags", models.CharField(blank=True, max_length=255)),
                ("body_markdown", models.TextField(blank=True)),
            ],
            options={
                "ordering": ["-published_at", "-created_at"],
            },
        ),
        migrations.CreateModel(
            name="HomePage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(default="Chris Berry", max_length=160)),
                ("profile_image", models.ImageField(blank=True, upload_to="profile/")),
                ("intro_markdown", models.TextField(blank=True, default="Welcome. This is a local-first personal site for writing, videos, photos, and links.")),
                ("source_format", models.CharField(choices=[("markdown", "Markdown"), ("latex", "LaTeX")], default="markdown", max_length=12)),
                ("source_body", models.TextField(blank=True)),
            ],
            options={
                "verbose_name": "Home page",
                "verbose_name_plural": "Home page",
            },
        ),
        migrations.CreateModel(
            name="LinkItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120)),
                ("url", models.URLField(max_length=500)),
                ("description", models.TextField(blank=True)),
                ("icon", models.ImageField(blank=True, upload_to="link_icons/")),
                ("display_order", models.PositiveIntegerField(db_index=True, default=0)),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                ("opens_in_new_tab", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["display_order", "title"],
            },
        ),
        migrations.CreateModel(
            name="NavigationItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(max_length=80)),
                ("url_name", models.CharField(blank=True, help_text="Internal Django route name, for example: blog_latest.", max_length=120)),
                ("external_url", models.URLField(blank=True, help_text="Use this instead of url_name for external destinations.", max_length=500)),
                ("display_order", models.PositiveIntegerField(db_index=True, default=0)),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                ("opens_in_new_tab", models.BooleanField(default=False)),
            ],
            options={
                "ordering": ["display_order", "label"],
            },
        ),
        migrations.CreateModel(
            name="PhotoPost",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("slug", models.SlugField(max_length=160, unique=True)),
                ("source_format", models.CharField(choices=[("markdown", "Markdown"), ("latex", "LaTeX")], default="markdown", max_length=12)),
                ("source_body", models.TextField(blank=True)),
                ("rendered_html", models.TextField(blank=True)),
                ("published_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_published", models.BooleanField(db_index=True, default=False)),
                ("tags", models.CharField(blank=True, max_length=255)),
                ("image", models.ImageField(upload_to="photos/")),
                ("caption_markdown", models.TextField(blank=True)),
            ],
            options={
                "ordering": ["-published_at", "-created_at"],
            },
        ),
        migrations.CreateModel(
            name="SiteSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("site_title", models.CharField(default="Chris Berry", max_length=120)),
                ("default_background_color", models.CharField(default="#2B213A", max_length=7)),
                ("default_text_color", models.CharField(default="#F6F0FF", max_length=7)),
                ("default_font_size", models.CharField(choices=[("small", "Small"), ("medium", "Medium"), ("large", "Large")], default="medium", max_length=12)),
            ],
            options={
                "verbose_name": "Site settings",
                "verbose_name_plural": "Site settings",
            },
        ),
        migrations.CreateModel(
            name="VideoPost",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("slug", models.SlugField(max_length=160, unique=True)),
                ("source_format", models.CharField(choices=[("markdown", "Markdown"), ("latex", "LaTeX")], default="markdown", max_length=12)),
                ("source_body", models.TextField(blank=True)),
                ("rendered_html", models.TextField(blank=True)),
                ("published_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_published", models.BooleanField(db_index=True, default=False)),
                ("tags", models.CharField(blank=True, max_length=255)),
                ("description_markdown", models.TextField(blank=True)),
                ("youtube_url", models.URLField(blank=True, max_length=500)),
                ("youtube_video_id", models.CharField(blank=True, max_length=32)),
                ("thumbnail", models.ImageField(blank=True, upload_to="video_thumbnails/")),
            ],
            options={
                "ordering": ["-published_at", "-created_at"],
            },
        ),
    ]

