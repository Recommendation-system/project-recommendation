from time import time

from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils.text import slugify


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, verbose_name='Пользователь')
    avatar = models.ImageField(upload_to='avatars/', default="avatars/default.jpg", null=True,
                               blank=True, verbose_name='Аватар')
    registration_date = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Зарегестрирован')
    course_number = models.IntegerField(default=1, verbose_name="Курс")

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.avatar.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)

    class Meta:
        verbose_name_plural = 'Профили'
        verbose_name = 'Профиль'
        ordering = ['user']


class Post(models.Model):
    slug = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Автор')
    title = models.TextField(max_length=50, verbose_name="Название")
    theme = models.ForeignKey('Theme', on_delete=models.PROTECT, verbose_name='Тема')
    content = models.TextField(verbose_name='Тело')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    likes = models.ManyToManyField(User, default=None, blank=True, related_name='likes')

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'post_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            new_slug = slugify(self.title, allow_unicode=True)
            new_slug += '-' + (str(int(time())))
            self.slug = new_slug

        super().save(*args, **kwargs)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.theme.name

    class Meta:
        verbose_name_plural = 'Посты'
        verbose_name = 'Пост'
        ordering = ['-published']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.user, self.post)


class Theme(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Тема')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Темы'
        verbose_name = 'Тема'
        ordering = ['name']


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)

    def __str__(self):
        return str(self.post)
