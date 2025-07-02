from django.contrib import admin

from authentication.models import User
from reviews.models import Ticket, Review, UserFollows


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "email")


class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "time_created")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("ticket", "headline", "user", "time_created")


class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ("user", "followed_user")


admin.site.register(User, UserAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserFollows, UserFollowsAdmin)
