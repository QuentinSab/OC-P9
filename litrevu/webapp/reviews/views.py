from django.shortcuts import render, redirect
from reviews import forms

from django.contrib.auth.decorators import login_required


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
