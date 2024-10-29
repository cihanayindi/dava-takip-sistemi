from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from davatakipsistemi.backends.user_authenticate import custom_authenticate

def login_request(request):
    # GET isteğinde `next` parametresi varsa oturuma kaydedilir
    if request.method == 'GET':
        next_url = request.GET.get('next', '/')
        request.session['next_url'] = next_url  # Oturumda saklanır
        print(request.session['next_url'])

    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        if custom_authenticate(username, password):
            # Oturumdan `next_url` değeri alınır
            next_url = request.session.get('next_url', '/')
            print(next_url)
            return redirect(next_url)  # Başarılı giriş sonrası `next_url`e yönlendir
        else:
            # Hatalı girişte `next_url` değeri tekrar sayfaya gönderilir
            return render(request, "authentication/login.html", {
                "error": "Kullanıcı adı ya da parola yanlış!",
                "next": request.session.get('next_url', '/')
            })

    return render(request, 'authentication/login.html', {"next": request.session.get('next_url', '/')})

def logout_request(request):
    return render(request, 'authentication/login.html')

# Create your views here.
