from django.contrib import admin

from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('subject', 'author', 'content', 'published')
    list_display_links = ('subject', 'content')
    search_fields = ('subject', 'content')


admin.site.register(Post, PostAdmin)
admin.site.register(Subject)
admin.site.register(Like)

