from django.shortcuts import render
from davatakipsistemi.backends.user_authenticate import custom_authenticate

def login_request(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        if custom_authenticate(username, password):
            pass # burada kullanıcı o an hangi sayfadan geldiyse 
                # oraya ya da anasayfaya yönlendirilecek
        else:
            return render(request, "authentication/login.html", {
                "error" : "Kullanıcı adı ya da parola yanlış!"})

    return render(request, 'authentication/login.html')

def logout_request(request):
    return render(request, 'authentication/login.html')

# Create your views here.
