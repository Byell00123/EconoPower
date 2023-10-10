from django.shortcuts import render
# from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,'home.html')

# def home1(request):
#     return render(request,'home1.html')

# @login_required
# def home2(request):
#     return render(request,'home2.html')