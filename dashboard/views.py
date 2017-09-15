# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib.auth.models import User
from news.models import News
from perks.models import Perks
from events.models import Event

@user_passes_test(lambda u: u.is_superuser)
def index(request):
	news_list = News.objects.all().order_by('-pub_date')
	context = {
		'news_list': news_list,
	}
	return render(request, 'dashboard/content_dashboard.html', context)

@user_passes_test(lambda u: u.is_superuser)
def perks(request):
	news_list = Perks.objects.all().order_by('-pub_date')
	context = {
		'news_list': news_list,
	}
	return render(request, 'dashboard/perks_dashboard.html', context)

@user_passes_test(lambda u: u.is_superuser)
def users(request):
	user_list = User.objects.all()
	context = {
		'user_list': user_list,
	}
	return render(request, 'dashboard/users_dashboard.html', context)

@user_passes_test(lambda u: u.is_superuser)
def events(request):
	event_list = Event.objects.all()
	context = {
		'event_list': event_list,
	}
	return render(request, 'dashboard/events_dashboard.html', context)