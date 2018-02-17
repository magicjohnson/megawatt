from django.db import models
from django.urls import reverse


class Site(models.Model):
    name = models.CharField(max_length=1024)

    def get_absolute_url(self):
        return reverse('site-detail', args=[str(self.id)])

    def __str__(self):
        return "%s: %s" % (self.pk, self.name)


class SiteDataRecord(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='records')
    date = models.DateField()
    value_a = models.DecimalField(max_digits=10, decimal_places=2)
    value_b = models.DecimalField(max_digits=10, decimal_places=2)
