from django.db import models
from datetime  import datetime
from django.utils import formats
# Create your models here.

from django_hosts.resolvers import reverse
from .utils import code_generator, create_shortcode

from .validators import validate_url, validate_dot_com


class thwURLManager(models.Manager):
	def all(self, *args, **kwargs):
		qs_main = super(thwURLManager, self).all(*args,**kwargs)
		qs = qs_main.filter(active=True)
		objects = []
		for q in qs:
			objects.append(q)
		return objects


	def refresh_shortcodes(self, items=None):
		qs = thwURL.objects.filter(id__gte=1)
		if items is not None and isinstance(items, int):
			qs = qs.order_by('-id')[:items]
		new_codes = 0
		for q in qs:
			q.shortcode = create_shortcode(q)
			print(q.id)
			q.save()
			new_codes += 1
		return "New codes made: {i}".format(i=new_codes)


class thwURL(models.Model):
	url         = models.CharField(max_length=220, validators=[validate_url, validate_dot_com])
	shortcode   = models.CharField(max_length=8,unique=True)
	updated     = models.DateTimeField(auto_now=True,blank=False)
	timestamp   = models.DateTimeField(auto_now_add=True,blank=False)
	t_created   = models.DateTimeField(default=datetime.now, blank=False)
	active      = models.BooleanField(default=True)
	objects = thwURLManager()
	def save(self, *args, **kwargs):
		if self.shortcode is None or self.shortcode == "":
			self.shortcode = create_shortcode(self)
		if not "http" in self.url:
			self.url = "http://" + self.url
		super(thwURL, self).save(*args, **kwargs)

#	def index(request):
#		urlsave=thwURL.objects.all()
#		return render(request,'home.html',{'urlsave':urlsave})


	def __str__(self):
		return str(self.url)

	def __unicode__(self):
		return str(self.url)

	def get_short_url(self):
		url_path = reverse("scode", kwargs={'shortcode': self.shortcode}, host='www', scheme='http')
		return url_path