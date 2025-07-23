from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from itertools import chain
from operator import attrgetter
from .models import Ticket, Review, UserFollows


def resize_image(image_file, max_width=256, max_height=256):
    img = Image.open(image_file)
    img.thumbnail((max_width, max_height), Image.LANCZOS)

    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)

    return InMemoryUploadedFile(
        buffer,
        field_name='ImageField',
        name=image_file.name,
        content_type='image/jpeg',
        size=sys.getsizeof(buffer),
        charset=None
    )


def get_user_posts(user, include_followed=False):
    users = [user]
    if include_followed:
        followed_users = UserFollows.objects.filter(user=user).values_list('followed_user', flat=True)
        users += list(followed_users)

    tickets = Ticket.objects.filter(user__in=users)
    reviews = Review.objects.filter(user__in=users)

    reviews_on_my_tickets = Review.objects.filter(ticket__user=user)
    all_reviews = (reviews | reviews_on_my_tickets).distinct()

    for ticket in tickets:
        ticket.content_type = "ticket"
    for review in all_reviews:
        review.content_type = "review"

    posts = sorted(chain(tickets, all_reviews), key=attrgetter("time_created"), reverse=True)
    return posts
