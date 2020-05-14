from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.index, name="p_Home"),
    path('signin/',views.signin, name="p_Signin"),
    path('signup/',views.signup, name="p_Signup"),
    path('plogout/',views.plogout,name='plogout'),
    path('about/',views.about, name="p_about"),
    path('consultation/',views.consultation, name="p_consultation"),
    path('dashboard/',views.dashboard, name="p_Dashboard"),
    path('profile/',views.profile, name="p_patientProfile"),
    path('p_editprofile/',views.p_edit, name='p_edit'),
    path('search_doctor/',views.search_doctor, name="p_searchdoctor"),
    # path('srch_doctor/<slug:typeofdoc>',views.srch_doctor, name="p_srchdoctor"),
    path('appointment_doc/<int:pk>/',views.appointment_doc, name="appointment_doc"),
    path('treatment/',views.treatment, name="p_Treatment"),
    path('payment/',views.payment, name='p_payment'),
    path('p_appointment/',views.p_appointment, name='p_appointment'),
    path('p_chatting_req/<int:pk>/',views.p_chatting_req, name='p_chatting_req'),
    path('p_chatting/<int:pk>/',views.p_chatting, name='p_chatting'),
    path('p_print_consultation/<int:pk>/',views.p_print_consultation,name='p_print_consultation'),

    path('handlerequest/', views.handlerequest, name='HandleRequest'),
    path('makepayment/<int:pk>', views.makepayment, name='makepayment'),

    path('list/',views.PatientListView.as_view(), name='list'),
    path('patient/<int:pk>', views.PatientDetails.as_view(),name='patient_details'),
    path('patientProfile/',views.PatientProfile.as_view(), name='patient_profile'),





    
    # path('post', views.Post, name='post'),
    # path('messages', views.Messages, name='messages')

]
