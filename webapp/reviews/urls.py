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
    path('block/<int:following_user_id>/', views.block_user, name='block'),
    path('follow/unblock/<int:blocked_user_id>/', views.unblock_user, name='unblock'),
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('ticket/<int:ticket_id>/edit/', views.edit_ticket, name='edit_ticket'),
    path('ticket/<int:ticket_id>/delete/', views.delete_ticket, name='delete_ticket'),
]
