from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.core.mail import EmailMessage
# Create your views here.

def home(request):
    return render(request,'home.html')
# -------user signin function---------######
def signin(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Invalid username or password')
            return redirect('signin')
    else:
        return render(request,'signin.html')


####### User signup function--------########
@csrf_exempt
def signup(request):

    if request.method == 'POST':
        username=request.POST['username']
        first_name= request.POST['first_name']
        password= request.POST['password']
        cpassword = request.POST['cpassword']

        if len(password) < 8:
            messages.error(request,'Password should be atleast 8 character')
            return redirect('signup')
            
        if password==cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request,'Email already registered')
                return redirect('signup')
            else: 
                    user = User.objects.create_user(username=username,first_name=first_name,password=password)
                    user.is_active=False
                    user.save()
                    email_subject='Activate your account'
                    email_body='test'
                    email=EmailMessage(
                        email_subject,
                        email_body,
                        'sumanbhutiya123@gmail.com',
                        [username],
                        
                    )
                    email.send(fail_silently=False)
                    messages.info(request,'User Created')
                    return redirect('signin')
        else:        
            messages.error(request,'Password not matching')
            return redirect('signup')
        #return redirect('/')
    else:
      return render(request,'signup.html')

#######---------- logout function------------#####
def logout(request):
    auth.logout(request)
    return redirect('/')


########----- sending email---#######


