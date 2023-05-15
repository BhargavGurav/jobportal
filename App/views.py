from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.decorators.cache import cache_control
from .models import *
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.conf import settings

# Create your views here.

def home(request):
    feeds = Feedback.objects.all()
    jobs = list(Job_Post.objects.all())
    today = datetime.now().strftime("%Y-%m-%d")
    today = datetime.date(datetime.strptime(today, "%Y-%m-%d"))
    # print(type(today))
    # print((int(str(today)[8:])%30))
    # print(int(str(jobs[1].upto)[8:])%30)
    for i in jobs:
        # if abs((int(str(today)[8:])%30) - (int(str(i.upto)[8:])%30)) >= 5:
        if today - i.upto >= timedelta(5): 
            print(i.post)
            i.delete()

    # print(today)
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        password = request.POST.get('password')


        if len(password) < 8:
            messages.error(request, 'Password must be 8 character long.')
            return HttpResponseRedirect('/')

        if not any(x.isdigit() for x in password):
            messages.error(request, 'Password must contain at least one digit.')
            return HttpResponseRedirect('/')

        if not any(x.islower() for x in password):
            messages.error(request, 'Password must contain at least one small letter.')
            return HttpResponseRedirect('/')

        if not any(x.isupper() for x in password):
            messages.error(request, 'Password must contain at least one capital letter.')
            return HttpResponseRedirect('/')

        else:
            usr = User.objects.create_user(username=email, email=email, password=password)
            usr.first_name = fname
            usr.last_name = lname
            usr.save()

            user = Job_Seeker(user=usr, phone=mobile)
            user.save()
            messages.success(request, 'Candidate Registered successfully.')
            return HttpResponseRedirect('/')


    return render(request, 'home.html', {'jobs' : jobs, 'feedbacks' : feeds, 'today' : today})


def registerRecruiter(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        cname = request.POST.get('cname')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        password = request.POST.get('password')


        if len(password) < 8:
            messages.error(request, 'Password must be 8 character long.')
            return HttpResponseRedirect('/')

        if not any(x.isdigit() for x in password):
            messages.error(request, 'Password must contain at least one digit.')
            return HttpResponseRedirect('/')

        if not any(x.islower() for x in password):
            messages.error(request, 'Password must contain at least one small letter.')
            return HttpResponseRedirect('/')

        if not any(x.isupper() for x in password):
            messages.error(request, 'Password must contain at least one capital letter.')
            return HttpResponseRedirect('/')

        else:
            usr = User.objects.create_user(username=email, email=email, password=password)
            usr.first_name = fname
            usr.last_name = lname
            usr.is_staff = True
            usr.save()

            user = Recruiter(user=usr, phone=mobile, company=cname)
            user.save()
            messages.success(request, 'Recruiter Registered successfully.')
            return HttpResponseRedirect('/')
    return render(request, 'registerRecruiter.html')


@cache_control(no_cache=True, must_revalidade=True, no_store=True)
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        # print(username, password)
        
        if User.objects.filter(username=username):  
            usr = authenticate(username=username, password=password)
            if usr:
                login(request, usr)
                messages.success(request, 'Login successful.')
                return HttpResponseRedirect('/')
            else:
                messages.error(request, 'Wrong username or password.')
                return HttpResponseRedirect('loginUser')
        else:
            messages.error(request, 'No user found.')
            return HttpResponseRedirect('/')

@login_required(login_url='loginUser')
@cache_control(no_cache=True, must_revalidade=True, no_store=True)
def profile(request):
    applied = 0
    appliers = []
    applied_list = []
    
    if Job_Seeker.objects.filter(user=request.user):
        user_detaile = Job_Seeker.objects.get(user=request.user)
        applied = len(AppliedPost.objects.filter(applied_by=user_detaile))
        applied_list = list(AppliedPost.objects.filter(applied_by=user_detaile))
    elif Recruiter.objects.filter(user=request.user):
        user_detaile = Recruiter.objects.get(user=request.user)

        for i in AppliedPost.objects.all():
            if i.job.user == user_detaile:
                appliers.append(Job_Seeker.objects.get(user=i.applied_by.user))
                
    return render(request, 'profile.html', {'userDetail' : user_detaile, 'applied': applied, 'applied_to' : applied_list, 'appliers' : appliers})

@cache_control(no_cache=True, must_revalidade=True, no_store=True)
def logoutuser(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return HttpResponseRedirect('/')

def apply(request, job_id):
    post = Job_Post.objects.get(id=job_id)
    applier = Job_Seeker.objects.get(user=request.user)

    if AppliedPost.objects.filter(applied_by=applier):
        for i in AppliedPost.objects.filter(applied_by=applier):
            if i.job == post:
                messages.error(request, 'Already applied')
                return HttpResponseRedirect('/')

    
    job_obj = AppliedPost(applied_by=applier, job=post, applied_on=datetime.now())
    job_obj.save()
        
    from_mail = settings.EMAIL_HOST_USER
    to_mail = [request.user.email]
    try:
        send_mail('About apply to job', f'You have applied for the Post of {post.post} on JobPortal.com . Congrats! you will here from recruiter soon.', from_mail, to_mail)
    except:
        print('Email not found.')
    messages.success(request, 'Congrats Applied successfully.')
    return HttpResponseRedirect('/')

@login_required(login_url='loginUser')
def addPost(request):
    if request.method == 'POST':
        user = Recruiter.objects.get(user=request.user)
        post = request.POST.get('post')
        salary = int(request.POST.get('salary'))
        description = request.POST.get('description')
        posted_on = datetime.now()
        upto = request.POST.get('upto')

        job_obj = Job_Post(user=user, post=post, salary=salary, description=description, posted_on=posted_on, upto=upto)
        job_obj.save()
        messages.success(request, 'Posted Successfully.')
        return HttpResponseRedirect('/')

def feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        feedback = request.POST.get('feedback')

        feedback_obj = Feedback(name=name, email=email, feedback=feedback)
        feedback_obj.save()
        messages.success(request, 'Thanks for feedback !')
        return HttpResponseRedirect('/')

def about(request):
    return render(request, 'aboutus.html')

def searched(request):
    feeds = Feedback.objects.all()
    today = datetime.now().strftime("%Y-%m-%d")

    if request.method == 'POST':
        searchType = request.POST.get('query')

        matched = list()
        for i in Job_Post.objects.all():
            if (str(searchType).lower()) in str(i.post).lower():
                matched.append(i)
        if len(matched) == 0:
            
            messages.error(request, 'No job till now.')
            return HttpResponseRedirect('/')
        else:
            return render(request, 'home.html', {'jobs' : matched, 'feedbacks' : feeds, 'today' : today})