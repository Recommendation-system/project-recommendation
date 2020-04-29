from django.contrib import admin

from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('theme', 'author', 'content', 'published')
    list_display_links = ('theme', 'content')
    search_fields = ('theme', 'content')


admin.site.register(Post, PostAdmin)
admin.site.register(Theme)
admin.site.register(Like)
