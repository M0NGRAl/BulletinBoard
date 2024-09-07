import django_filters
from .models import Response, Advertisement

class ResponseFilter(django_filters.FilterSet):
    advertisement = django_filters.ModelChoiceFilter(
        queryset=Advertisement.objects.none(),  # По умолчанию ничего не отображаем
        label="Объявление",
        empty_label="Все объявления"
    )

    class Meta:
        model = Response
        fields = ['advertisement']