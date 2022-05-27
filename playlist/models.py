from email.policy import default
from django.db import models
from django.core.cache import cache

# Create your models here.

class Playlist(models.Model):
    id = models.AutoField(primary_key=True)
    playlist_name = models.CharField(max_length=254, blank=False, null=False)
    videos = models.JSONField(default=dict, blank=False, null=False)
    username = models.CharField(max_length=254, blank=False, null=False)

    def save(self, *args, **kwargs):
        cache.delete('playlist-'+self.username)
        super(Playlist, self).save(*args, **kwargs)

    def delete_update(self):
        self.delete()
        cache.delete('playlist-'+self.username)