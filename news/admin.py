from django.contrib import admin
from .models import Post, PostCategory   #Доработайте ваш новостной портал.
# Во все объекты добавьте удобный вывод и фильтры


admin.site.register(Post)
admin.site.register(PostCategory)