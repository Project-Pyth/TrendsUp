from django.urls import path
from trendsup.views import index, about, contact

app_name = 'trendsup'

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact')
]
