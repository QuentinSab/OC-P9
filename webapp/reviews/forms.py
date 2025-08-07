from django import forms

from authentication.models import User
from reviews.models import Ticket, Review, UserFollow


class TicketForm(forms.ModelForm):
    # Form for creating or editing a Ticket
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'image')
        labels = {'title': 'Titre'}

    def clean_image(self):
        # Validates that the uploaded image is not larger than 2MB
        image = self.cleaned_data.get('image')
        if image and image.size > 2 * 1024 * 1024:
            raise forms.ValidationError("L'image ne doit pas dépasser 2 Mo.")
        return image


class ReviewForm(forms.ModelForm):
    # Form for creating or editing a Review
    class Meta:
        model = Review
        fields = ('rating', 'headline', 'body')


class FollowForm(forms.Form):
    # Form to follow another user by username
    followed_user = forms.CharField(label="Nom d'utilisateur")

    def __init__(self, *args, user=None, **kwargs):
        # Initialize the form and store the current user for validation
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_followed_user(self):
        # Check that the user exists, is not self, and is not already followed
        username = self.cleaned_data["followed_user"]

        existing_users = User.objects.filter(username=username)
        if not existing_users.exists():
            raise forms.ValidationError("Cet utilisateur n'existe pas.")

        self.followed_user = existing_users.first()

        if self.followed_user.id == self.user.id:
            raise forms.ValidationError("Vous ne pouvez pas vous suivre vous-même.")

        if UserFollow.objects.filter(user=self.user, followed_user=self.followed_user).exists():
            raise forms.ValidationError("Vous suivez déjà cet utilisateur.")

        return username

    def save(self):
        return UserFollow.objects.create(user=self.user, followed_user=self.followed_user)
