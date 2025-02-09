from django.db import models

class Org(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    source_id = models.CharField(max_length=128, null=True, blank=True)
    facility_type = models.CharField(max_length=128, null=True, blank=True)
    authority_name = models.CharField(max_length=128, null=True, blank=True)
    isced010 = models.CharField(max_length=128, null=True, blank=True)
    isced020 = models.CharField(max_length=128, null=True, blank=True)
    isced1 = models.CharField(max_length=128, null=True, blank=True)
    isced2 = models.CharField(max_length=128, null=True, blank=True)
    isced3 = models.CharField(max_length=128, null=True, blank=True)
    isced4plus = models.CharField(max_length=128, null=True, blank=True)
    olms_status = models.CharField(max_length=128, null=True, blank=True)
    full_addr = models.CharField(max_length=128, null=True, blank=True)
    unit = models.CharField(max_length=128, null=True, blank=True)
    street_no = models.CharField(max_length=128, null=True, blank=True)
    street_name = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    prov_terr = models.CharField(max_length=128, null=True, blank=True)
    postal_code = models.CharField(max_length=128, null=True, blank=True)
    pruid = models.CharField(max_length=128, null=True, blank=True)
    csdname = models.CharField(max_length=128, null=True, blank=True)
    csduid = models.CharField(max_length=128, null=True, blank=True)
    longitude = models.CharField(max_length=128, null=True, blank=True)
    latitude = models.CharField(max_length=128, null=True, blank=True)
    geo_source = models.CharField(max_length=128, null=True, blank=True)
    provider = models.CharField(max_length=128, null=True, blank=True)
    cmaname = models.CharField(max_length=128, null=True, blank=True)
    cmauid = models.CharField(max_length=128, null=True, blank=True)

    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['deleted', 'name'], name='org_idx'),
        ]

    def __str__(self):
        return self.name

