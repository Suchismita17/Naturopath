from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name="d_Home"),
    path('signin/',views.signin, name="d_Signin"),
    path('signup/',views.signup, name="d_Signup"),
    path('logout/',views.logout,name='logout'),
    path('about/',views.about, name="d_about"),
    path('consultation/',views.consultation, name="d_consultation"),
    path('dashboard/',views.dashboard, name="d_Dashboard"),
    path('profile/',views.profile, name="d_Profile"),
    path('notification/',views.notification, name="d_Notification"),
    path('treatment/',views.treatment, name="d_Treatment"),
    path('profile_edit/',views.d_profile_edit, name='d_profile_edit'),
    path('d_appointment/',views.d_appointment, name='d_appointment'),
    path('d_app_accept/<int:pk>',views.d_app_accept, name='d_app_accept'),
    path('d_app_reject/<int:pk>',views.d_app_reject, name='d_app_reject'),
    path('d_consult_details_edit/',views.d_consult_details_edit, name='d_consult_details_edit'),

]