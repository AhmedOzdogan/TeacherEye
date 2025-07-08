from pyexpat.errors import messages
from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from core.models import User, CustomUserManager, UserSession


import logging
logging.basicConfig(level=logging.INFO)

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

def blog(request):
    return render(request, 'core/blog.html')

def features(request):
    return render(request, 'core/features.html')

def login_view(request):
    if request.method == 'POST':
        # Handle login logic here
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me') == 'on'
        
        logging.info(f"Login attempt for email: {email}, Remember Me: {remember_me}")
        
        # For now, just print the values to the console
        user = authenticate(request, email=email, password=password)

        if user is not None:
            logging.info(f"User {email} authenticated successfully.")

            if user.email_verified is False: #type: ignore
                return render(request, 'core/login.html', {'message': f'{email} has not been verified yet.'})
            
            if user.blocked:  # type: ignore
                return render(request, 'core/login.html', {'message': f'{email} is blocked. Please contact support.'})
            
            if user.is_active is False:  # type: ignore
                return render(request, 'core/login.html', {'message': f'{email} is inactive. Please reset your password.'})
                        # ✅ Actually log the user in
            
            login(request, user)

            # # ✅ Optional: set session to expire on browser close
            # if not remember_me:
            #     request.session.set_expiry(0)
                
            # # ✅ Create a session for the user
            # if not request.session.session_key:
            #     request.session.create()
                
            # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            # if x_forwarded_for:
            #     ip = x_forwarded_for.split(',')[0].strip()
            # else:
            #     ip = request.META.get('REMOTE_ADDR', '')

            # UserSession.objects.create(
            #     user=user,
            #     user_agent=request.META.get('HTTP_USER_AGENT', ''),
            #     ip_address=ip,
            #     session_key=request.session.session_key
            # )
            
            # logging.info(f"User {email} logged in successfully with session key {request.session.session_key}.")
                
            # ✅ Redirect to appropriate dashboard
            if user.role == 'teacher': # type: ignore
                return redirect('dashboard_teachers')  # type: ignore
            elif user.role == 'manager': # type: ignore
                return redirect('dashboard_managers')  # type: ignore
            elif user.role == 'admin': # type: ignore
                logging.info(f"User {email} has admin access.")
                return redirect('dashboard_admins')  # type: ignore
            


        else:
            logging.warning(f"Failed login attempt for {email}.")
            return render(request, 'core/login.html', {'message': 'Invalid email or password.'})

    return render(request, 'core/login.html')

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_Confirm')
        terms = request.POST.get('terms') == 'on'

        if password != password_confirm:
            return render(request, 'core/register.html', {'message': 'Passwords do not match.'})

        # Optional: check if email already exists
        if User.objects.filter(email=email).exists():
            return render(request, 'core/register.html', {'message': 'Email already registered. Please log in or reset your password.'})

        user = User.objects.create_user(email=email, password=password) # type: ignore
        user.save()
        return redirect('login')  # or wherever you want to send them next

    return render(request, 'core/register.html')

def reset_password_view(request):
    return render(request, 'core/reset_password.html')