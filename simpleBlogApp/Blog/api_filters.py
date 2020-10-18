from django_filters import rest_framework as filters
from django_filters import widgets


class PostsFilter(filters.FilterSet):
    blog_id = filters.BaseInFilter(field_name="blog_id", lookup_expr="in")