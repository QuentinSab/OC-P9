from django.contrib import admin

from reviews.models import Ticket, Review, UserFollows, UserBlocks


class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "id", "time_created")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("headline", "user", "id", "ticket_title", "time_created")


class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ("user", "followed_user")


class UserBlocksAdmin(admin.ModelAdmin):
    list_display = ("user", "blocked_user")


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserFollows, UserFollowsAdmin)
admin.site.register(UserBlocks, UserBlocksAdmin)
