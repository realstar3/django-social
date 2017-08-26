# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
import dateutil.parser

# from .models import Event
from .models import Event


# Create your views here.

@login_required
def index(request):
    try:
        week = int(request.GET.get('week', ''))
        next_week = week + 1
        previous_week = week - 1

    except:
        week = 0
        next_week = 1
        previous_week = -1

    # this sets up for a 10 day event view window in the template
    base_date = datetime.now() + timedelta(week * 10)
    limit_date = datetime.now() + timedelta(10 + week * 10)
    print(base_date, limit_date)
    event_list = Event.objects.filter(start_date__gte=base_date).filter(start_date__lte=limit_date).order_by(
        'start_date')

    context = {
        'next_week': next_week,
        'previous_week': previous_week,
        'event_list': event_list
    }
    print event_list

    return render(request, 'events/event-list.html', context)


@login_required
def detail(request, event_id):
    event = Event.objects.get(id=event_id)
    context = {
        'event': event,
    }
    return render(request, 'events/event-details.html', context)


@login_required
def create(request):
    """
    Create new event.
    :param request: 
    :return: 
    """

    event_id = request.POST.get("event_id", None)
    print('event_id:', event_id)
    if event_id:
        body = request.POST['body']
        event = Event.objects.get(id=event_id)
        event.description = body
        event.save()

        return redirect('/events/' + event_id)

    else:
        title = request.POST["title"]
        start_time = request.POST["start-time"]
        start_day = request.POST["start-date"]
        start_date = dateutil.parser.parse(start_time + ' ' + start_day)

        pub_time = request.POST["end-time"]
        pub_day = request.POST["end-date"]
        pub_date = dateutil.parser.parse(pub_time + ' ' + pub_day)

        feature_image = request.POST["featureImage"]
        if feature_image:
            featured = True
        else:
            featured = False

        event_url = request.POST["event-url"]

        new_event = Event(title=title, image=feature_image, start_date=start_date,
                          pub_date=pub_date, event_url=event_url, featured=featured)
        new_event.save()

        context = {
            'start_date': start_day + " " + start_time,
            'pub_date': pub_day + " " + pub_time,
            'title': title,
            'event_id': new_event.id
        }

        return render(request, 'events/event-edit.html', context=context)


@login_required
def edit(request):
    if request.POST:
        pass


@login_required
def delete(request):
    pass
