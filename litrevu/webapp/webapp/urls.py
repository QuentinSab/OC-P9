from django.contrib import admin
from django.urls import path

import reviews.views
import authentication.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', authentication.views.login_page, name="login"),
    path('logout/', authentication.views.logout_user, name="logout"),
    path('signup/', authentication.views.signup_page, name="signup"),
    path('home/', reviews.views.home, name='home'),
]
