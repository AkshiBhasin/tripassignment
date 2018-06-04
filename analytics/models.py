from django.db import models
from datetime  import datetime
# Create your models here.
from shortener.models import thwURL


class ClickEventManager(models.Manager):
    def create_event(self, thwInstance):
        if isinstance(thwInstance, thwURL):
            obj, created = self.get_or_create(thw_url=thwInstance)
            obj.count += 1
            obj.save()
            return obj.count
        return None

class ClickEvent(models.Model):
	thw_url     = models.OneToOneField(thwURL, on_delete=models.DO_NOTHING)
	count       = models.IntegerField(default=0 )
	updated     = models.DateTimeField(auto_now=True)
	timestamp   = models.DateTimeField(auto_now_add=True)
	#t_created   = models.DateTimeField(default=datetime.now, blank=False)
	objects     = ClickEventManager()
	

	def __str__(self):
		return "{i}".format(i=self.count)