from django.urls import path
from accounts import views

urlpatterns = [
    path("register/",views.ResgisterationAPIView.as_view(),name="registeration"),
    # path("login/",views.ResgisterationAPIView.as_view(),name="registeration"),
    # path("token/refresh/",views.ResgisterationAPIView.as_view(),name="registeration"),
]
