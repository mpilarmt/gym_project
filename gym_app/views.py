from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registre completat amb èxit!')
            return redirect('home')
        else:
            messages.error(request, 'Error en el registre. Si us plau, corregeix els errors.')
    else:
        form = UserRegistrationForm()
    return render(request, 'gym_app/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Has iniciat sessió correctament!')
                return redirect('home')
            else:
                messages.error(request, 'Email o contrasenya incorrectes.')
    else:
        form = UserLoginForm()
    return render(request, 'gym_app/login.html', {'form': form})

@login_required
def home(request):
    return render(request, 'gym_app/home.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'El teu perfil s\'ha actualitzat correctament!')
            return redirect('profile_edit')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'gym_app/profile_edit.html', {
        'form': form,
        'active_tab': 'profile'  # Per marcar la pestanya activa al menú
    })

def index(request):
    return render(request, 'gym_app/index.html')