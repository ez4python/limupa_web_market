import django_filters
from apps.models import Blog


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Blog
        fields = ('name',)
