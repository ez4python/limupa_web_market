from collections import defaultdict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView

from apps.forms import RegisterForm, EmailForm
from apps.mixins import NotLoginRequiredMixin
from apps.models import Blog, Category, Product, Tag, User


class IndexView(TemplateView):
    template_name = 'apps/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ShopListView(ListView):
    template_name = 'apps/shopping/shop-list.html'
    queryset = Product.objects.all()
    context_object_name = 'products'


class SingleProductView(DetailView):
    template_name = 'apps/shopping/single-product.html'
    queryset = Product.objects.all()
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BlogListView(ListView):
    template_name = 'apps/blogs/blog-list.html'
    paginate_by = 2
    queryset = Blog.objects.order_by('-id')
    context_object_name = 'blogs'

    def get_queryset(self):
        queryset = super().get_queryset()
        if search := self.request.GET.get('search'):
            return queryset.filter(name__icontains=search)
        return queryset


class BlogDetailView(DetailView):
    queryset = Blog.objects.order_by('-created_at')
    template_name = 'apps/blogs/blog-detail.html'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['recent_blogs'] = self.get_queryset()[:3]
        context['tags'] = Tag.objects.all()
        return context


class CustomLoginView(NotLoginRequiredMixin, LoginView):
    template_name = 'apps/login-register.html'
    next_page = 'index_page'


class RegisterFormView(FormView):
    template_name = 'apps/login-register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login_page')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class SignUpToNewsView(CreateView):
    template_name = 'apps/base.html'
    form_class = EmailForm
    success_url = reverse_lazy('.')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect('.', {'form': form})


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = 'apps/profile/profile_page.html'
    model = User
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('profile_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
