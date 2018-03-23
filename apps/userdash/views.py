from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from time import gmtime, strftime
from .models import User    
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# HOME *************************************************

def index(request):
    return render(request, 'userdash/index.html')

# REGISTRATION *************************************************

def register(request):
    if request.method == "POST":
        #grabs record if email exists in the Db
        reg_check = User.objects.filter(email=request.POST['regemail'])
        #hashes password for storage to the Db        
        hashed_password = bcrypt.hashpw(request.POST['regpassword'].encode(), bcrypt.gensalt(13))

        request.session['fname'] = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['regemail']
        password = request.POST['regpassword']
        password2 = request.POST['regpassword2']
    
        # Checks name fields
        if len(request.session['fname']) < 2 or len(lname) < 2:
            messages.warning(request, "Name must be longer.")
            return redirect('reg')
        elif not str(request.session['fname']).isalpha():
            messages.warning(request, "First Name can only be letters.")
            return redirect('reg')       
        elif not str(lname).isalpha():
            messages.warning(request, "Last Name can only be letters.")
            return redirect('reg')
      
        # Validates email address for proper format.
        if len(email) < 1:
            messages.warning(request, "Email cannot be blank!")
            return redirect('reg')
        elif not EMAIL_REGEX.match(email):
            messages.warning(request, "Invalid Email Address!")
            return redirect('reg')
        elif len(reg_check) != 0:
            messages.warning(request, "Duplicate address, please enter another one or try logging in!")
            return redirect('reg')
        
        # Check password length and matching confirmation
        if len(password) < 8:
            messages.warning(request, "Password is not long enough!")
            return redirect('reg')
        elif password != password2:
            messages.warning(request, "Passwords do not match!")
            return redirect('reg')
        password = ''
        password2 = ''

        request.session['from'] = 0
        #creates a new validated record in database for new user
        User.objects.create(first_name=request.session['fname'], last_name=lname, email=email, password=hashed_password)
        #sets logged in user for use later
        request.session['id'] = User.objects.last().id
        request.session['from'] = 0
        #redirects to success to display sucessful login
    return redirect('dash')

# SIGNIN *************************************************

def signin(request):
    if request.method == "POST":
        #Checks Db for log email address. If not there returns empty list
        log_email = request.POST['logemail']
        log_check = User.objects.filter(email=log_email)
        
        # Validates email address for proper format.
        if len(log_email) < 1:
            messages.warning(request, "Email cannot be blank!")
            return redirect('/')
        elif not EMAIL_REGEX.match(log_email):
            messages.warning(request, "Invalid Email Address!")
            return redirect('/')
        elif len(log_check) == 0:
            messages.warning(request, "Email not found!")
            return redirect('/')

        log_pass = User.objects.get(email=log_email).password

        #password validation - compares hashed logged in password to hashed Db password
        if not bcrypt.checkpw(request.POST['logpassword'].encode(), log_pass.encode()):
            messages.warning(request, "Password does not match.")
            return redirect('/')

        #sets logged in user id for use later  
        request.session['id'] = User.objects.get(email=log_email).id
        #sets First name for user interaction
        request.session['fname'] = User.objects.get(email=log_email).first_name
        #sets login or registration indicator
        request.session['from'] = 1
        #redirects to success to display sucessful login
    return redirect('dash')

# SUCCESSFUL LOGIN OR REGISTRATION *************************************************

def success(request):
    if request.session['from'] == 1:
        messages.success(request, "Welcome Back {}!  You have successfully logged in!".format(request.session['fname']))
    else:
        messages.success(request, "Welcome {}!  You have successfully registered on our site!".format(request.session['fname']))
    return render(request, 'logreg/success.html')
