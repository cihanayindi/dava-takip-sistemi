from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail

def send_test_email():
    send_mail(
        'Test Email',
        'This is a test email sent from Django.',
        'davatakippaneli@gmail.com',  # Gönderen e-posta adresi
        ['suakbenli@gmail.com'],  # Alıcı e-posta adresi
        fail_silently=False,
    )
    
    
    
def login_request(request):
    # if request.user.is_authenticated:
    #     return redirect("/")
    send_test_email()
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(request, "account/login.html")

    return render(request, "account/login.html")

def register_request(request):
    pass
    """if request.user.is_authenticated:
        return redirect("home")
        
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]

        if password == repassword:
            if User.objects.filter(username=username).exists():
                return render(request, "account/register.html", 
                {
                    "error":"username kullanılıyor.",
                    "username":username,
                    "email":email,
                    "firstname": firstname,
                    "lastname":lastname
                })
            else:
                if User.objects.filter(email=email).exists():
                    return render(request, "account/register.html", 
                    {
                        "error":"email kullanılıyor.",
                        "username":username,
                        "email":email,
                        "firstname": firstname,
                        "lastname":lastname
                    })
                else:
                    user = User.objects.create_user(username=username,email=email,first_name=firstname,last_name=lastname,password=password)
                    user.save()
                    return redirect("login")                    
        else:
            return render(request, "account/register.html", {
                "error":"parola eşleşmiyor.",
                "username":username,
                "email":email,
                "firstname": firstname,
                "lastname":lastname
            })

    return render(request, "account/register.html")"""

def logout_request(request):
    logout(request)
    return redirect("home")