from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from apps.users.models import CustomUser
from django.contrib import messages

def sign_in(request):

    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        remember_me = request.POST.get('remember_me')

        user = authenticate(request, username=username, password=password)
        if user:

            login(request, user)
            messages.success(request, 'Tizimga muvaffaqiyatli kirdingiz')
            
            # Sessiya muddati
            if remember_me:
                request.session.set_expiry(7200)  # 2 soat
            else:
                request.session.set_expiry(1800)  # 30 daqiqa
            
            return redirect('home')
        
        messages.error(request, 'Login yoki parol xato')
        return redirect('sign-in')
        
    context = {
        'page_title': 'Tizimga kirish'
    }

    return render(request, 'auth/sign-in.html', context)


def sign_up(request):

    if request.method == 'POST':
        
        full_name = request.POST.get('full_name').strip()
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        confirm_password = request.POST.get('confirm_password').strip()
        remember_me = request.POST.get('remember_me')

        if not full_name or not username or not password or not confirm_password:
            messages.error(request, "Barcha maydonlarni to'ldiring")
            return redirect('sign-up')
        
        if password != confirm_password:
            messages.error(request, "Parollar mos emas")
            return redirect('sign-up')
        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Bu foydalanuvchi nomi allaqachon mavjud.")
            return redirect('sign-up')
        
        user = CustomUser(full_name=full_name, username=username)
        user.set_password(password)
        user.save()

        messages.success(request, "Ro'yxatdan o'tish muoffaqiyatli amalga oshirildi")
        return redirect('sign-in')
    
    context = {
        'page_title': 'Ro\'yxatdan o\'tish'
    }

    return render(request, 'auth/sign-up.html', context)

def sign_out(request):
    logout(request)
    messages.success(request, 'Tizimdan muvaffaqiyatli chiqdingiz')
    return redirect('home')