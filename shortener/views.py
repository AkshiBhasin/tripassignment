from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic import ListView

from .forms import SubmitUrlForm
from .models import thwURL
from analytics.models import ClickEvent 

# Create your views here.
def home_view_fbv(request, *args, **kwargs):
    if request.method == "POST":
        print(request.POST)
    return render(request, "shortener/home.html", {})

class HomeView(View):
	def get(self, request, *args, **kwargs):
	 	the_form = SubmitUrlForm()
	 	b =	thwURL.objects.all()
	 	paginator = Paginator(b, 3)
	 	page = request.GET.get('page')
	 	#obj= paginator.get_page(page)
	 	try:
	 		b = paginator.page(page)
	 	except PageNotAnInteger:
	 		b = paginator.page(1)
	 	except EmptyPage:
	 		b = paginator.page(paginator.num_pages)	 		 	
	 	context = {
	 		"title": "",
	 		"form": the_form,
	 		"bb":b
	 		}
	 	#print(context)
	 	return render(request, "shortener/home.html", context)

	def post(self, request, *args, **kwargs):
		form = SubmitUrlForm(request.POST)
		context = {
		"title": "",
		"form": form
		}
		template = "shortener/home.html"
		if form.is_valid():
			new_url = form.cleaned_data.get("url")
			obj, created = thwURL.objects.get_or_create(url=new_url)
			context = {
			    "object": obj,
			    "created": created,
			}
			if created:
				template = "shortener/success.html"
			else:
				template = "shortener/already-exists.html"
		return render(request, template, context)


class URLRedirectView(View):
	def get(self, request, shortcode=None, *args, **kwargs):
		qs = thwURL.objects.filter(shortcode__iexact=shortcode)
		if qs.count() != 1 and not qs.exists():
			raise Http404
		obj = qs.first()
		print(ClickEvent.objects.create_event(obj))
		return HttpResponseRedirect(obj.url)

	