from django.shortcuts import render,redirect
from .models import Patient, Doctor, Appoitment
from django.contrib.auth.models import User,Group
from django.contrib.auth import login,authenticate,logout
from django.http import HttpResponse
from django.utils import timezone
# Create your views here.
def homepage(request):
    return render(request, 'index.html')

def aboutpage(request):
    return render(request, 'about.html')

def loginpage(request):
    error=""
    if request.method == 'POST':
        u = request.POST['email']
        p = request.POST['password']

        user = authenticate(request,username=u,password=p)
        try:
            if user is not None:
                error="no"
                login(request,user)
                g = request.user.groups.all()[0].name
                if g == 'Patient':
                    d = {'error':error}
                    return render(request,'patienthome.html',d)
                elif g == 'Doctor':
                    d ={'error':error}
                    return render(request,'doctorhome.html',d)
        except Exception as e:
            print(e)

    return render(request, 'login.html')

def createaccountpage(request):
    user = "none"
    error = ""
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        password = request.POST['password']
        repeatpassword = request.POST['repeatpassword']
        email = request.POST['email']
        telephone = request.POST['telephone']
        address = request.POST['address']
        gender = request.POST['gender']
        birthday = request.POST['birthday']

    
        if password == repeatpassword:
            Patient.objects.create(name=name,surname=surname,email=email,telephone=telephone,address=address,birthday=birthday,gender=gender)
            user = User.objects.create_user(first_name=name,email=email,password=password,username=email)
            pat_group = Group.objects.get(name='Patient')
            pat_group.user_set.add(user)
            user.save()
            error = "no"
        else:
            error = "yes"
  
    d = {'error' : error}

    return render(request, 'createaccount.html', d)

def Logout(request):
    logout(request)
    return redirect('loginpage')

def Home(request):
    if not request.user.is_active:
        return redirect('loginpage')

    g = request.user.groups.all()[0].name
    if g == 'Patient':
        return render(request,'patienthome.html')
    if g == 'Doctor':
        return render(request,'doctorhome.html')

def profile(request):
    if not request.user.is_active:
        return redirect('loginpage')
    
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        patient_details = Patient.objects.all().filter(email=request.user)
        d = {'patient_details':patient_details}
        return render(request,'pateintprofile.html',d)
    if g == 'Doctor':
        doctor_details = Doctor.objects.all().filter(email=request.user)
        d = {'doctor_details':doctor_details}
        return render(request,'doctorprofile.html',d)

def MakeAppoitments(request):
    if not request.user.is_active:
        return redirect('loginpage')
    error=""
    alldoctors = Doctor.objects.all()
    d = {'alldoctors' : alldoctors}

    if request.method == 'POST':
        temp = request.POST['doctoremail']
        doctoremail = temp.split()[0]
        doctorname = temp.split()[1]
        patientname = request.POST['patientname']
        patientemail = request.POST['patientemail']
        appoitmentdate = request.POST['appoitmentdate']
        appoitmenttime = request.POST['appoitmenttime']
        symptoms = request.POST['symptoms']
        try:
            Appoitment.objects.create(doctorname=doctorname,doctoremail=doctoremail,patientname=patientname,patientemail=patientemail,appoitmentdate=appoitmentdate,appoitmenttime=appoitmenttime,symptoms=symptoms,status=True,exam="")
            error='no'
        except Exception as e:
            error='yes'
        e={'error':error}
        return render(request,'pateintmakeappointments.html',e)
    


    return render(request,'pateintmakeappointments.html',d)

def viewappoitments(request):
    if not request.user.is_active:
        return redirect('loginpage')

    g = request.user.groups.all()[0].name
    if g == 'Patient':
        upcomming_appoitments = Appoitment.objects.filter(patientemail=request.user,appoitmentdate__gte=timezone.now(),status=True).order_by('appoitmentdate')
        previous_appoitments = Appoitment.objects.filter(patientemail=request.user,appoitmentdate__lt=timezone.now()).order_by('-appoitmentdate') | Appoitment.objects.filter(patientemail=request.user,status=False).order_by('-appoitmentdate')
        d = {'upcomming_appoitments':upcomming_appoitments,'previous_appoitments':previous_appoitments}
        return render(request,'patientviewappointments.html',d)
    if g == 'Doctor':
        if request.method == 'POST':
            examdata = request.POST['exam']
            idvalue = request.POST['idof']
            Appoitment.objects.filter(id=idvalue).update(exam=examdata,status=False)
        upcomming_appoitments = Appoitment.objects.filter(doctoremail=request.user,appoitmentdate__gte=timezone.now(),status=True).order_by('appoitmentdate')
        previous_appoitments = Appoitment.objects.filter(doctoremail=request.user,appoitmentdate__lt=timezone.now()).order_by('-appoitmentdate') | Appoitment.objects.filter(doctoremail=request.user,status=False).order_by('-appoitmentdate')
        d = {'upcomming_appoitments':upcomming_appoitments,'previous_appoitments':previous_appoitments}
        return render(request,'doctorviewappointment.html',d)
    

