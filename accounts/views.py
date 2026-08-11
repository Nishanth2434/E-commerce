from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        full_name = request.POST.get('full_name')
        
        if password != confirm_password:
            return render(request, 'registration/register.html', {'error': 'Passwords do not match'})
            
        if User.objects.filter(username=username).exists():
            return render(request, 'registration/register.html', {'error': 'Username already exists'})
            
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = full_name
        user.save()
        
        Profile.objects.create(user=user)
        login(request, user)
        return redirect('products:home')
        
    return render(request, 'registration/register.html')

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        request.user.first_name = request.POST.get('full_name')
        request.user.email = request.POST.get('email')
        request.user.save()
        
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.city = request.POST.get('city')
        profile.save()
        
        return redirect('accounts:profile')
        
    return render(request, 'accounts/profile.html', {'profile': profile})
