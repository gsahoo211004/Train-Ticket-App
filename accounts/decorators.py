from django.shortcuts import redirect
from django.contrib import messages

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
            messages.error(request, "Access denied. Admins only.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper