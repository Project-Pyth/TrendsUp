"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings, urls
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.static import serve

urlpatterns = [
    path('', include('trendsup.urls')),
    path('account/', include('account.urls')),
    path('admin/', admin.site.urls, name='admin'),
    path('post/', include('post.urls', 'post')),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # Password Reset
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
         name='password_change'),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/reset.html'),
         name='password_reset_confirm'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),

    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

    url(r'^auth_social/', include('social_django.urls', namespace='social'))
]

urls.handler404 = 'trendsup.views.error_404_view'
urls.handler500 = 'trendsup.views.error_500_view'
