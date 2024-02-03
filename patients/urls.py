from django.urls import path
from patients import views
urlpatterns = [
    path("",views.PatientProfileListCreateAPIView.as_view(),name="profiles_list"),
    path("profile/",views.PatientRetrieveUpdateAPIView.as_view(),name="patient_profile_update"),
    path("send/user/token/<int:id>/",views.SendUserToken.as_view(),name="send_token"),
]
