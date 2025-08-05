from django import forms

from authentication.models import User
from reviews.models import Ticket, Review, UserFollow, UserBlock


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'image')
        labels = {'title': 'Titre'}


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'headline', 'body')


class FollowForm(forms.Form):
    followed_user = forms.CharField(label="Nom d'utilisateur")

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_followed_user(self):
        username = self.cleaned_data["followed_user"]

        existing_users = User.objects.filter(username=username)
        if not existing_users.exists():
            raise forms.ValidationError("Cet utilisateur n'existe pas.")

        self.followed_user = existing_users.first()

        if self.followed_user.id == self.user.id:
            raise forms.ValidationError("Vous ne pouvez pas vous suivre vous-même.")

        if UserFollow.objects.filter(user=self.user, followed_user=self.followed_user).exists():
            raise forms.ValidationError("Vous suivez déjà cet utilisateur.")

        if UserBlock.objects.filter(user=self.followed_user, blocked_user=self.user).exists():
            raise forms.ValidationError("Vous ne pouvez pas suivre cet utilisateur car il vous a bloqué.")

        return username

    def save(self):
        return UserFollow.objects.create(user=self.user, followed_user=self.followed_user)
