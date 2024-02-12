from django.shortcuts import render, redirect
from app.models import Tour, Blog, Gallery, BlogTag, PeopleSay, About, Menu, Country, Payment
import requests as axios
import json


# Create your views here.


def home(request):
    hot_tours = Tour.objects.filter(is_hot=True, language__name=request.LANGUAGE_CODE).order_by('-created_at')[:3]
    latest_blogs = Blog.objects.filter(language__name=request.LANGUAGE_CODE).order_by('-created_at').all()[:6]
    galleries = Gallery.objects.filter(language__name=request.LANGUAGE_CODE).order_by('-created_at').all()[:6]
    people_says = PeopleSay.objects.filter(language__name=request.LANGUAGE_CODE)[:3]

    return render(request, 'index.html', {
        'hot_tours': hot_tours,
        'latest_blogs': latest_blogs,
        'galleries': galleries,
        'people_says': people_says,
    })


def about(request):
    about_data = About.objects.prefetch_related('destinations').filter(is_active=True,
                                                                       language__name=request.LANGUAGE_CODE).first()
    destinations = about_data.destinations.all()
    people_says = PeopleSay.objects.filter(language__name=request.LANGUAGE_CODE)

    return render(request, 'about.html', {
        'about_data': about_data,
        'destinations': destinations,
        'people_says': people_says,
    })


def contact_us(request):
    about_data = About.objects.filter(is_active=True, language__name=request.LANGUAGE_CODE).first()
    menu = Menu.objects.filter(is_active=True, language__name=request.LANGUAGE_CODE).first()

    return render(request, 'contact-us.html', {
        'about_data': about_data,
        "menu": menu
    })


def tours(request):
    all_tours = Tour.objects.select_related('country', 'type').filter(language__name=request.LANGUAGE_CODE)

    return render(request, 'our-tours.html', {
        'all_tours': all_tours,
    })


def tour_detail(request, slug):
    tour = (Tour.objects.select_related('country', 'type').prefetch_related('events')
            .get(slug=slug, language__name=request.LANGUAGE_CODE))

    events = tour.events.all()

    prev_tour = (Tour.objects.select_related('country', 'type')
                 .filter(id__lt=tour.id, language__name=request.LANGUAGE_CODE).first())
    next_tour = (Tour.objects.select_related('country', 'type')
                 .filter(id__gt=tour.id, language__name=request.LANGUAGE_CODE).first())

    return render(request, 'single-tour.html', {
        'tour': tour,
        'prev_tour': prev_tour,
        'next_tour': next_tour,
        'events': events,
    })


def gallery(request):
    galleries = Gallery.objects.select_related('country').filter(language__name=request.LANGUAGE_CODE)

    return render(request, 'grid-gallery.html', {
        'galleries': galleries,
    })


def blog(request):
    tag = request.GET.get('tag')

    tags = BlogTag.objects.filter(language__name=request.LANGUAGE_CODE)

    if tag:
        blogs = (Blog.objects.select_related('tags')
                 .filter(tags__name__icontains=tag, language__name=request.LANGUAGE_CODE).order_by('-created_at'))

        return render(request, 'classic-blog.html', {
            'blogs': blogs,
            'tags': tags,
            'current_tag': tag,
        })

    blogs = Blog.objects.select_related('tags').filter(language__name=request.LANGUAGE_CODE).order_by('-created_at')

    return render(request, 'classic-blog.html', {
        'blogs': blogs,
        'tags': tags,
        'current_tag': tag,
    })


def blog_detail(request, slug):
    bl = Blog.objects.select_related('tags').get(slug=slug, language__name=request.LANGUAGE_CODE)

    popular_blogs = Blog.objects.order_by('-created_at').filter(language__name=request.LANGUAGE_CODE)[:2]

    tags = BlogTag.objects.filter(language__name=request.LANGUAGE_CODE)

    return render(request, 'blog-post.html', {
        'blog': bl,
        'popular_blogs': popular_blogs,
        'tags': tags
    })


def page_not_found(request, exception):
    return render(request, '404.html', {})


def privacy(request):
    return render(request, 'privacy-policy.html', {})


def countries(request):
    ct = Country.objects.filter(language__name=request.LANGUAGE_CODE)

    return render(request, 'countries.html', {
        'countries': ct
    })


def country_detail(request, slug):
    ct = Country.objects.prefetch_related('tours').get(slug=slug, language__name=request.LANGUAGE_CODE)
    trs = Tour.objects.select_related('type').filter(language__name=request.LANGUAGE_CODE, country=ct)

    return render(request, 'country_detail.html', {
        'country': ct,
        'tours': trs,
    })


def payment(request):
    country = request.GET.get('country')
    error = request.GET.get('error', False)

    all_countries = Country.objects.filter(language__name=request.LANGUAGE_CODE)
    popular_blogs = Blog.objects.order_by('-created_at').filter(language__name=request.LANGUAGE_CODE)[:2]

    return render(request, 'payment.html', {
        'popular_blogs': popular_blogs,
        'all_countries': all_countries,
        'country': country,
        'error': error,
    })


def create_payment(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        price = request.POST.get('price')
        country = request.POST.get('country')
        comment = request.POST.get('comment')

        payment_is_created = Payment.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            price=price,
            country=country,
            comment=comment,
        )

        country = Country.objects.get(slug=country)

        auth = dict(email="maruf.tairov@gmail.com", password="2Gv!G5RpdmQccB5")

        data = axios.post('https://api.mel.store/api/mel-store/auth/login', json=auth)

        booking_data = {
            "thumbnail_type": "button",
            "button_title": "Check offer",
            "has_promo_codes": False,
            "prices": [
                {
                    "is_discount_price": False,
                    "price": payment_is_created.price,
                    "currency_id": 2
                }
            ],
            "product_title": country.name,
            "product_description": f'{country.description[:50]}...',
        }

        book = axios.patch('https://api.mel.store/api/mel-store/products/85791',
                           json=booking_data,
                           headers={'Authorization': f'Bearer {data.json().get("access_token")}'})

        if book.status_code == 200:
            return redirect('https://mel.store/odamlar.tv/85791')

        return redirect('payment?error=true')

    return redirect('payment')
