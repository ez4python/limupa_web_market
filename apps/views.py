from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from apps.forms import CustomUserCreationForm
from apps.models import Blog, Category


def index_page(request):
    return render(request, 'apps/index.html')


def blog_list_page(request):
    context = {
        'blogs': Blog.objects.all().order_by('-created_at')
    }
    return render(request, 'apps/blogs/blog-list.html', context)


def blog_detail_page(request, pk):
    blog = Blog.objects.filter(pk=pk).first()
    context = {
        'blog': blog,
        'comments': blog.comment_set.all(),
        'tags': blog.tags.all(),
        'categories': Category.objects.all()
    }
    return render(request, 'apps/blogs/blog-detail.html', context)


def logout_page(request):
    logout(request)
    return redirect('index_page')


def register_page(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.', extra_tags='register')
            return redirect('login_page')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}', extra_tags='register')
    context = {'form': form}
    return render(request, 'apps/login-register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('index_page')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.', extra_tags='login')
            return redirect('index_page')

        messages.error(request, 'Invalid username or password. Please try again.', extra_tags='login')

    return render(request, 'apps/login-register.html')
