from django.urls import path
from . import views
urlpatterns = [
    path('', views.toLogin_view),
    path('login_status/', views.Login_view),
    path("type_in_dest/", views.type_in_dest_view)
]
