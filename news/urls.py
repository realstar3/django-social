from django.conf.urls import url

from news import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    url(r'^(?P<news_article_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<news_article_id>[0-9]+)/edit$', views.edit, name='edit'),
    url(r'^(?P<news_article_id>[0-9]+)/delete$', views.delete, name='delete'),

]