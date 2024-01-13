from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CharField, ForeignKey, CASCADE, ManyToManyField, DateTimeField, ImageField, \
    PositiveIntegerField, FloatField
from django_ckeditor_5.fields import CKEditor5Field


class User(AbstractUser):
    image = ImageField(upload_to='users/images', default='users/default.jpg')


class Product(Model):
    title = CharField(max_length=255)
    description = CKEditor5Field(blank=True, null=True)
    image = ImageField(upload_to='products/images')
    category = ForeignKey('apps.Category', on_delete=CASCADE)
    quantity = PositiveIntegerField(default=0)
    price = FloatField(default=0)
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Category(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name

    def count_blogs(self):
        return self.blog_set.count()

    class Meta:
        verbose_name_plural = 'Categories'


class Tag(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Blog(Model):
    name = CharField(max_length=255)
    image = ImageField(upload_to='blogs/images/', default='blogs/default-blog.jpg')
    author = ForeignKey('apps.User', CASCADE)
    category = ForeignKey('apps.Category', CASCADE)
    tags = ManyToManyField('apps.Tag')
    text = CKEditor5Field(blank=True, null=True)
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)

    def count_commit(self):
        return self.comment_set.count()

    def __str__(self):
        return self.name


class Comment(Model):
    text = CharField(max_length=255)
    blog = ForeignKey('apps.Blog', CASCADE)
    author = ForeignKey('apps.User', CASCADE)
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)
