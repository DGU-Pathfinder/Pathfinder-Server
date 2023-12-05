import django_filters

from django.contrib.auth import get_user_model
from .models import RtImage

User = get_user_model()


class RtImageFilter(django_filters.FilterSet):
    upload_date = django_filters.DateFromToRangeFilter(
        field_name  ='upload_date',
        method      ='filter_upload_date'
    )
    score = django_filters.NumericRangeFilter(
        field_name  ='ai_model__ai_defect_set__score',
        method      ='filter_score'
    )
    modifier = django_filters.ModelChoiceFilter(
        queryset    = User.objects.all(),
        method      = 'filter_modifier'
    )
    uploader = django_filters.ModelChoiceFilter(
        queryset    = User.objects.all(),
        method      ='filter_uploader'
    )
    expert_check = django_filters.BooleanFilter(
        method  = 'filter_expert_check'
    )

    class Meta:
        model   = RtImage
        fields  = [
            'uploader',
            'upload_date',
            'score',
            'modifier',
            'expert_check'
        ]

    def filter_upload_date(self, queryset, name, value):
        if value:
            return queryset.filter(
                upload_date__range = (value.start, value.stop)
            )
        return queryset

    def filter_score(self, queryset, name, value):
        if value:
            return queryset.filter(
                ai_model__ai_defect_set__score__range = (value.start, value.stop)
            )
        return queryset

    def filter_modifier(self, queryset, name, value):
        if value:
            return queryset.filter(
                expert__expert_defect_set__modifier = value
            )
        return queryset

    def filter_uploader(self, queryset, name, value):
        if value:
            return queryset.filter(uploader=value)
        return queryset

    def filter_expert_check(self, queryset, name, value):
        if value:
            return queryset.filter(expert__isnull=False)
        else:
            return queryset.filter(expert__isnull=True)