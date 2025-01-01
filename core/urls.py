from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name='index'),
    path('settings', views.settings, name='settings'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('upload', views.upload, name='upload'),
    path('single_post/<int:post_id>', views.single_post, name='single_post'),
    path('like', views.like, name='like'),
    path('save', views.save, name='save'),
    path('saved/<int:user_id>', views.saved, name='saved'),
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('follow_user', views.follow_user, name='follow_user'),
    path('unfollow_user', views.unfollow_user, name='unfollow_user'),
    path('edit/<int:post_id>', views.edit, name='edit'),
]