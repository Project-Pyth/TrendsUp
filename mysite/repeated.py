# Repeated Package

import json
import urllib
import operator

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from post.models import Category, Post


# Function For Displaying Footer Categories
def footer():
    # Footer

    foot_cat = Category.objects.all()
    foot = {}
    for i in foot_cat:
        foot[i.name] = Post.objects.all().filter(category=i.pk).count()
    d = dict(sorted(foot.items(), key=operator.itemgetter(1), reverse=True))
    return d


# Function For Displaying API's
def api(context):
    cat = (
        'science',
        'technology',
        'business',
        'entertainment',
        'sports',

    )

    for i in cat:
        with urllib.request.urlopen(
                "http://newsapi.org/v2/top-headlines?country=in&category=" + str(
                    i) + "&pageSize=4&apiKey=e7d1b2d281964be6a4a42dd6935aee20") as url:
            document = json.loads(url.read().decode())
            context[i] = document['articles']
    return context


# Function For Displaying Categories Dropdown
def category_dropdown():
    cate = Category.objects.all()
    return cate


# Function For Pagination
def pagination(request, post):
    POST_PER_PAGE = 8
    page = request.GET.get('page', 1)
    posts_paginator = Paginator(post, POST_PER_PAGE)
    try:
        posts = posts_paginator.page(page)
    except PageNotAnInteger:
        posts = posts_paginator.page(POST_PER_PAGE)
    except EmptyPage:
        posts = posts_paginator.page(posts_paginator.num_pages)
    return posts
