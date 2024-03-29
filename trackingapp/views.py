from django.shortcuts import render, redirect
from .decorators import unauthenticated_user
from django.contrib.auth import login, logout, authenticate
from trackingproject import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *

# Create your views here.
def home(request):
    return render(request, 'trackingapp/home.html')


def about(request):
    return render(request, 'trackingapp/about.html')


@unauthenticated_user
def loginpage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = authenticate(request, email = email, password = password)
            login(request,user)
            return redirect('user-form')

        except:
            messages.error(request, 'Email or Password is invalid!!!')

    return render(request,'trackingapp/signin.html')


def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)    
        return redirect('home')
    
    return redirect('loginuser')


@unauthenticated_user
def registeruser(request):
    form = SignUpForm()

    try:
        if request.method == 'POST':
            form = SignUpForm(request.POST)

            if form.is_valid:                
                user = form.save(commit = False)
                subject = 'Welcome to trackingapp!!!'
                mesg = f'Hi {user.username}, thank you for registering!!!'
                host_email = settings.EMAIL_HOST_USER
                user_email_list = [user.email,]
                send_mail(subject, mesg, host_email, user_email_list)
                form.save()
                messages.success(request, f'Hi {user.username}, thank you for registering!!!')
                return redirect('loginuser')

    except:
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        all_users_username = MyUser.objects.all().values('username')
        all_users_email = MyUser.objects.all().values('email')

        if {'username' : username} in all_users_username:
            messages.error(request, f'User with username "{username}" already exists!!!')

        elif {'email' : email} in all_users_email:
            messages.error(request, 'User with this email id already exists!!!')    

        elif password1 != password2:
            messages.error(request ,'Password and Confirm Password are not matching with each other!!!')

        else:
            messages.error(request ,'Something went wrong,try again!!!')    

        return redirect('registeruser')

    context={'form' : form}
    return render(request, 'trackingapp/signup.html', context)


@login_required(login_url = 'loginuser')
def userform(request):
    u = request.user

    if len(Userprofile.objects.filter(user = u.id)) > 0:
        return redirect('dashboard')

    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST)

        if form.is_valid():
            f = form.save(commit = False)
            profile = Userprofile( 
                user = u,
                height = f.height,
                weight = f.weight,
                age = f.age,
                gender = f.gender
            )

            profile.save()
            return redirect('home')

    context = {'form' : form}
    return render(request, 'trackingapp/userform.html', context)


@login_required(login_url = 'loginuser')
def dashboard(request):
    return render(request, 'trackingapp/dashboard.html')


@login_required(login_url = 'loginuser')
def dashboard_activitiytracker(request):
    user = request.user
    p = Userprofile.objects.filter(user = user)
    if len(p) == 0:
        return redirect('user-form')

    if request.method == 'POST':
        activity_name = request.POST.get('type')
        duration = int(request.POST.get('duration'))
        met = float(request.POST.get('met'))
        age = user.userprofile.age
        calorie = (met*3.5*age)/200*duration/60

        form = Activity(
            user = user.userprofile,
            name = activity_name, 
            duration = duration,
            met = met,
            calorie = calorie
        )

        form.save()

    activities = Activity.objects.filter(user = user.userprofile)
    context = {'activities' : activities}
    return render(request, 'trackingapp/dashboard_activitytracker.html', context)


@login_required(login_url = 'loginuser')
def dashboard_foodtracker(request):
    user = request.user

    if request.method == 'POST':
        food_item = request.POST.get('food-item')
        amount = request.POST.get('serving-size')
        protein = float(request.POST.get('protein')) 
        fat = float(request.POST.get('fat'))
        carbohydrates = float(request.POST.get('carbohydrates'))
        calorie = 4 * (carbohydrates + protein) + 9 * fat 

        form = Food( 
            user = user.userprofile, 
            food = food_item, 
            amount = amount, 
            protein = protein, 
            fat = fat,
            carbohydrates = carbohydrates,
            calorie = calorie
        )

        form.save()

    food = Food.objects.filter(user = user.userprofile)
    context = {'food' : food}
    return render(request, 'trackingapp/dashboard_foodtracker.html', context)


@login_required(login_url = 'loginuser')
def userprofile(request):
    user = request.user
    p = Userprofile.objects.filter(user = user)
    if len(p) == 0:
        return redirect('user-form')
    
    return render(request, 'trackingapp/userprofile.html', {'u' : user})


@login_required(login_url = 'loginuser')
def updateprofile(request):
    user = request.user
    p = Userprofile.objects.filter(user = user)
    if len(p) == 0:
        return redirect('user-form')

    u = Userprofile.objects.get(id = user.userprofile.id)
    form = ProfileForm(instance = u)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance = u)

        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'trackingapp/userform.html', {'form' : form})