from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import *    
import bcrypt

# HOME *************************************************

def index(request):
    return render(request, 'userdash/index.html')

# SIGN-IN PAGE ******************************************

def signin(request):
    return render(request, 'userdash/signin.html')

# REGISTRATION PAGE ******************************************

def register(request):
    return render(request, 'userdash/register.html')

# REGISTRATION VALIDATION AND RECORDING ***********************

def register_val(request):
     if request.method == "POST":
        #hashes password for storage to the Db        
        hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt(13))
        request.session['fname'] = request.POST['fname']
        errors = User.objects.name_validator(request.POST)
        if errors is not None:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('reg')
        errors = User.objects.email_validator(request.POST)
        if errors is not None:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('reg')
        errors = User.objects.db_validator(request.POST)
        if errors is not None:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('reg')
        errors = User.objects.pw_validator(request.POST)
        if errors is not None:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('reg')
        else:
            #creates a new validated record in database for new user
            user = User.objects.create(first_name=request.session['fname'], last_name=request.POST['lname'], email=request.POST['email'], password=hashed_password, level=request.POST['level'])
            #sets permission indicator
            if request.session['id'] != 1:
                    request.session['level'] = 0
                    #sets logged in user for use later
                    request.session['id'] = user.id
            #redirects to success to display sucessful login
            return redirect('dash')

# SIGNIN VALIDATION *************************************************

def signin_val(request):
    if request.method == "POST":
        errors = User.objects.email_validator(request.POST)
        if errors is not None:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('sign')
        errors = User.objects.dbcheck_validator(request.POST)
        if errors is not None:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('sign')
        errors = User.objects.hpw_validator(request.POST)
        if errors is not None:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('sign')
        else:
            #sets logged in user id for use later
            user = User.objects.get(email=request.POST['email'])
            request.session['id'] = user.id
            #sets First name for user interaction
            request.session['fname'] = user.first_name
            #sets permission indicator
            if user.level == "admin":
                request.session['level'] = 1
            else:
                request.session['level'] = 0
            #redirects to success to display sucessful login
            return redirect('dash')

# DASHBOARD - USER AND ADMIN *************************************************

def dashboard(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, 'userdash/dashboard.html', context)

# EDIT - ADMIN *************************************************

def edit(request, id):
    context = {
        'user': User.objects.get(id=id)
    }
    return render(request, 'userdash/dashboard/edit.html', context)

# EDIT - USER *************************************************

def profile(request):
    context = {
        'user': User.objects.get(id=request.session['id'])
    }
    return render(request, 'userdash/users/profile.html', context)

# NEW - ADMIN *************************************************

def new(request):
    return render(request, 'userdash/users/new.html')

# SHOW - USER AND ADMIN *************************************************

def show(request, id):
    this_user = User.objects.get(id=id)
    context = {
        'user': this_user,
        'user_posts': this_user.posts.all().select_related('user'),
        'comments': Comment.objects.all()
    }
    return render(request, 'userdash/users/show.html', context)

# UPDATE - USER INFO *************************************************

def update(request):
    if request.method == "POST":
        errors = User.objects.email_validator(request.POST)
        if errors is not None:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('profile')
        errors = User.objects.name_validator(request.POST)
        if errors is not None:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('profile')
        errors = User.objects.db_validator(request.POST)
        if errors is not None:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('profile')
        else:
            #Updates validated record in database for user profile
            update_info = User.objects.get(id=request.POST['id'])
            update_info.first_name = request.POST['fname']
            update_info.last_name = request.POST['lname']
            update_info.email = request.POST['email']
            update_info.level = request.POST['level']
            update_info.save()
            #redirects to success to display sucessful login
            return redirect('dash')

# UPDATE - PROFILE DESCRIPTION *************************************************

def save(request):
    if request.method == "POST":
            #Updates description in database for user profile
            update_info = User.objects.get(id=request.POST['id'])
            update_info.desc = request.POST['desc']
            update_info.save()
            #redirects to dashboard
            return redirect('dash')

# CHANGE PASSWORD *************************************************

def change(request):
    if request.method == "POST":
        errors = User.objects.pw_validator(request.POST)
        if errors is not None:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('profile')
        else:
            hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt(13))
            #Updates validated password in database for user profile
            change_pw = User.objects.get(id=request.POST['id'])
            change_pw.password = hashed_password
            change_pw.save()
            #redirects to success to display sucessful login
            return redirect('dash')

# DESTROY USER - ADMIN *************************************************

def destroy(request, id):
    destroyit = User.objects.get(id=id)
    destroyit.delete()
    # TO BE ADDED LATER -- DELETING POSTS AND COMMENTS SENT TO THE USER AND NOT POST AND COMMENTS TO OTHER USERS
    return redirect('dash')

# LOGOFF *************************************************

def logoff(request):
    request.session['id'] = 0
    request.session['fname'] = ''
    return redirect('/')

# POST MESSAGE *************************************************

def post_msg(request):
    if request.method == "POST":
        profile_id = request.POST['id']
        errors = User.objects.msg_validator(request.POST)
        if errors is not None:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('ushow', profile_id)
        else:
            userid = request.session['id']
            a1 = Post.objects.create(message=request.POST['post'], user=User.objects.get(id=userid))
            a1.users.add(profile_id)
            a1.save()
            return redirect('ushow', profile_id)

# POST COMMENT *************************************************

def post_cmt(request):
    if request.method == "POST":
        profile_id = request.POST['id']
        errors = User.objects.msg_validator(request.POST)
        if errors is not None:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('ushow', profile_id)
        else:
            userid = request.session['id']
            b1 = Comment.objects.create(comment=request.POST['post'], user=User.objects.get(id=userid), post_id=request.POST['message_id'])
            return redirect('ushow', profile_id)
