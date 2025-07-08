from django.shortcuts import render, redirect, get_object_or_404
from reviews import forms

from django.contrib.auth.decorators import login_required
from reviews.models import Ticket


@login_required
def home(request):
    return render(request, "reviews/home.html")


@login_required
def create_ticket(request):
    form = forms.TicketForm()

    if request.method == "POST":
        form = forms.TicketForm(request.POST, request.FILES)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
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
