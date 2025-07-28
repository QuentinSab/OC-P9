from django.shortcuts import render, redirect, get_object_or_404
from reviews import forms
from reviews.utils import resize_image, get_user_posts

from django.contrib.auth.decorators import login_required
from authentication.models import User
from reviews.models import Ticket, Review, UserFollows, UserBlocks


@login_required
def feed(request):
    posts = get_user_posts(request.user, include_followed=True)
    return render(request, "reviews/home.html", {"posts": posts})


@login_required
def post(request):
    posts = get_user_posts(request.user, include_followed=False)
    return render(request, "reviews/post.html", {"posts": posts})


@login_required
def create_ticket(request):
    form = forms.TicketForm()

    if request.method == "POST":
        form = forms.TicketForm(request.POST, request.FILES)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user

            image = form.cleaned_data.get("image")
            if image:
                ticket.image = resize_image(image)

            ticket.save()
            return redirect("home")

    return render(request, "reviews/create_ticket.html", context={"form": form})


@login_required
def create_review(request, ticket_id):
    form = forms.ReviewForm()

    if request.method == "POST":
        form = forms.ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = get_object_or_404(Ticket, id=ticket_id)
            review.save()
            return redirect("home")

    return render(request, "reviews/create_review.html", context={"form": form}, )


@login_required
def create_ticket_and_review(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()

    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)

        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)

            image = ticket_form.cleaned_data.get("image")
            if image:
                ticket.image = resize_image(image)

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
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    if request.method == "POST":
        form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect("post")
    else:
        form = forms.TicketForm(instance=ticket)

    return render(request, "reviews/edit_post.html", {"form": form})


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    if request.method == "POST":
        ticket.delete()
        return redirect("post")

    return render(request, "reviews/delete_post.html", {"ticket": ticket})


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == "POST":
        form = forms.ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("post")
    else:
        form = forms.ReviewForm(instance=review)

    return render(request, "reviews/edit_post.html", {"form": form})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == "POST":
        review.delete()
        return redirect("post")

    return render(request, "reviews/delete_post.html", {"review": review})


@login_required
def follow(request):
    if request.method == "POST":
        form = forms.FollowForm(request.POST, user=request.user)

        if form.is_valid():
            form.save()
            return redirect("follow")
    else:
        form = forms.FollowForm(user=request.user)

    following = UserFollows.objects.filter(user=request.user)
    followers = UserFollows.objects.filter(followed_user=request.user)
    blocked_user = UserBlocks.objects.filter(user=request.user)

    return render(request, "reviews/follow.html", {
        "form": form,
        "following": following,
        "followers": followers,
        "blocked_user": blocked_user
    })


@login_required
def unfollow(request, followed_user_id):
    relation = get_object_or_404(UserFollows, user=request.user, followed_user_id=followed_user_id)
    relation.delete()

    return redirect("follow")


@login_required
def block_user(request, following_user_id):
    if request.method == "POST":
        blocked_user = get_object_or_404(User, id=following_user_id)
        UserBlocks.objects.get_or_create(user=request.user, blocked_user=blocked_user)
        UserFollows.objects.filter(user=blocked_user, followed_user=request.user).delete()

    return redirect("follow")


@login_required
def unblock_user(request, blocked_user_id):
    if request.method == "POST":
        block_relation = get_object_or_404(UserBlocks, user=request.user, blocked_user_id=blocked_user_id)
        block_relation.delete()

        # blocked_user = get_object_or_404(User, id=blocked_user_id)
        # UserFollows.objects.get_or_create(user=blocked_user, followed_user=request.user)

    return redirect("follow")
