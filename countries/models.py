from django.db import models


MEASURE_GROUPS = [
    ('SD', 'Social distance'),
    ('BC', 'Business closed'),
    ('Other', 'Other')
]

class Country(models.Model):
    name = models.CharField(primary_key=True, max_length=56)
    population = models.PositiveIntegerField()
    first_case = models.DateField(blank=True, null=True)
    first_death = models.DateField(blank=True, null=True)
    emergency_state = models.BooleanField(default=False)
    quarantine = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class DailyReport(models.Model):
    date = models.DateField()
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    cases = models.PositiveIntegerField(default=0)
    deaths = models.PositiveIntegerField(default=0)
    recoveries = models.PositiveIntegerField(default=0)
    critical = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together=('date', 'country')


class Measure(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    group = models.CharField(choices=MEASURE_GROUPS, default='Other', max_length=100)
