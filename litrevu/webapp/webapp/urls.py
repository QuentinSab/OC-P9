from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

import reviews.views
import authentication.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', authentication.views.login_page, name="login"),
    path('logout/', authentication.views.logout_user, name="logout"),
    path('signup/', authentication.views.signup_page, name="signup"),
    path('home/', reviews.views.home, name='home'),
    path('create_ticket/', reviews.views.create_ticket, name='create_ticket'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
