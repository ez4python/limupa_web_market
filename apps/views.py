from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, FormView

from apps.forms import RegisterForm
from apps.mixins import NotLoginRequiredMixin
from apps.models import Blog, Category


class IndexView(TemplateView):
    template_name = 'apps/index.html'


class BlogListView(ListView):
    template_name = 'apps/blogs/blog-list.html'
    queryset = Blog.objects.order_by('-created_at')
    context_object_name = 'blogs'


class BlogDetailView(DetailView):
    queryset = Blog.objects.all()
    template_name = 'apps/blogs/blog-detail.html'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CustomLoginView(NotLoginRequiredMixin, LoginView):
    template_name = 'apps/login-register.html'
    success_url = reverse_lazy('index_page')


class RegisterFormView(FormView):
    template_name = 'apps/login-register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('register_page')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
