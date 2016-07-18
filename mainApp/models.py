from django.db import models


class Categories(models.Model):
    name = models.CharField(verbose_name='Название категории', max_length=32, unique=True)
    desc = models.TextField(verbose_name='Описание категории', blank=True, null=True)


class Films(models.Model):
    category = models.ManyToManyField(Categories, verbose_name='Категории')
    name = models.CharField(verbose_name='Название фильма', max_length=64, unique=True)
    is_active = models.BooleanField(verbose_name='Активность', default=False)
    image = models.CharField(verbose_name='Обложка', max_length=64)
    preview = models.CharField(verbose_name='Превью', max_length=64, blank=True)
    desc = models.TextField(verbose_name='Описание', blank=True)