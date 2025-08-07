from django.shortcuts import render, redirect, get_object_or_404
from reviews import forms
from reviews.utils import get_feed_posts, get_user_posts

from django.contrib.auth.decorators import login_required
from authentication.models import User
from reviews.models import Ticket, Review, UserFollow, UserBlock


@login_required
def feed(request):
    # Display the user feed with viewables posts
    posts = get_feed_posts(request.user)
    return render(request, "reviews/home.html", {"posts": posts})


@login_required
def post(request):
    # Display the current user's own posts
    posts = get_user_posts(request.user)
    return render(request, "reviews/post.html", {"posts": posts})


@login_required
def create_ticket(request):
    # Create a new ticket (with optional image)
    form = forms.TicketForm()

    if request.method == "POST":
        form = forms.TicketForm(request.POST, request.FILES)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user

            image = form.cleaned_data.get("image")
            if image:
                ticket.image = image

            ticket.save()
            return redirect("home")

    return render(request, "reviews/create_ticket.html", context={"form": form})


@login_required
def create_review(request, ticket_id):
    # Create a review in response to a specific ticket
    ticket = get_object_or_404(Ticket, id=ticket_id)
    form = forms.ReviewForm()

    if request.method == "POST":
        form = forms.ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("home")

    context = {
        "form": form,
        "ticket": ticket,
    }

    return render(request, "reviews/create_review.html", context=context)


@login_required
def create_ticket_and_review(request):
    # Create both a ticket and a review
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()

    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)

        # Validate both forms before saving
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)

            image = ticket_form.cleaned_data.get("image")
            if image:
                ticket.image = image

            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            return redirect("home")

    context = {
        "ticket_form": ticket_form,
        "review_form": review_form,
    }

    return render(request, "reviews/create_ticket_and_review.html", context=context)


@login_required
def edit_ticket(request, ticket_id):
    # Edit an existing ticket belonging to the user
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    if request.method == "POST":
        form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect("post")
    else:
        form = forms.TicketForm(instance=ticket)

    return render(request, "reviews/edit_ticket.html", {"form": form})


@login_required
def delete_ticket(request, ticket_id):
    # Delete a ticket belonging to the user
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    if request.method == "POST":
        ticket.delete()
        return redirect("post")

    return render(request, "reviews/delete_post.html", {"ticket": ticket})


@login_required
def edit_review(request, review_id):
    # Edit a review belonging to the user
    review = get_object_or_404(Review, id=review_id, user=request.user)
    ticket = review.ticket

    if request.method == "POST":
        form = forms.ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("post")
    else:
        form = forms.ReviewForm(instance=review)

    context = {
        "form": form,
        "ticket": ticket,
    }

    return render(request, "reviews/edit_review.html", context=context)


@login_required
def delete_review(request, review_id):
    # Delete a review belonging to the user
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == "POST":
        review.delete()
        return redirect("post")

    return render(request, "reviews/delete_post.html", {"review": review})


@login_required
def follow(request):
    # Manage following, followers, blocked users and display a form to follow other users
    if request.method == "POST":
        form = forms.FollowForm(request.POST, user=request.user)

        if form.is_valid():
            form.save()
            return redirect("follow")
    else:
        form = forms.FollowForm(user=request.user)

    following = UserFollow.objects.filter(user=request.user)
    followers = UserFollow.objects.filter(followed_user=request.user)
    blocked_user = UserBlock.objects.filter(user=request.user)

    return render(
        request,
        "reviews/follow.html",
        {"form": form, "following": following, "followers": followers, "blocked_user": blocked_user},
    )


@login_required
def unfollow(request, followed_user_id):
    # Unfollow a user
    relation = get_object_or_404(UserFollow, user=request.user, followed_user_id=followed_user_id)
    relation.delete()

    return redirect("follow")


@login_required
def block_user(request, following_user_id):
    # Block a user and remove follow relationship
    if request.method == "POST":
        blocked_user = get_object_or_404(User, id=following_user_id)
        UserBlock.objects.get_or_create(user=request.user, blocked_user=blocked_user)
        UserFollow.objects.filter(user=request.user, followed_user=blocked_user).delete()

    return redirect("home")


@login_required
def unblock_user(request, blocked_user_id):
    # Unblock a user
    if request.method == "POST":
        block_relation = get_object_or_404(UserBlock, user=request.user, blocked_user_id=blocked_user_id)
        block_relation.delete()

    return redirect("follow")
