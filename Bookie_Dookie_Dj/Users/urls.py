
from django.urls import path
from . import views
from Users.views import SignUp, Login

urlpatterns = [
path('login/', Login.as_view(), name='login'),
path('signup/', views.SignUp.as_view(), name='signup'),
]