from itertools import chain
from operator import attrgetter
from .models import Ticket, Review, UserFollow, UserBlock


def get_feed_posts(user):
    """
    Retrieve posts for the feed:
    - Include the active user + followed users
    - Exclude blocked users
    - Also include reviews on my tickets
    """

    # Users to include: User + followed_user
    users = [user]
    followed_users = UserFollow.objects.filter(user=user).values_list('followed_user', flat=True)
    users += list(followed_users)

    blocked_user_ids = UserBlock.objects.filter(user=user).values_list('blocked_user_id', flat=True)

    # Filtered tickets and reviews
    tickets = Ticket.objects.filter(user__in=users).exclude(user__in=blocked_user_ids)
    reviews = Review.objects.filter(user__in=users).exclude(user__in=blocked_user_ids)

    # Include reviews user tickets if they are not from blocked users
    reviews_on_user_tickets = Review.objects.filter(ticket__user=user).exclude(user__in=blocked_user_ids)
    reviews = (reviews | reviews_on_user_tickets).distinct()

    for ticket in tickets:
        ticket.content_type = "ticket"
    for review in reviews:
        review.content_type = "review"

    posts = sorted(chain(tickets, reviews), key=attrgetter("time_created"), reverse=True)
    return posts


def get_user_posts(user):
    """Retrieve only user posts"""
    tickets = Ticket.objects.filter(user=user)
    reviews = Review.objects.filter(user=user)

    for ticket in tickets:
        ticket.content_type = "ticket"
    for review in reviews:
        review.content_type = "review"

    posts = sorted(chain(tickets, reviews), key=attrgetter("time_created"), reverse=True)
    return posts
