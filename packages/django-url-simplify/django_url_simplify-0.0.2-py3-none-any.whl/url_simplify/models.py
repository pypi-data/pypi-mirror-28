from django.db import models
from django.conf import settings
from shortuuid import ShortUUID


class Url(models.Model):
    full_url = models.CharField(max_length=2083)
    short_id = models.CharField(max_length=200)
    redirects = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s, %d" % (self.full_url, self.redirects)

    @staticmethod
    def gen_short_id():
        """
        Helper which randomly generates base62 id
        """
        return ShortUUID().random(length=settings.SHORT_ID_LEN)
