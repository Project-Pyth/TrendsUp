from django.conf.urls import url
from django.urls import path
from account import views

app_name = 'account'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('must_authenticate/', views.must_authenticate, name='must_authenticate'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('change-password/done/', views.change_password_done, name='change_password_done'),
    url(r'^delete/(?P<username>[\w|W.-]+)/$', views.delete_account, name='delete'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
