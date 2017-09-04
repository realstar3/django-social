# Create your views here.
import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .models import News, Category
from bs4 import BeautifulSoup
import datetime

from django.contrib.auth.models import User


# Create your views here.
@login_required
def index(request):
    news_list = News.objects.all().order_by('-pub_date').exclude(is_page=True)
    total_articles = news_list.count()

    per = Paginator(news_list, 5)
    # total_page = per.count()
    first_page = per.page(1)
    navbar_pages = News.objects.filter(display_in_navbar=True)

    # Return three articles to render in the featured articles fields in template
    featured_news_list = News.objects.filter(featured=True).exclude(is_page=True).order_by('-pub_date')[1:3]
    primary_feature = News.objects.order_by('feature_rank').exclude(is_page=True).order_by('-pub_date')[0]
    category_list = Category.objects.all()

    try:
        feature_list = News.objects.order_by('-pub_date').exclude(is_page=True).order_by('-feature_rank')[0:3]

    except:
        feature_list = False

    context = {
        'news_list': first_page,
        'primary_feature': primary_feature,
        'featured_news_list': featured_news_list,
        'feature_list': feature_list,
        'total_articles': total_articles,
        'category_list': category_list,
        'navbar_pages': navbar_pages,
    }
    return render(request, 'news/news.html', context)


@login_required
def update(request):

    page_number = request.GET.get('pg_num', 0)

    news_list = News.objects.all().order_by('-pub_date').exclude(is_page=True)
    per = Paginator(news_list, 5)

    try:
        per_page = per.page(page_number)
    except Exception as e:
        print('Error: {}'.format(e))
        context = {
            'news_list': False,
        }
        return render(request, 'news/news-content.html', context)

    context = {
        'news_list': per_page,
    }
    return render(request, 'news/news-content.html', context)


@login_required
def category(request):
    category_name = request.GET.get('category')
    page_number = request.GET.get('pg_num', 0)
    category_name = str(category_name).replace("-", " ")
    tag = Category.objects.filter(tag=category_name).first()
    news_list = News.objects.filter(category=tag).order_by('-pub_date').exclude(is_page=True)
    per = Paginator(news_list, 5)

    try:
        per_page = per.page(page_number)
    except Exception as e:
        print('Error: {}'.format(e))
        context = {
            'news_list': False,
        }
        return render(request, 'news/news-content.html', context)

    context = {
        'news_list': per_page,
    }
    return render(request, 'news/news-content.html', context)


@login_required
def search(request):
    """
    
    :param request: 
    :return: 
    """

    keyword = request.GET.get('keyword', "")
    page_number = request.GET.get('pg_num', 0)

    news_list = News.objects.filter(title__icontains=keyword).filter(article__icontains=keyword).order_by('-pub_date').exclude(is_page=True)

    per = Paginator(news_list, 5)

    try:
        per_page = per.page(page_number)
    except Exception as e:
        print('Error: {}'.format(e))
        context = {
            'news_list': False,
        }
        return render(request, 'news/news-content.html', context)

    context = {
        'news_list': per_page,
    }
    return render(request, 'news/news-content.html', context)


@login_required
def detail(request, news_article_id):
    # return HttpResponse('Hello from Python!')

    # return latest four articles to present as 'related news'. Change to be related to tags in future (so that it is genuinely related news)

    news_article = News.objects.get(id=news_article_id)
    related_news = News.objects.filter().exclude(is_page=True).order_by('-pub_date')[0:4]
    navbar_pages = News.objects.filter(display_in_navbar=True)

    try:
        next_url = request.GET['next']
    except:
        next_url = False

    context = {
        'navbar_pages': navbar_pages,
        'news_article': news_article,
        'related_news': related_news,
        'next': next_url,
    }

    return render(request, 'news/news-details.html', context)


@login_required
def create(request):
    try:
        next_url = request.GET['next']

    except:
        next_url = False

    categories = Category.objects.all()
    navbar_pages = News.objects.filter(display_in_navbar=True)

    context = {
        'categories': categories,
        'create': True,
        'next': next_url,
        'navbar_pages': navbar_pages
    }

    if request.POST:
        owner = request.user

        body = request.POST['body']
        title = request.POST['title']

        feature_rank = request.POST.get('feature_rank', None)
        pub_date = datetime.datetime.now()
        selected_tag = request.POST.get('category', None)

        tag = Category.objects.filter(tag=selected_tag).first()

        is_page = request.POST.get('is_page', None)
        if is_page == 'OK':
            is_page = True
        else:
            is_page = False

        display_in_navbar = request.POST.get('display_in_navbar', None)
        if display_in_navbar == 'OK':
            display_in_navbar = True
        else:
            display_in_navbar = False

        news_article = News(title=title, article=body, feature_rank=feature_rank, pub_date=pub_date, owner=owner,
                            is_page=is_page, display_in_navbar=display_in_navbar)
        news_article.save()

        news_article.category.add(tag)

        return redirect('/dashboard')

    return render(request, 'news/news-edit.html', context)


@login_required
def edit(request, news_article_id):
    # return HttpResponse('Hello from Python!')
    # return latest four articles to present as 'related news'.
    # Change to be related to tags in future (so that it is genuinely related news)

    news_article = News.objects.get(id=news_article_id)
    related_news = News.objects.filter().order_by('-pub_date')[0:4]
    try:
        next_url = request.GET['next']
    except:
        next_url = False

    categories = Category.objects.all()
    navbar_pages = News.objects.filter(display_in_navbar=True)

    context = {
        'categories': categories,
        'news_article': news_article,
        'related_news': related_news,
        'next': next_url,
        'navbar_pages': navbar_pages,
    }

    if request.POST:
        body = request.POST['body']
        title = request.POST['title']

        feature_rank = request.POST.get('feature_rank', None)
        selected_tag = request.POST.get('category', None)

        is_page = request.POST.get('is_page', None)
        if is_page == 'OK':
            is_page = True
        else:
            is_page = False

        display_in_navbar = request.POST.get('display_in_navbar', None)
        if display_in_navbar == 'OK':
            display_in_navbar = True
        else:
            display_in_navbar = False

        tag = Category.objects.filter(tag=selected_tag).first()

        news_article.article = body
        news_article.title = title
        news_article.feature_rank = feature_rank
        news_article.category.add(tag)
        news_article.is_page = is_page
        news_article.display_in_navbar = display_in_navbar

        news_article.save()

        return redirect('detail', news_article_id=news_article.id)

    return render(request, 'news/news-edit.html', context)


@login_required
def delete(request, news_article_id):
    news_article = News.objects.get(id=news_article_id)
    news_article.delete()

    context = {}

    return redirect('/dashboard')


# @login_required
# def category(request, keyword):
#     """
#     arrange the list by category
#     :param request:
#     :param keyword:
#     :return:
#     """
#     news_json = []
#     try:
#         tag = Category.objects.filter(tag=keyword).first()
#         news_list = News.objects.filter(category=tag)
#
#         for news_item in news_list:
#             print(news_item.owner)
#             news_json.append({
#                 'category': category,
#                 'img': previewImage(news_item.article),
#                 'title': news_item.title,
#                 'id': news_item.id,
#                 'snippet': snippet(news_item.article),
#                 'owner': news_item.owner
#             })
#
#     except Exception as e:
#         print('error: {}'.format(e))
#         news_json = []
#
#     # print('news_json: {}'.format(news_json))
#     response = HttpResponse()
#     response['Content-Type'] = "text/javascript"
#     response.write(news_json)
#     return response
