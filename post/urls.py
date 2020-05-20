from django.urls import path
from post import views

app_name = 'post'

urlpatterns = [
    path('pending/', views.pending, name='pending'),
    path('approve/<pk>', views.approve, name='approve'),
    path('postComment/', views.postComment, name='postComment'),
    path('create/', views.create_post, name='create'),
    path('<slug>/', views.detail_view, name='detail'),
    path('category/<pk>', views.category_view, name='category'),
    path('author/<pk>', views.author, name='author'),
    path('<slug>/edit', views.edit_post, name='edit'),
    path('<slug>/delete/', views.delete_post, name='delete_post'),

]
