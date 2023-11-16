import django_filters
from ..accounts.models import User
from .models import RtImage

class RtImageFilter(django_filters.FilterSet):
    upload_date = django_filters.DateFromToRangeFilter()
    score = django_filters.NumericRangeFilter(method='filter_score')
    expert_check = django_filters.BooleanFilter(
        method  = 'filter_expert_check'
    )
    modifier = django_filters.ModelChoiceFilter(
        queryset    = User.objects.all(),
        method      = 'filter_modifier'
    )
    uploader = django_filters.ModelChoiceFilter(
        queryset    = User.objects.all()
    )

    class Meta:
        model   = RtImage
        fields  = [
            'uploader__username',
            'upload_date',
            'score',
            'expert_check',
            'modifier__username',
        ]

    def filter_score(self, queryset, name, value):
        if value:
            return queryset.filter(
                ai_model__score__range  = (value.start, value.stop)
            )
        return queryset
    
    def filter_expert_check(self, queryset, name, value):
        return queryset.filter(ai_model__expert_check=value)

    def filter_modifier(self, queryset, name, value):
        if value:
            return queryset.filter(ai_model__d__modifier=value)
        return queryset
