from django_filters import rest_framework as filters

from reviews.models import Title


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class TitleFilter(filters.FilterSet):
    """Фильтр для произведений."""
    category = CharFilterInFilter(field_name='category__slug',
                                  lookup_expr='in')
    genre = CharFilterInFilter(field_name='genre__slug', lookup_expr='in')
    name = CharFilterInFilter(field_name='title__name', lookup_expr='in')
    year = filters.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']
