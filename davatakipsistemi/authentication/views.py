from django.shortcuts import render

def login_request(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        print(username,password)
    return render(request, 'authentication/login.html')

def logout_request(request):
    return render(request, 'authentication/login.html')

# Create your views here.
