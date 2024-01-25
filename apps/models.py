import uuid

from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CharField, ForeignKey, CASCADE, ManyToManyField, DateTimeField, ImageField, \
    PositiveIntegerField, FloatField, UUIDField, EmailField
from django_ckeditor_5.fields import CKEditor5Field
from django_resized import ResizedImageField
from apps.tasks import task_send_email


class User(AbstractUser):
    image = ResizedImageField(size=[200, 200], crop=['middle', 'center'], upload_to='users/images',
                              default='users/default.jpg')


class CreatedBaseModel(Model):
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Product(CreatedBaseModel):
    title = CharField(max_length=255)
    description = CKEditor5Field(blank=True, null=True, config_name='extends')
    category = ForeignKey('apps.Category', CASCADE)
    image = ForeignKey('apps.ProductImage', CASCADE, related_name='products_images')
    quantity = PositiveIntegerField(default=0)
    price = FloatField()

    def __str__(self):
        return self.title


class ProductImage(Model):
    image = ImageField(upload_to='products/images/', default='products/default-product.jpg')
    product_id = ForeignKey('apps.Product', CASCADE)


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


class Blog(CreatedBaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = CharField(max_length=255)
    image = ImageField(upload_to='blogs/images/', default='blogs/default-blog.jpg')
    # qr_code_image = ImageField(upload_to='blogs')
    author = ForeignKey('apps.User', CASCADE)
    category = ForeignKey('apps.Category', CASCADE)
    tags = ManyToManyField('apps.Tag')
    text = CKEditor5Field(blank=True, null=True, config_name='extends')
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.id in None:
            all_emails: list = NewsReceiver.objects.values_list('email', flat=True)
            task_send_email.delay('New blog added', self.name, list(all_emails))
        super().save(force_insert, force_update, using, update_fields)

    def count_commit(self):
        return self.comment_set.count()

    def __str__(self):
        return self.name


class Comment(CreatedBaseModel):
    text = CharField(max_length=255)
    blog = ForeignKey('apps.Blog', CASCADE)
    author = ForeignKey('apps.User', CASCADE)
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.blog.name


class NewsReceiver(CreatedBaseModel):
    email = EmailField()

    def __str__(self):
        return self.email
