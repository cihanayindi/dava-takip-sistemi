from django.shortcuts import render

def show_work_list(request):
    return render(request, "worklist/work_list.html")

# Create your views here.
