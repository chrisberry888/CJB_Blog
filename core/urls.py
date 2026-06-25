from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("blog/", views.blog_latest, name="blog_latest"),
    path("blog/archive/", views.blog_archive, name="blog_archive"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("videos/", views.video_latest, name="video_latest"),
    path("videos/archive/", views.video_archive, name="video_archive"),
    path("videos/<slug:slug>/", views.video_detail, name="video_detail"),
    path("photos/", views.photo_latest, name="photo_latest"),
    path("photos/archive/", views.photo_archive, name="photo_archive"),
    path("photos/<slug:slug>/", views.photo_detail, name="photo_detail"),
    path("links/", views.links, name="links"),
]

