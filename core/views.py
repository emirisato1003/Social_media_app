import json
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from .models import User, Profile, Post, Category, Like, Save, Follow

# Create your views here.
@login_required(login_url='login')
def index(request):
    all_post = Post.objects.select_related('user').all()

    return render(request, 'index.html',{
        'all_post': all_post,
    })

def single_post(request, post_id):
    all_category = Category.objects.all()
    post = Post.objects.get(id=post_id)
    all_likes = Like.objects.all()
    user = request.user.id
    user_liked = []
    all_posts = Post.objects.all()
    try:
        for like in all_likes:
            if not user in user_liked:
                if like.user.id == user:
                    user_liked.append(like.post.id)
    except:
        user_liked = []

    all_saves = Save.objects.all()
    user_saved = []
    try:
        for save in all_saves:
            if not user in user_saved:
                if save.user.id == user:
                    user_saved.append(save.post.id)
    except:
        user_saved = []

    return render(request, 'single_post.html', {
        'post': post,
        'user_liked': user_liked,
        'user_saved': user_saved,
        'all_posts': all_posts,
        'all_category':all_category,
        })

def edit(request, post_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        edit_post = Post.objects.get(pk=post_id)
        edit_post.title = data['title']
        edit_post.caption = data['caption']
        # category_id = int(data['category'])
        # category_selected = Category.objects.get(pk=category_id)
        # edit_post.category = category_selected
        edit_post.save()
        return JsonResponse({"message": "Change successful", "data": data})
    else:
        return JsonResponse({'error': 'POST request required'}, status=400)


@login_required(login_url='login')
def profile(request, user_id):
    current_user = User.objects.get(pk=request.user.id)
    user = User.objects.get(pk=user_id)
    user_profile = Profile.objects.filter(user=user).first()
    user_posts = Post.objects.filter(user=user_id)
    user_liked = []
    try:
        for like in all_likes:
            if not user in user_liked:
                if like.user.id == user:
                    user_liked.append(like.post.id)
    except:
        user_liked = []

    following = Follow.objects.filter(user_following=user)
    follower = Follow.objects.filter(follower=user)
    try:
        # Check if a follow relationship exists for the current user
        isFollowing = follower.filter(user_following=current_user).exists()                
    except User.DoesNotExist:
        # if the user doesn't exist, they can't be following
        isFollowing = False        
    return render(request, 'profile.html', {
        'user': user,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_liked': user_liked,
        'isFollowing': isFollowing,
        'following': following,
        'follower': follower
    })

def follow_user(request):
    following_user = request.POST['following']
    current_user = User.objects.get(pk=request.user.id)
    following = User.objects.get(username=following_user)
    f = Follow.objects.create(user_following=current_user, follower=following)
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': following.id}))

def unfollow_user(request):
    unfollowing_user = request.POST['unfollowing']
    current_user = User.objects.get(pk=request.user.id)
    unfollowing = User.objects.get(username=unfollowing_user)
    f = Follow.objects.filter(user_following=current_user, follower=unfollowing).delete()
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': unfollowing.id}))

@login_required(login_url='login')
def like(request):
    post_id = request.GET.get('post_id')
    post = Post.objects.get(pk=post_id)
    user = request.user

    like_filter = Like.objects.filter(post=post, user=user).first()

    if like_filter is None:
        new_like = Like.objects.create(user=user, post=post)
        like_count = post.post_like.count()
        new_like.save()
        return JsonResponse({'like_count': like_count, 'like_status': True })
    else:
        like_filter.delete()
        like_count = post.post_like.count()
        return JsonResponse({'like_count': like_count, 'like_status': False})

@login_required(login_url='login')
def save(request):
    # get the current user from the request
    user = request.user
    # get the post id from the GET parameters
    post_id = request.GET.get('post_id')
    # retrieve the Post object with the given post id
    post = Post.objects.get(pk=post_id)

    # check if (filter) the post is already saved by the user
    save_filter = Save.objects.filter(user=user, post=post).first()
    # If the post is not saved, create a new Save object
    if save_filter is None:
        new_save = Save.objects.create(user=user, post=post)
        new_save.save()
        messages.success(request, 'Successfully saved a photo')
        # redirect to the detail view of the post
        return redirect('single_post', post_id=post_id)
    else:
        # if the post is already saved, delete the Save object
        save_filter.delete()
        messages.info(request, 'Removed a photo form save')
        # redirect to the detail view of the post
        return redirect('single_post', post_id=post_id)
    
def saved(request, user_id):
    user = User.objects.get(pk=user_id)
    posts = Save.objects.filter(user=user)
    return render(request, 'saved.html',{
        'user': user,
        'posts': posts
    })

@login_required(login_url='login')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        image = request.FILES.get('image', user_profile.profile_img)
        b_image = request.FILES.get('b-image', user_profile.background_img)

        bio = request.POST.get('bio', user_profile.bio)
        location = request.POST.get('location', user_profile.location)

        user_profile.profile_img = image
        user_profile.background_img = b_image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()
        return redirect('settings')
    # print(user_profile.bio)
    return render(request, 'setting.html', {'user_profile': user_profile})

@login_required(login_url='login')
def upload(request):
    if request.method == "GET":
        all_category = Category.objects.all()
        return render(request, "upload.html",{
        "all_category": all_category
    })
    if request.method == "POST":
        file = request.FILES["img_file"]
        title = request.POST["title"]
        caption = request.POST["caption"]
        category_select = request.POST.get("category_select")
        category_input = request.POST.get("category_input")
        current_user = request.user        
        if category_input:
            new_category = Category(category_name=category_input)
            new_category.save()
            new_post = Post(
            image=file,
            title=title,
            caption=caption,
            user=current_user,
            category=new_category
            )
            new_post.save()
        elif category_select:
            try:
                category_id = int(category_select)
                new_category = Category.objects.get(id=category_id)
                new_post = Post(
                    image=file,
                    title=title,
                    caption=caption,
                    user=current_user,
                    category=new_category
                    )
                new_post.save()
                # select_category.save()
            except ValueError:
                pass
        
        messages.success(request, 'Your post has been created successfully!')
        # redirect the index page
        return HttpResponseRedirect(reverse("index"))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, 'login.html', {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, 'login.html')

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

            #log user in and redirect to settings page
            user_login = authenticate(request, username=username, password=password)
            login(request, user_login)

            #create a Profile object for the new user
            user_model = User.objects.get(username=username)
            new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
            new_profile.save()
            return redirect('settings')

        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")