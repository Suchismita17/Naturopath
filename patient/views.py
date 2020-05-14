from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView, UpdateView
from requests import request
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.http import HttpResponse , JsonResponse
from .models import Patient, Appointment,Chat
from doctor.models import Doctor, Consultation
from django.contrib.auth.decorators import login_required
import datetime

from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum

MERCHANT_KEY = 'Fxbv21vqPsSdO5R6'

# Create your views here.



class PatientListView(ListView):
    model = Patient
    template_name = 'patient/PatientList.html'


class PatientDetails(DetailView):
    model = Patient
    template_name = 'patient/PatientDetails.html'
    context_object_name = 'simple'

class PatientProfile(UpdateView):
    model = Patient
    template_name = 'patient/PatientProfile.html'
    fields = ['name','address','pin','mobile_no']



def search_doctor(request):
    doctor=Doctor.objects.all()
    consultation=Consultation.objects.all()
    arg={'doctor':doctor,'consultation':consultation}
    return render(request, 'patient/p_search_doctor.html',arg)




def index(request):

    return render(request,'patient/p_index.html')

def plogout(request):
    auth.logout(request)
    return render(request,'patient/p_index.html')


def signin(request):
    if request.method == 'POST':

        username =  request.POST.get('username')
        password =  request.POST.get('password')

        user = auth.authenticate(username=username,password=password)



        if user is not None :

            try:
                if (user.patient.Is_patient == True ) :
                    auth.login(request,user)

                    # request.session['patientusername'] = user.username

                    return redirect(index)
                else:
                    return HttpResponse ("else part")

            except :
                messages.info(request,'INVALID USERNAME OR PASSWORD')
                return redirect(signin)


        else :
            messages.info(request,'INVALID USERNAME OR PASSWORD')
            return redirect(signin)


    else :
        return render(request,'patient/p_signin.html')








    
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
        image = request.POST.get('image')
        password = request.POST.get('password')
        password1 = request.POST.get('confpassword')


        if password == password1:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'User name already exists')
                    return redirect(signup)
                    # return HttpResponse('id exists')

                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'email already exists')
                    return redirect(signup)
                    # return HttpResponse('email exists')
                else:
                    user = User.objects.create_user(username=username, password=password, email=email)
                    user.save()

                    patientnew = Patient(user=user, name=name, dob=dob, address=address, mobile_no=mobile_no, gender=gender, pin=pin, image=image)
                    patientnew.save()
                    messages.info(request, 'User Created Successfully')
                    return redirect(signin)

            # return redirect('login')

    else:
        return render(request,'patient/p_signup.html')






@login_required
def p_edit(request):
    if request.method == 'POST':
        user=request.user
        name=request.POST.get('name')
        mobile_no = request.POST.get('mobile')
        address = request.POST.get('address')
        pin = request.POST.get('pin')
        image = request.POST.get('image')

        user.patient.name=name
        user.patient.mobile_no=mobile_no
        user.patient.address=address
        user.patient.pin=pin
        user.patient.image=image
        user.save()
        return render(request,'patient/p_profile.html')

    else :
        return render(request,'patient/p_edit.html')


    


@login_required
def profile(request):

        return render(request,'patient/p_profile.html')


@login_required
def dashboard(request):
    return render(request,'patient/p_dashboard.html')


@login_required
def consultation(request):
    return render(request,'patient/p_consultation.html')


def treatment(request):
    return render(request,'patient/p_treatment.html')

def about(request):
    return render(request,'patient/p_about.html')


@login_required
def payment(request):
    return render(request, 'patient/p_payment.html')



@login_required
def appointment_doc(request,pk):
    if request.method == 'POST':
        doc_id= pk
        pat_id= request.user.patient.pk
        conobj=Consultation.objects.get(pk=pk)

        appointment_status= False
        payment_status = False
        tm = conobj.time
        appdate = request.POST.get('appdate')
        reason = request.POST.get('reason')
        print('appdate:',appdate)
        print(type(appdate))

        new_appointment=Appointment( doc_id=doc_id, pat_id=pat_id, appointment_status=appointment_status, payment_status=payment_status, appdate=appdate, time=tm,  reason=reason)
        new_appointment.save()

        return redirect(index)
  

    else:
        docobj= Doctor.objects.get(pk=pk)
        dconobj= Consultation.objects.get(pk=pk)
        

        date=[]
        dayname=[]
        today=datetime.datetime.now()

        nextday=today+datetime.timedelta(days=1)
        tday=nextday.strftime("%x")

        for i in range(1,7):
            nextday=today+datetime.timedelta(days=i)
            d=nextday.strftime('%x')
            n=nextday.strftime('%A')
            date.append(d)
            dayname.append(n)


        arg={'docobj':docobj, 'dconobj':dconobj, 'date':date, 'dayname':dayname,'tday':tday}

        return render(request, 'patient/p_choose_doc.html',arg)


@login_required
def p_appointment(request):
    objs=Appointment.objects.all()
    docobjs=Doctor.objects.all()
    arg={'objs':objs, 'docobjs':docobjs}
    return render(request, 'patient/p_appointment.html',arg)

@login_required
def p_chatting_req(request,pk):
    return render(request, 'patient/p_chatting_req.html')


@login_required
def p_chatting(request,pk):
    docobj= Doctor.objects.get(pk=pk)
    arg={'docobj':docobj}
    return render(request, 'patient/p_chatting.html',arg)




#==========================================================================
    
def post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)

        consultation_id = request.session['consultation_id'] 
        consultation_obj = consultation.objects.get(id=consultation_id)

        c = Chat(consultation_id=consultation_obj,sender=request.user, message=msg)

        #msg = c.user.username+": "+msg

        if msg != '':            
            c.save()
            print("msg saved"+ msg )
            return JsonResponse({ 'msg': msg })
            
    else:
        return HttpResponse('Request must be POST.')



def messages2(request):
   if request.method == "GET":

         consultation_id = request.session['consultation_id'] 

         c = Chat.objects.filter(consultation_id=consultation_id)
         return render(request, 'consultation/chat_body.html', {'chat': c})


#==========================================================



@login_required
def p_print_consultation(request,pk):
    appobj=Appointment.objects.get(pk=pk)
    docobj= Doctor.objects.get(pk=appobj.doc_id)
    dconobj= Consultation.objects.get(pk=appobj.doc_id)
    arg={'docobj':docobj, 'dconobj':dconobj, 'appobj':appobj }
    print(appobj.appdate)
    print(appobj.pk)

    return render(request, 'patient/p_print_consultation.html',arg)



@login_required
def makepayment(request,pk):
    appobj=Appointment.objects.get(pk=pk)
    docappobj=Consultation.objects.get(pk=appobj.doc_id)
    user=request.user


    param_dict = {

                'MID': 'fnAdst51355811627397',
                'ORDER_ID': str(appobj.pk),
                'TXN_AMOUNT': str(docappobj.fees),
                'CUST_ID': user.email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/patient/handlerequest/',
        }
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
    return render(request,'patient/paytm.html', {'param_dict': param_dict})



@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('Payment successful')
            appobj=Appointment.objects.get(pk=response_dict['ORDERID'])
            appobj.txnid=response_dict['TXNID']
            appobj.payment_status=True
            appobj.save()


        else:
            print('Payment was not successful because' + response_dict['RESPMSG'])
    return render(request, 'patient/paymentstatus.html', {'response': response_dict})