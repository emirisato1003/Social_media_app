from django.contrib import admin
from .models import Profile, Post, Category, Like, Save, Follow

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'date_posted']

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Like)
admin.site.register(Save)
admin.site.register(Follow)