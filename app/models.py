from django.db import models
from ckeditor.fields import RichTextField


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        abstract = True


class Language(BaseModel):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Menu(BaseModel):
    start_time = models.TimeField()
    end_time = models.TimeField()

    phone = models.CharField(max_length=13)
    email = models.EmailField()
    address = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)

    language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name='menu')

    def __str__(self):
        return f'#{self.id} / {self.is_active} / {self.language}'

    class Meta:
        unique_together = ('language', )


class Country(BaseModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField()

    language = models.ForeignKey('Language', on_delete=models.PROTECT, related_name='countries')

    def __str__(self):
        return self.name


class TourType(BaseModel):
    type = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.type


class Tour(BaseModel):
    name = models.CharField(max_length=100)
    description = RichTextField()
    price = models.IntegerField()
    preview_image = models.ImageField(upload_to='tours/preview_images/', null=True)

    is_hot = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, null=True)

    language = models.ForeignKey('Language', on_delete=models.PROTECT, related_name='tours')
    country = models.ForeignKey('Country', on_delete=models.PROTECT, related_name='tours')
    type = models.ForeignKey('TourType', on_delete=models.PROTECT, related_name='tours')

    def __str__(self):
        return self.name


class TourEvent(BaseModel):
    name = models.CharField(max_length=100)
    description = RichTextField()

    language = models.ForeignKey('Language', on_delete=models.PROTECT, related_name='events')
    tour = models.ForeignKey('Tour', on_delete=models.PROTECT, related_name='events')

    def __str__(self):
        return self.name


class Gallery(BaseModel):
    TOURS = 'Tours'
    EXCURSIONS = 'Excursions'
    DESTINATIONS = 'Destinations'

    types = (
        ('Tours', 'Tours'),
        ('Excursions', 'Excursions'),
        ('Destinations', 'Destinations'),
    )

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=types, default=TOURS)
    image = models.ImageField(upload_to='gallery/', blank=True, null=True)

    country = models.ForeignKey('Country', on_delete=models.PROTECT, related_name='galleries')
    language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name='galleries')

    def __str__(self):
        return self.name


class BlogTag(BaseModel):
    name = models.CharField(max_length=40, unique=True)

    language = models.ForeignKey('Language', on_delete=models.PROTECT, related_name='blog_tags')

    def __str__(self):
        return self.name


class Blog(BaseModel):
    title = models.CharField(max_length=100)
    description = RichTextField()
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_popular = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True)

    tags = models.ForeignKey('BlogTag', on_delete=models.CASCADE, related_name='blogs', blank=True)
    language = models.ForeignKey('Language', on_delete=models.PROTECT, related_name='blogs')

    def __str__(self):
        return self.title


class About(BaseModel):
    description = RichTextField()

    image = models.ImageField(upload_to='about/', blank=True, null=True)
    award_count = models.CharField(max_length=3)
    tour_count = models.CharField(max_length=4)
    travel_count = models.IntegerField()
    team_member_count = models.CharField(max_length=5)

    is_active = models.BooleanField(default=False, unique=True)

    language = models.ForeignKey('Language', on_delete=models.PROTECT, related_name='abouts')

    def __str__(self):
        return 'about'


class Destination(BaseModel):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='destination/', blank=True, null=True)

    about = models.ForeignKey('About', on_delete=models.PROTECT, related_name='destinations')
    language = models.ForeignKey('Language', on_delete=models.PROTECT, related_name='destinations')

    def __str__(self):
        return self.name


class PeopleSay(BaseModel):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    comment = models.TextField()

    avatar = models.ImageField(upload_to='about/people/')

    language = models.ForeignKey('Language', on_delete=models.PROTECT, related_name='people_says')

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


# class Request(BaseModel):
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField()
#     phone_number = models.CharField(max_length=13)
#     arrival_date = models.DateTimeField()
#     departure_date = models.DateTimeField()
