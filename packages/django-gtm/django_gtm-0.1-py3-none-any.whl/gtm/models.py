from django.db import models
from django.core.cache import cache


class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)
        self.set_cache()

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        if cache.get(cls.__name__) is None:
            obj, created = cls.objects.get_or_create(pk=1)
            if not created:
                obj.set_cache()
        return cache.get(cls.__name__)

    def set_cache(self):
        cache.set(self.__class__.__name__, self)


class GTMDefault(SingletonModel):
    """
    Google Tag Manager Default value.
    """
    code = models.CharField(max_length=32, default='')


class GTMSettings(models.Model):
    """
    GTM Settings that can be named.
    """
    name = models.CharField(max_length=24, unique=True)
    code = models.CharField(max_length=32, default='')
