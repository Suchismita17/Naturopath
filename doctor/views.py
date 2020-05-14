# Create your views here.
from django.shortcuts import render, redirect
from requests import request
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from . models import Doctor, ConsultDetails, Consultation
from patient.models import Patient, Appointment
from django.contrib.auth.decorators import login_required


def logout(request):
    auth.logout(request)
    # request.session.pop('patientid', None)
    # request.session.pop('doctorid', None)
    # request.session.pop('adminid', None)
    return render(request,'doctor/d_index.html')



def index(request):
    return render(request,'doctor/d_index.html')

def about(request):
    return render(request,'doctor/d_about.html')

def signin(request):
    if request.method == 'POST':

        username =  request.POST.get('username')
        password =  request.POST.get('password')

        user = auth.authenticate(username=username,password=password)



        if user is not None :
            try:
                if (user.doctor.Is_doctor == True ) :
                    auth.login(request,user)

                    request.session['doctorusername'] = user.username

                    return redirect(index)
                else:
                    return HttpResponse ("else part")

            except :
                messages.info(request,'Invalid USERNAME or PASSWORD')
                return redirect(signin)


        else :
            messages.info(request,'Invalid ID or PASSWORD')
            return redirect(signin)


    else :
        return render(request,'doctor/d_signin.html')



def signup(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        name = request.POST.get('name')
        dob = request.POST.get('dob')
        pin = request.POST.get('pin')
        address = request.POST.get('address')
        mobile_no = request.POST.get('mobile')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        specialist = request.POST.get('specialist')
        qualification = request.POST.get('qualification')
        language = request.POST.get('language')
        fees = request.POST.get('fees')
        time = request.POST.get('time')
        experience = request.POST.get('experience')
        password = request.POST.get('password')
        password1 = request.POST.get('confpassword')


        if password == password1:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'User name already exists')
                # return redirect('registration')
                return HttpResponse('id exists')

            elif User.objects.filter(email=email).exists():
                messages.info(request, 'email already exists')
                # return redirect('registration')
                return HttpResponse('email exists')
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()

                doctortnew = Doctor(user=user, name=name, dob=dob, pin = pin, address=address,specialist = specialist,  mobile_no=mobile_no, gender=gender,qualification=qualification,language=language ,experience=experience )
                doctortnew.save()
                condetnew = Consultation(user=user, fees=fees, time=time)
                condetnew.save()
                messages.info(request, 'User Created Successfully')
                # return HttpResponse('data inputed successfully')
                return redirect(signin)

        # return redirect('login')

    else:
        return render(request,'doctor/d_signup.html')


@login_required
def profile(request):
    return render(request,'doctor/d_profile.html')


@login_required
def d_profile_edit(request):
    if request.method == 'POST':
        user=request.user
        name=request.POST.get('name')
        mobile_no = request.POST.get('mobile')
        address = request.POST.get('address')
        pin = request.POST.get('pin')

        user.doctor.name=name
        user.doctor.mobile_no=mobile_no
        user.doctor.address=address
        user.doctor.pin=pin
        user.save()
        return render(request,'doctor/d_profile.html')

    else :
        return render(request,'doctor/d_profile_edit.html')

@login_required
def d_consult_details_edit(request):
    if request.method == 'POST':
        user=request.user
        fees=request.POST.get('fees')
        time = request.POST.get('time')



        user.consultation.fees=fees
        user.consultation.time=time
        user.save()
        return render(request,'doctor/d_profile.html')

    else :
        return render(request,'doctor/d_consult_details.html')


@login_required
def dashboard(request):
    return render(request,'doctor/d_dashboard.html')

def consultation(request):
    return render(request,'doctor/d_consultaion.html')

def treatment(request):
    return render(request,'doctor/d_treatment.html')

def notification(request):
    return render(request,'doctor/d_notification.html')



@login_required
def d_appointment(request):
    objs=Appointment.objects.all()
    patobjs=Patient.objects.all()
    arg={'objs':objs, 'patobjs':patobjs}
    return render(request, 'doctor/d_appointment.html',arg)



@login_required
def d_app_accept(request,pk):
    objs=Appointment.objects.all()
    patobjs=Patient.objects.all()

    appointmentnew = Appointment.objects.get(pk=pk)
    appointmentnew.appointment_status = True
    appointmentnew.save()

    return redirect(d_appointment)




@login_required
def d_app_reject(request,pk):
    objs=Appointment.objects.all()
    patobjs=Patient.objects.all()

    appointmentnew = Appointment.objects.get(pk=pk)
    appointmentnew.reject_status = True
    appointmentnew.save()
    return redirect(d_appointment)