from types import SimpleNamespace

from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import OperationalError, ProgrammingError
from django.urls import NoReverseMatch, reverse

from .models import HomePage, NavigationItem, SiteSettings


DEFAULT_SITE_SETTINGS = SimpleNamespace(
    site_title="Chris Berry",
    default_background_color="#2B213A",
    default_text_color="#F6F0FF",
    default_font_size="medium",
)


def _resolved_navigation_items():
    items = []
    for item in NavigationItem.objects.filter(is_active=True).order_by("display_order", "label"):
        url = item.external_url
        if item.url_name:
            try:
                url = reverse(item.url_name)
            except NoReverseMatch:
                continue
        if not url:
            continue
        items.append(
            {
                "label": item.label,
                "url": url,
                "opens_in_new_tab": item.opens_in_new_tab,
            }
        )
    return items


def site_context(_request):
    try:
        site_settings = SiteSettings.load()
        home_page = HomePage.objects.filter(pk=1).first()
        navigation_items = _resolved_navigation_items()
    except (OperationalError, ProgrammingError, ObjectDoesNotExist):
        site_settings = DEFAULT_SITE_SETTINGS
        home_page = None
        navigation_items = []

    return {
        "site_settings": site_settings,
        "navigation_items": navigation_items,
        "drawer_profile_image_url": home_page.profile_image.url if home_page and home_page.profile_image else "",
    }

