from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
def index(request):
    dustbin_color = 'dustbins.jpg'
    context = {"dustbin_color":dustbin_color}
    print("context", context)
    return render(request,'WhichCan/index.html',context)

def about(request):
    return render(request,'WhichCan/about.html')

def findDustbin(request):
    dustbin_color = None
    message = None
    wet = request.POST.get("wet") if request.POST.get("wet") else ""
    dry = request.POST.get("dry") if request.POST.get("dry") else ""
    biomedical = request.POST.get("biomedical") if request.POST.get("biomedical") else ""
    recyclable = request.POST.get("recyclable") if request.POST.get("recyclable") else ""
    biodegradable = request.POST.get("biodegradable") if request.POST.get("biodegradable") else ""
    non_biodegradable = request.POST.get("non_biodegradable") if request.POST.get("non_biodegradable") else ""
    if non_biodegradable == "non_biodegradable":
        dustbin_color = 'red_bin.jpg'

    context = {"dustbin_color":dustbin_color, "message":message}
    messages.success(request, "Your comment has been posted successfully")
    return render(request, 'WhichCan/index.html', context)
