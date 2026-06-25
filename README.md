# CJB_Blog

This repository is my attempt of creating a website entirely using ChatGPT/Codex. I am exploring the capabilities of LLMs, and seeing the breadth of what it is able to create and do for me.

Local-only Django personal content site for Chris Berry. It includes a home page, blog posts, video posts using YouTube embeds, photo posts, a link page, admin-editable navigation, and browser-local theme controls.

## Stack

- Python
- Pipenv
- Django
- SQLite
- Django templates
- Plain CSS
- Vanilla JavaScript
- Markdown rendering with sanitized HTML
- Pillow-backed image uploads

## Local setup

Install Pipenv if it is not already available:

```bash
python3 -m pip install --user pipenv
```

Install dependencies with Pipenv:

```bash
pipenv install
```

Run migrations:

```bash
pipenv run python manage.py migrate
```

Create an admin user:

```bash
pipenv run python manage.py createsuperuser
```

Seed placeholder local content:

```bash
pipenv run python manage.py seed_initial_data
```

Run the development server:

```bash
pipenv run python manage.py runserver
```

Open the site at:

- Site: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Content management

Use the Django admin to manage:

- `HomePage`: title, profile image, and intro Markdown.
- `BlogPost`: Markdown blog posts with editable slugs and publish status.
- `VideoPost`: YouTube URL, description Markdown, thumbnail, and publish status.
- `PhotoPost`: uploaded image, caption Markdown, and publish status.
- `LinkItem`: linktree-style links with ordering and active status.
- `NavigationItem`: drawer menu items. Use `url_name` for internal Django routes or `external_url` for outside links.
- `SiteSettings`: default site title, background color, text color, and default font size.

Visitor theme preferences are saved in that visitor's browser with `localStorage`. They override `SiteSettings` only in that browser.

## Notes

- This is intentionally local-development only. It does not include production deployment, Docker, AWS, EC2, or homelab configuration.
- Version 1 video posts use YouTube embeds. Self-hosted playback is not implemented yet.
- LaTeX support is not implemented yet. The models include minimal `source_format`, `source_body`, and `rendered_html` fields so a later import/conversion path can be added cleanly.
- The seed command does not create a placeholder photo post because `PhotoPost.image` requires an uploaded image. The photo pages handle the empty state.
