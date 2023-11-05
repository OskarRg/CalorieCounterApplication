from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm, ProfileUpdateForm, PasswordChangeForm, DeactivateUserForm, ProfileImageUpdateForm
from .models import Profile


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'You registered as {username}. You can log in now')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required()
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            messages.success(request, f'You changed your measurements')
            return redirect(profile)
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'users/profile.html', {'form': form})


@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password has been changed.')
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/password_change.html', {'form': form})


@login_required()
def deactivate_account(request):
    if request.method == 'POST':
        form = DeactivateUserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = request.user
            if user.check_password(password):
                profile = Profile.objects.get(user=user)
                profile.deactivate_user()
                logout(request)
                return redirect('food_counter-home')  # Możesz ustawić inny adres po deaktywacji konta
            else:
                form.add_error('password', 'Incorrect password')
    else:
        form = DeactivateUserForm()

    return render(request, 'users/deactivate_account.html', {'form': form})


@login_required
def change_profile_image(request):
    if request.method == 'POST':
        form = ProfileImageUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileImageUpdateForm(instance=request.user.profile)
    return render(request, 'users/change_profile_image.html', {'form': form})