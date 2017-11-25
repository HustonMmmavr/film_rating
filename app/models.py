from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count, Sum, Avg
from django.core.urlresolvers import reverse
from django.db.models.functions import Coalesce
import datetime

class FilmRatingManager(models.Manager):
    def save_rating(self, film_id, film_rating, user_id):
        obj, new = self.update_or_create(film_id=film_id, user_id=user_id, defaults={'film_rating': film_rating})
        if new != None:
            obj = new
        return self.get_rating(film_id)

    def get_rating(self, film_id):
        res = self.filter(film_id=film_id).aggregate(avg=Avg('film_rating'))['avg']
        return res if res else -1

class FilmRating(models.Model):
    film_id = models.IntegerField()
    film_rating = models.IntegerField(default = 0)
    user_id = models.IntegerField()

    objects = FilmRatingManager()
