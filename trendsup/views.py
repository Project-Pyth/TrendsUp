import datetime
from operator import attrgetter
from django.shortcuts import render
from post.models import Post
from post.views import get_post_queryset
from mysite import repeated


def index(request):
    context = {}
    # API
    context = repeated.api(context)

    # Category Dropdown
    context['cate'] = repeated.category_dropdown()

    # Footer
    context['foot'] = repeated.footer()

    # Header Posts

    pp = []
    start = datetime.datetime.today()
    end = start - datetime.timedelta(days=7)
    for i in range(4):
        pp.append(Post.objects.filter(date_posted__range=[end, start], status=True,).order_by('?').first())
        context['pp' + str(i)] = pp
        pp = []

    # Search

    query = " "
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)

    # Index Posts sorted based on date posted

    post = sorted(get_post_queryset(query), key=attrgetter('date_posted'), reverse=True)

    # Pagination

    posts = repeated.pagination(request, post)
    context['posts'] = posts

    # Popular Post
    pp = []
    start = datetime.datetime.today()
    end = start - datetime.timedelta(days=15)
    for i in range(6):
        pp.append(Post.objects.filter(date_posted__range=[end, start], status=True).order_by('?').first())
    context['pp'] = pp

    return render(request, 'index.html', context)


def about(request):
    context = {}

    # Footer
    context['foot'] = repeated.footer()
    return render(request, 'snippets/about_us.html', context)


def contact(request):
    context = {}

    # Footer
    context['foot'] = repeated.footer()
    return render(request, 'snippets/contact_us.html', context)


def error_404_view(request, exception):
    return render(request, '404/error.html', {'error': 404, 'er_txt': 'the page you are looking for not avaiable!'})


def error_500_view(request):
    return render(request, '404/error.html', {'error': 500, 'er_txt': 'Uh Oh!, Looks like server went way down hill'})
