from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404


franchises = [
    {
        'id': 1,
        'name': 'FitZone Gym',
        'industry': 'Fitness & Health',
        'desc': 'Modern fitness center with state-of-the-art equipment.',
        'investment': '₱450k+ Investment',
        'location': 'Suburban',
        'established': 'Est 2015',
        'rating': '4.9 ★',
    },
    {
        'id': 2,
        'name': 'Foodies Express',
        'industry': 'Food & Beverage',
        'desc': 'Popular fast food franchise with nationwide reach.',
        'investment': '₱750k+ Investment',
        'location': 'Metro',
        'established': 'Est 2018',
        'rating': '4.8 ★',
    },
    {
        'id': 3,
        'name': 'TechGuru Repair',
        'industry': 'Technology Services',
        'desc': 'Quick and reliable electronics repair services.',
        'investment': '₱300k+ Investment',
        'location': 'Metro',
        'established': 'Est 2016',
        'rating': '4.6 ★',
    },
    {
        'id': 4,
        'name': 'Green Thumb Nursery',
        'industry': 'Agriculture & Gardening',
        'desc': 'Organic plant nursery with a wide variety of plants.',
        'investment': '₱400k+ Investment',
        'location': 'Suburban',
        'established': 'Est 2014',
        'rating': '4.7 ★',
    },
    {
        'id': 5,
        'name': 'Spark Cleaners',
        'industry': 'Cleaning Services',
        'desc': 'Eco-friendly cleaning franchise for homes and offices.',
        'investment': '₱350k+ Investment',
        'location': 'Metro',
        'established': 'Est 2017',
        'rating': '4.5 ★',
    },
    {
        'id': 6,
        'name': 'PetPals Grooming',
        'industry': 'Pet Care',
        'desc': 'Professional pet grooming for dogs and cats.',
        'investment': '₱250k+ Investment',
        'location': 'Suburban',
        'established': 'Est 2019',
        'rating': '4.6 ★',
    },
    {
        'id': 7,
        'name': 'BookNest',
        'industry': 'Retail',
        'desc': 'Cozy bookstore cafe with community events.',
        'investment': '₱500k+ Investment',
        'location': 'Metro',
        'established': 'Est 2013',
        'rating': '4.8 ★',
    },
    {
        'id': 8,
        'name': 'QuickBites',
        'industry': 'Food & Beverage',
        'desc': 'Fast service snack bars with a modern twist.',
        'investment': '₱600k+ Investment',
        'location': 'Suburban',
        'established': 'Est 2016',
        'rating': '4.7 ★',
    }
]

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        user.save()

        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')

    return render(request, 'accounts/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('home')  # This should map to your homepage view
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

def home_view(request):
    return render(request, 'accounts/home.html')

def browse(request):
    return render(request, 'accounts/browse.html', {'franchises': franchises})

def get_franchise_by_id(franchise_id):
    # franchises list defined here or imported
    return next((f for f in franchises if f['id'] == franchise_id), None)

def franchise_detail(request, franchise_id):
    franchise = get_franchise_by_id(franchise_id)
    if not franchise:
        raise Http404("Franchise not found")
    if request.GET.get('ajax') == '1':
        return render(request, 'accounts/franchise_detail_modal.html', {'franchise': franchise})
    else:
        return render(request, 'accounts/franchise_detail_full.html', {'franchise': franchise})

def franchise_inquiry(request):
    if request.method == "POST":
        # process form input, e.g. save to DB, send email, etc.
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        location = request.POST.get("location")
        experience_level = request.POST.get("experience_level")
        comments = request.POST.get("comments")
        subscribe = bool(request.POST.get("subscribe"))
        agree_terms = bool(request.POST.get("agree_terms"))
        # [store or process the inquiry here]
        return HttpResponse("Thank you for your inquiry! We will contact you soon.")
    return redirect('site-home')