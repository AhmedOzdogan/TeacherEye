from pyexpat.errors import messages
from django.shortcuts import render, redirect


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
        
        # For now, just print the values to the console
        logging.info(email)
        logging.info(password)
        if remember_me == True:
            logging.info("Remember me is checked")
        else:
            logging.info("Remember me is not checked")
        
        return render(request, 'core/login.html', {'message': 'Login successful!'})
        
    return render(request, 'core/login.html')

def register_view(request):
    if request.method == 'POST':
        # Handle registration logic here
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_Confirm')  # Changed from 'password_again' to 'password_Confirm'
        terms = request.POST.get('terms') == 'on'
        
        # For now, just print the values to the console
        logging.info(first_name)
        logging.info(last_name)
        logging.info(email)
        logging.info(password)
        logging.info(password_confirm)
        logging.info(f"Terms accepted: {terms}")
        
        if password != password_confirm:
            return render(request, 'core/register.html', {'message': 'Passwords do not match.'})
            
        return redirect('register')
    return render(request, 'core/register.html')