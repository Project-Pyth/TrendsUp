import datetime
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from mysite import repeated
from post.models import Post, Category, PostComment
from post.forms import CreatePostForm, UpdatePostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from post.templatetags import extras


# Post Creation View
@login_required(login_url='account:must_authenticate')
def create_post(request):
    context = {}

    # Footer
    context['foot'] = repeated.footer()

    user = request.user
    if not user.is_authenticated:
        return redirect('account:must_authenticate')
    post_form = CreatePostForm(request.POST or None, request.FILES or None)
    cat = Category.objects.all()
    def_cat = Category.objects.filter(name='World')
    if post_form.is_valid():
        post_form = post_form.save(commit=False)
        author = User.objects.filter(email=user.email).first()
        post_form.author = author
        post_form.save()
        context[
            'messages'] = 'Your Post has been created successfully and it will be uploaded within 24 hours if approved by the admin.'

        # return redirect('trendsup:index')
    post_form = CreatePostForm()
    context['post_form'] = post_form
    context['cat'] = cat
    context['def'] = def_cat
    return render(request, 'post/create_post.html', context)


# Single Post Detail View
@login_required(login_url='account:must_authenticate')
def detail_view(request, slug):
    context = {}
    # API
    context = repeated.api(context)

    # Category Dropdown
    context['cate'] = repeated.category_dropdown()

    # Footer
    context['foot'] = repeated.footer()

    post = get_object_or_404(Post, slug=slug)

    # Passing Comments
    comments = PostComment.objects.filter(post=post, parent=None)
    replies = PostComment.objects.filter(post=post).exclude(parent=None)
    replydict = {}
    for reply in replies:
        if reply.parent.pk not in replydict.keys():
            replydict[reply.parent.pk] = [reply]
        else:
            replydict[reply.parent.pk].append(reply)
    context['comments'] = comments
    context['replydict'] = replydict

    post1 = Post.objects.filter(status=True).order_by('?').first()
    post2 = Post.objects.filter(status=True).order_by('?').first()
    pp = []
    start = datetime.datetime.today()
    end = start - datetime.timedelta(days=7)
    for i in range(6):
        pp.append(Post.objects.filter(date_posted__range=[end, start], status=True, category=post.category).order_by(
            '?').first())
    context['pp'] = pp
    context['post'] = post
    context['post1'] = post1
    context['post2'] = post2
    return render(request, 'post/detail.html', context)


# Post Edit View
@login_required(login_url='account:must_authenticate')
def edit_post(request, slug):
    context = {}

    # Footer

    context['foot'] = repeated.footer()

    user = request.user
    if not user.is_authenticated:
        return redirect('account:must_authenticate')
    post = get_object_or_404(Post, slug=slug)
    if request.POST:
        post_form = UpdatePostForm(request.POST, request.FILES or None, instance=post)
        if post_form.is_valid():
            obj = post_form.save(commit=False)
            obj.save()
            context['success_message'] = 'Your Post Has Been Updated.'
            post = obj

    post_form = UpdatePostForm(
        initial={
            'title': post.title,
            'body': post.body,
            'image': post.image,
        }
    )
    context['post_form'] = post_form
    return render(request, 'post/edit_post.html', context)


# Post Deletion View
@login_required(login_url='account:must_authenticate')
def delete_post(request, slug):
    context = {}

    # Footer

    context['foot'] = repeated.footer()

    Post.objects.get(slug=slug).delete()
    context['message'] = 'Your Post Has Been Deleted Successfully.'
    return render(request, 'post/del_post.html', context)



# Posting Comments View
@login_required(login_url='account:must_authenticate')
def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user = request.user
        postpk = request.POST.get('postpk')
        post = Post.objects.get(pk=postpk, status=True)
        parentpk = request.POST.get('parentpk')
        if parentpk == '':
            comment = PostComment(comment=comment, user=user, post=post)
            comment.save()
        else:
            parent = PostComment.objects.get(pk=parentpk)
            comment = PostComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
    return redirect(f"/post/{post.slug}/")


# View To Display Single Category Posts
@login_required(login_url='account:must_authenticate')
def category_view(request, pk):
    context = {}

    # API
    context = repeated.api(context)

    # Category Dropdown
    context['cate'] = repeated.category_dropdown()

    # Footer
    context['foot'] = repeated.footer()

    heading = Category.objects.all().filter(pk=pk)
    context['heading'] = heading
    post = Post.objects.all().filter(category=pk, status=True).order_by('-date_posted')

    # Pagination

    posts = repeated.pagination(request, post)
    context['posts'] = posts

    pp = []
    start = datetime.datetime.today()
    end = start - datetime.timedelta(days=15)
    for i in range(6):
        pp.append(Post.objects.filter(date_posted__range=[end, start], status=True).order_by('?').first())
    context['pp'] = pp
    return render(request, 'post/category.html', context)


# Author Profile View
@login_required(login_url='account:must_authenticate')
def author(request, pk=None):
    context = {}
    # API
    context = repeated.api(context)

    # Category Dropdown
    context['cate'] = repeated.category_dropdown()

    # Footer
    context['foot'] = repeated.footer()
    if request.method == 'GET':
        post = Post.objects.all().filter(author=pk, status=True)
        author_name = User.objects.get(pk=pk)
        context['author_name'] = author_name
        # Pagination

        posts = repeated.pagination(request, post)
        context['posts'] = posts

        pp = []
        start = datetime.datetime.today()
        end = start - datetime.timedelta(days=15)
        for i in range(6):
            pp.append(Post.objects.filter(date_posted__range=[end, start], status=True).order_by('?').first())
        context['pp'] = pp
        return render(request, 'post/author.html', context)


# Posts Pending For Approval View
@login_required(login_url='account:must_authenticate')
def pending(request):
    context = {}
    # API
    context = repeated.api(context)

    # Category Dropdown
    context['cate'] = repeated.category_dropdown()

    # Footer
    context['foot'] = repeated.footer()

    if request.user.is_staff:
        if request.method == 'GET':
            posts = Post.objects.filter(status=False)
            context['posts'] = posts
            return render(request, 'post/pending.html', context)


# Post Approve View
@login_required(login_url='account:must_authenticate')
def approve(request, pk):
    context = {}

    # Footer
    context['foot'] = repeated.footer()

    if request.user.is_staff:
        if request.method == 'POST':
            Post.objects.filter(pk=pk).update(status=True)
            context['message'] = 'Post is Successfully Approved and Will Be Displayed Soon on The Home Page. '
            return render(request, 'post/post_approved.html', context)


# Returning Posts Matching The Query
def get_post_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = Post.objects.filter(
            Q(title__icontains=q) |
            Q(body__icontains=q)
            , status=True
        ).distinct()
        for post in posts:
            queryset.append(post)
    return list(set(queryset))
