from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_profile")
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profile_img = models.ImageField(upload_to='profile_images', default='default_profile_img.png')
    background_img = models.ImageField(upload_to='background_images', default='default_background_img.jpg')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

class Category(models.Model):
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return self.category_name

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_post")
    title = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField(max_length=1000, blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_post")

    def __str__(self):
        return f'{self.user.username} Post'
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name='post_like')
    is_like = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} like {self.post.title}"

class Save(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user_save')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name='post_save')
    is_save = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} save {self.post.title}"

class Follow(models.Model):
    user_following = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='following')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='follower')

    def __str__(self):
        return f"{self.user_following} follow {self.follower}"