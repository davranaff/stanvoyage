from django.shortcuts import render

from app.models import Tour, Blog, Gallery, BlogTag, PeopleSay, About, Menu, Country


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

    about_data = About.objects.prefetch_related('destinations').filter(is_active=True).first()
    destinations = about_data.destinations.all()
    people_says = PeopleSay.objects.all()

    return render(request, 'about.html', {
        'about_data': about_data,
        'destinations': destinations,
        'people_says': people_says,
    })


def contact_us(request):

    about_data = About.objects.filter(is_active=True).first()
    menu = Menu.objects.filter(is_active=True).first()

    return render(request, 'contact-us.html', {
        'about_data': about_data,
        "menu": menu
    })


def tours(request):

    all_tours = Tour.objects.select_related('country', 'type').all()

    return render(request, 'our-tours.html', {
        'all_tours': all_tours,
    })


def tour_detail(request, slug):

    tour = Tour.objects.select_related('country', 'type').prefetch_related('events').get(slug=slug)

    events = tour.events.all()

    prev_tour = Tour.objects.select_related('country', 'type').filter(id__lt=tour.id).first()
    next_tour = Tour.objects.select_related('country', 'type').filter(id__gt=tour.id).first()

    return render(request, 'single-tour.html', {
        'tour': tour,
        'prev_tour': prev_tour,
        'next_tour': next_tour,
        'events': events,
    })


def gallery(request):

    galleries = Gallery.objects.select_related('country').all()

    return render(request, 'grid-gallery.html', {
        'galleries': galleries,
    })


def blog(request):
    tag = request.GET.get('tag')

    tags = BlogTag.objects.all()

    if tag:

        blogs = Blog.objects.select_related('tags').filter(tags__name__icontains=tag).order_by('-created_at')

        return render(request, 'classic-blog.html', {
            'blogs': blogs,
            'tags': tags,
            'current_tag': tag,
        })

    blogs = Blog.objects.select_related('tags').order_by('-created_at')

    return render(request, 'classic-blog.html', {
        'blogs': blogs,
        'tags': tags,
        'current_tag': tag,
    })


def blog_detail(request, slug):

    bl = Blog.objects.select_related('tags').get(slug=slug)

    popular_blogs = Blog.objects.order_by('-created_at').all()[:2]

    tags = BlogTag.objects.all()

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

    ct = Country.objects.all()

    return render(request, 'countries.html', {
        'countries': ct
    })


def country_detail(request, slug):

    ct = Country.objects.prefetch_related('tours').get(slug=slug)
    trs = Tour.objects.select_related('type').all()

    return render(request, 'country_detail.html', {
        'country': ct,
        'tours': trs,
    })

