from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

import reviews.views
import authentication.views

urlpatterns = [
    path('', RedirectView.as_view(url='login/')),
    path('admin/', admin.site.urls),
    path('login/', authentication.views.login_page, name="login"),
    path('logout/', authentication.views.logout_user, name="logout"),
    path('signup/', authentication.views.signup_page, name="signup"),
    path('home/', reviews.views.home, name='home'),
    path('post/', reviews.views.post, name='post'),
    path('create_ticket/', reviews.views.create_ticket, name='create_ticket'),
    path('create_review/<int:ticket_id>/', reviews.views.create_review, name='create_review'),
    path('create_ticket_and_review/', reviews.views.create_ticket_and_review, name='create_ticket_and_review'),
    path('follow/', reviews.views.follow, name='follow'),
    path('unfollow/<int:followed_user_id>/', reviews.views.unfollow, name='unfollow'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
