from django.urls import path
from reviews import views

urlpatterns = [
    path('home/', views.feed, name='home'),
    path('post/', views.post, name='post'),
    path('create_ticket/', views.create_ticket, name='create_ticket'),
    path('create_review/<int:ticket_id>/', views.create_review, name='create_review'),
    path('create_ticket_and_review/', views.create_ticket_and_review, name='create_ticket_and_review'),
    path('follow/', views.follow, name='follow'),
    path('unfollow/<int:followed_user_id>/', views.unfollow, name='unfollow'),
]
