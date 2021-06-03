from django.shortcuts import render

def my_home(request):
    return render(request, 'home.html')

def about_me(request):
    return render(request, 'about_me.html')