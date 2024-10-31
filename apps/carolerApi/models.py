from django.db import models
from apps.core.models import DeleteLogic
from django.core.exceptions import ValidationError


# Create your models here.


class Category(DeleteLogic):
    title = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.title

    def clean(self):
        category = Category.objects.all()
        if self.title in category.title:
            raise ValidationError("Category already exists")

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        indexes = [models.Index(fields=['title'])]


class Music(DeleteLogic):
    url_detail_page = models.CharField(max_length=250)
    actor_name = models.CharField(max_length=100)
    title_album = models.CharField(max_length=100, null=True, blank=True)
    music_category = models.ManyToManyField('Category', related_name='category', related_query_name='categories')
    link_downloads_128 = models.URLField(max_length=250, blank=True, null=True)
    link_downloads_300 = models.URLField(max_length=250, blank=True, null=True)
    title_music = models.CharField(max_length=250)
    url_picture = models.URLField(max_length=250, blank=True, null=True)
    time_music = models.DateTimeField(auto_now_add=True)

    def clean(self):
        url = Music.objects.archive().all()
        if self.url_detail_page in url.url_detail_page:
            raise ValidationError("Url already exists")

    def __str__(self):
        return f'actor: {self.actor_name} // music: {self.title_music}'

    class Meta:
        verbose_name_plural = 'Musics'
        verbose_name = 'music'
        indexes = [models.Index(fields=['title_music', 'actor_name'])]
