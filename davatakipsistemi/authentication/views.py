from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from davatakipsistemi.backends.user_authenticate import custom_authenticate
from Client.models import CustomUsers
from django.contrib.auth import logout
import os
import binascii
import hashlib

def login_request(request):
    print(request.user.is_authenticated)
    # GET isteğinde `next` parametresi varsa oturuma kaydedilir
    if request.method == 'GET':
        next_url = request.GET.get('next', '/')
        request.session['next_url'] = next_url  # Oturumda saklanır
        print(request.session['next_url'])

    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        if custom_authenticate(username, password):
            print("Giriş başarılı!")  # Başarılı giriş
            # Oturumdan `next_url` değeri alınır
            next_url = request.session.get('next_url', '/')
            # Kullanıcı adını oturuma kaydet
            request.session['username'] = username  # Oturumda kullanıcı adı saklanır
            request.session['is_authenticated'] = True  # Kullanıcının kimliği doğrulandı olarak ayarlanır

            return redirect(next_url)  # Başarılı giriş sonrası `next_url`e yönlendir
        else:
            # Hatalı girişte `next_url` değeri tekrar sayfaya gönderilir
            return render(request, "authentication/login.html", {
                "error": "Kullanıcı adı ya da parola yanlış!",
                "next": request.session.get('next_url', '/')
            })

    return render(request, 'authentication/login.html', {"next": request.session.get('next_url', '/')})


def logout_request(request):
    logout(request)
    return render(request, 'authentication/login.html')

def create_admin(request):
    saltData = binascii.hexlify(os.urandom(15)).decode()
    password = "admin"
    hashed_password = hashlib.sha256((password + saltData).encode()).hexdigest()
    admin_user = {
        "username": "admin",
        "password": hashed_password,
        "salt" : saltData,
        "authority_level": 1
    }

    # Create a new user with the unpacked dictionary
    CustomUsers.objects.create(
        username=admin_user["username"],
        password=admin_user["password"],
        salt=admin_user["salt"],
        authority_level=admin_user["authority_level"]
    )

    return render(request, 'authentication/login.html')
# Create your views here.
