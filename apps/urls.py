from django.urls import path, include
from apps.views import index_page, register_page, login_page, logout_page, blog_list_page, blog_detail_page

urlpatterns = [
    path('', index_page, name='index_page'),
    path('register', register_page, name='register_page'),
    path('login', login_page, name='login_page'),
    path('logout', logout_page, name='logout_page'),
    path('blog-list', blog_list_page, name='blog_list_page'),
    path('blog-detail/<int:pk>', blog_detail_page, name='blog_detail_page'),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
]
