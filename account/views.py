from django.shortcuts import render , get_object_or_404, redirect
from .models import *
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
import datetime
from django.utils.timezone import utc
from django.contrib.auth.models import Group, User
from main.models import *
# Create your views here.

@login_required(login_url = '/login/')
def home(request):
    usr = request.user.username
    remaining = []

    teachers = Group.objects.get(name="teacher").user_set.all()
    students = Group.objects.get(name="student").user_set.all()

    if request.user.is_superuser:
        return render(request, 'front/home.html')
    elif request.user in students:
        userType = 'student'
        try:
            std = StudentProfile.objects.get(user=usr)
            revset = ReviewSet.objects.filter(semester=std.year_semester)

            for i in revset:
                if usr not in i.given:
                    remaining.append(i)

            return render(request, 'front/home.html',{'revset':revset,'remaining':remaining,'userType':userType})
        except:
            revset = []
            return render(request, 'front/home.html',{'revset':revset,'remaining':remaining,'userType':userType})
    elif request.user in teachers:
        userType = 'teacher'
        teachername = Teacher.objects.get(name=request.user.username)
        revset = ReviewSet.objects.filter(teacher=teachername)
        total = len(revset)
        for i in revset:
            totalquestion = i.question.all()
            totalquestion = len(totalquestion)
            totalpoint = int(i.totalpoint)
            avg = (totalpoint*100)/(totalquestion*5)
            print(avg)
            remaining.append(avg)
        return render(request, 'front/home.html',{'revset':revset, 'remaining':remaining,'userType':userType,'total':total})


    return render(request, 'front/home.html',{ 'remaining':remaining})

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')

                messages.success(request, 'Account was created for ' + username)
                print(user)

                f = request.POST.get('type')

                if f == 'student':
                    b = StudentProfile(user = user)

                    b.save()
                    group = Group.objects.get(name="student")
                    user.groups.add(group)
                if f == 'teacher':

                    b = Teacher(name = user)
                    b.save()
                    group = Group.objects.get(name="teacher")
                    user.groups.add(group)

                return redirect('login')

        context = {'form': form}
        return render(request , 'front/register.html', context)
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username, password = password)

            if user is not None:
                login(request, user)
                if request.user.is_staff:
                    return redirect('dashboard')
                return redirect('home')
            else:
                messages.info(request, 'Username or password is incorrect')
        context = {}
        return render(request , 'front/login.html', context)

@login_required(login_url = '/login/')
def logoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url = '/login/')
def dashboard(request):

    return render(request, 'back/dashboard.html')
