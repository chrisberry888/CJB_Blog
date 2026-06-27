# CJB_Blog

This repository is my attempt of creating a website entirely using ChatGPT/Codex. I am exploring the capabilities of LLMs, and seeing the breadth of what it is able to create and do for me.

Django personal content site for Chris Berry. It includes a home page, blog posts, video posts using YouTube embeds, photo posts, a link page, admin-editable navigation, browser-local theme controls, and Docker Compose support for homelab or EC2-style hosting.

## Stack

- Python
- Pipenv
- Django
- SQLite
- Docker / Docker Compose
- Gunicorn
- WhiteNoise
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

## Docker setup

The app can run in Docker with SQLite persisted in a named Docker volume. Uploaded media is also persisted in a named volume.

Create a local Docker environment file:

```bash
cp .env.example .env
```

Edit `.env` before running the container:

- Set `DJANGO_SECRET_KEY` to a long random value.
- Set `DJANGO_ALLOWED_HOSTS` to the hostnames or IP addresses you will use.
- Set `DJANGO_CSRF_TRUSTED_ORIGINS` to the full origins you will use, including `http://` or `https://` and any nonstandard port.
- Set `HOST_PORT` if you want to expose the site on a port other than `8000`.

You can generate a Django secret key locally with:

```bash
pipenv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Build a Docker image from the newest website changes:

```bash
docker compose build web
```

Start the container:

```bash
docker compose up -d
```

Watch logs:

```bash
docker compose logs -f web
```

Create an admin user inside the running container:

```bash
docker compose exec web python manage.py createsuperuser
```

Seed placeholder content, if needed:

```bash
docker compose exec web python manage.py seed_initial_data
```

Open the containerized site at:

- Site: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

To rebuild and restart after making code changes:

```bash
docker compose up -d --build
```

The `cjb_blog_data` and `cjb_blog_media` Docker volumes preserve the SQLite database and uploaded media across image rebuilds.

## Homelab docker-compose run

On the homelab machine:

1. Install Docker and Docker Compose.
2. Clone or copy this repository to the homelab.
3. Create `.env` from `.env.example`.
4. In `.env`, set `DJANGO_ALLOWED_HOSTS` to include the homelab IP address or domain.
5. In `.env`, set `DJANGO_CSRF_TRUSTED_ORIGINS` to include the exact browser URL, for example `http://192.168.1.50:8000`.
6. Run:

```bash
docker compose up -d --build
```

Then create the admin user:

```bash
docker compose exec web python manage.py createsuperuser
```

If you put the app behind a reverse proxy, update `.env` so `DJANGO_ALLOWED_HOSTS` includes the public hostname and `DJANGO_CSRF_TRUSTED_ORIGINS` includes the public `https://...` origin.

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

- The Docker setup is suitable for a small homelab or EC2 MVP. It is not a complete high-availability production architecture.
- `DJANGO_SERVE_MEDIA=True` lets Django serve uploaded media from the container for simplicity. For heavier traffic, serve `/media/` from a reverse proxy pointed at the mounted media volume.
- Version 1 video posts use YouTube embeds. Self-hosted playback is not implemented yet.
- LaTeX support is not implemented yet. The models include minimal `source_format`, `source_body`, and `rendered_html` fields so a later import/conversion path can be added cleanly.
- The seed command does not create a placeholder photo post because `PhotoPost.image` requires an uploaded image. The photo pages handle the empty state.
