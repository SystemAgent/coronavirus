from django.contrib import admin

from stats.models import Total, Individual


class TotalAdmin(admin.ModelAdmin):
    list_display = (
        'observation_date',
        'country',
        'confirmed',
        'deaths',
        'recovered',
        'province_state',
        'last_update',
    )
    ordering = ['-observation_date']
    search_fields = ['country']
    sortable_by = [
        'observation_date',
        'confirmed',
        'deaths',
        'recovered',
    ]


class IndividualAdmin(admin.ModelAdmin):
    list_display = (
        'country',
        'age',
        'sex',
        'city',
        'province',
        'symptoms',
    )
    ordering = ['-observation_date']
    search_fields = ['country', 'city', 'province', 'symptoms']


admin.site.register(Total, TotalAdmin)
admin.site.register(Individual)
