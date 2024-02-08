from django.urls import path

from app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tours/', views.tours, name='tours'),
    path('tours/<slug>', views.tour_detail, name='tour_detail'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('blogs/', views.blog, name='blog'),
    path('blogs/<slug>', views.blog_detail, name='blog_detail'),
    path('contact/', views.contact_us, name='contact_us'),
    path('privacy/', views.privacy, name='privacy'),
    path('countries/', views.countries, name='countries'),
    path('countries/<slug>', views.country_detail, name='country_detail'),
]
