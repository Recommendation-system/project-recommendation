from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='Author', verbose_name='Автор')
    theme = models.ForeignKey('Theme', on_delete=models.PROTECT, verbose_name='Тема')
    content = models.TextField(verbose_name='')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    likes = models.ManyToManyField(User, default=None, blank=True, related_name='likes')

    def total_likes(self):
        return self.likes.count();

    def __str__(self):
        return self.theme.name

    class Meta:
        verbose_name_plural = 'Записи'
        verbose_name = 'Запись'
        ordering = ['-published']


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


class Theme(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Тема')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Темы'
        verbose_name = 'Тема'
        ordering = ['name']
