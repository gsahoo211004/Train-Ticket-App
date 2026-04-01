from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm
from .models import Profile
from wallet.models import Wallet

def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        Profile.objects.create(user=user)
        Wallet.objects.create(user=user)
        messages.success(request, "Account created! Please login.")
        return redirect('login')
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user:
            login(request, user)
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'accounts/dashboard.html')

from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Save user fields
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()

            # Check if KYC-sensitive fields changed
            p = form.save(commit=False)
            if 'id_proof' in request.FILES or 'address_proof' in request.FILES:
                p.kyc_verified = False
                p.kyc_pending = True
            p.save()

            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })

    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')

from .decorators import admin_required
from django.contrib.auth.models import User

@admin_required
def admin_dashboard_view(request):
    all_users = User.objects.all().select_related('profile')
    return render(request, 'accounts/admin_dashboard.html', {'all_users': all_users})

@admin_required
def approve_kyc_view(request, user_id):
    try:
        profile = Profile.objects.get(user__id=user_id)
        profile.kyc_verified = True
        profile.kyc_pending = False
        profile.save()
        messages.success(request, f"KYC approved for {profile.user.username}.")
    except Profile.DoesNotExist:
        messages.error(request, "User not found.")
    return redirect('admin_dashboard')