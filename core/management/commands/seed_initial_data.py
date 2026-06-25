from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import BlogPost, HomePage, LinkItem, NavigationItem, SiteSettings, VideoPost


class Command(BaseCommand):
    help = "Create local placeholder content and default navigation."

    def handle(self, *args, **options):
        SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                "site_title": "Chris Berry",
                "default_background_color": "#2B213A",
                "default_text_color": "#F6F0FF",
                "default_font_size": "medium",
            },
        )

        HomePage.objects.get_or_create(
            pk=1,
            defaults={
                "title": "Chris Berry",
                "intro_markdown": (
                    "This is a local-first personal site for writing, videos, photos, and links. "
                    "Edit this introduction from the Django admin."
                ),
            },
        )

        nav_items = [
            ("Home", "home", 10),
            ("Blog", "blog_latest", 20),
            ("Videos", "video_latest", 30),
            ("Photos", "photo_latest", 40),
            ("Links", "links", 50),
        ]
        for label, url_name, order in nav_items:
            NavigationItem.objects.update_or_create(
                url_name=url_name,
                defaults={
                    "label": label,
                    "external_url": "",
                    "display_order": order,
                    "is_active": True,
                    "opens_in_new_tab": False,
                },
            )

        blog_body = (
            "## Welcome\n\n"
            "This placeholder post confirms the blog is wired up. Replace it with a real post "
            "from the Django admin when you are ready.\n\n"
            "- Markdown rendering is enabled.\n"
            "- Slugs are editable in admin.\n"
            "- LaTeX support is intentionally future-proofed, not implemented yet."
        )
        BlogPost.objects.update_or_create(
            slug="welcome-to-cjb-blog",
            defaults={
                "title": "Welcome to CJB Blog",
                "body_markdown": blog_body,
                "source_body": blog_body,
                "published_at": timezone.now(),
                "is_published": True,
                "tags": "placeholder, local",
            },
        )

        video_description = (
            "This is a placeholder YouTube embed for local development. "
            "Replace the URL and description from the Django admin."
        )
        VideoPost.objects.update_or_create(
            slug="placeholder-video",
            defaults={
                "title": "Placeholder Video",
                "description_markdown": video_description,
                "source_body": video_description,
                "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "published_at": timezone.now(),
                "is_published": True,
                "tags": "placeholder, video",
            },
        )

        links = [
            ("GitHub", "https://github.com/", "A placeholder profile link.", 10),
            ("YouTube", "https://www.youtube.com/", "A placeholder video channel link.", 20),
            ("Contact", "https://example.com/contact", "Replace this with a real contact link.", 30),
        ]
        for title, url, description, order in links:
            LinkItem.objects.update_or_create(
                title=title,
                defaults={
                    "url": url,
                    "description": description,
                    "display_order": order,
                    "is_active": True,
                    "opens_in_new_tab": True,
                },
            )

        self.stdout.write(self.style.SUCCESS("Seeded default site settings, home page, navigation, blog, video, and links."))
        self.stdout.write("Photo posts require an uploaded image, so the seeded photo page intentionally shows its empty state.")
