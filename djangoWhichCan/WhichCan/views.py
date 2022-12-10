from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
import json

# Create your views here.
def index(request):
    dustbin_color = 'dustbins.jpg'
    context = {"dustbin_color":dustbin_color}
    return render(request,'WhichCan/index.html',context)

def about(request):
    return render(request,'WhichCan/about.html')

def findDustbin(request):
    dustbin_color = None
    btn_clicked = "clicked"
    wet = request.POST.get("wet") if request.POST.get("wet") else ""
    dry = request.POST.get("dry") if request.POST.get("dry") else ""
    biomedical = request.POST.get("biomedical") if request.POST.get("biomedical") else ""
    recyclable = request.POST.get("recyclable") if request.POST.get("recyclable") else ""
    biodegradable = request.POST.get("biodegradable") if request.POST.get("biodegradable") else ""
    non_biodegradable = request.POST.get("non_biodegradable") if request.POST.get("non_biodegradable") else ""
    
    if (wet == "" and dry == "" and biomedical == "" and recyclable == "" and biodegradable == "" and non_biodegradable == ""):
        dustbin_color = 'dustbins.jpg'
        messages.warning(request, "Please select atleast three options to find exact dustbin. Thank you for using WhichBin.")
        context = {"dustbin_color":dustbin_color, "btn_clicked":btn_clicked}
        return render(request, 'WhichCan/index.html', context)

    if non_biodegradable == "non_biodegradable" and biodegradable == "biodegradable":
        dustbin_color = 'dustbins.jpg'
        messages.warning(request, "Please reselect the options, because there is no biodegradable and non biodegradable waste together. Thank you for using WhichBin.")
        context = {"dustbin_color":dustbin_color, "btn_clicked":btn_clicked}
        return render(request, 'WhichCan/index.html', context)

    if (wet == "wet" or dry == "dry" or recyclable == "recyclable") and (biodegradable != "biodegradable" and biomedical != "biomedical" and non_biodegradable != "non_biodegradable"):
        dustbin_color = 'green_bin.jpg'
        if recyclable != "recyclable" and biodegradable != "biodegradable":
            messages.warning(request, "Please select some more options to find exact dustbin or throw your waste in green dustbin if it not contain plastic or biomedical properties. Thank you for using WhichBin.")
        else:
            messages.success(request,"Please throw your waste in Green dustbin. Thank you for using WhichBin.")
        context = {"dustbin_color":dustbin_color, "btn_clicked":btn_clicked}
        return render(request, 'WhichCan/index.html', context)
    
    if  (biodegradable == "biodegradable" and biomedical != "biomedical") or (dry == "dry" or wet == "wet") and (non_biodegradable != "non_biodegradable"):
        dustbin_color = 'blue_bin.jpg'
        messages.success(request, "Please throw your waste in Blue dustbin. Thank you for using WhichBin.")
        context = {"dustbin_color":dustbin_color, "btn_clicked":btn_clicked}
        return render(request, 'WhichCan/index.html', context)
    
    if  biomedical == "biomedical" or (wet == "wet" or dry == "dry") or non_biodegradable == "non_biodegradable":
        dustbin_color = 'red_bin.jpg'
        messages.success(request, "Please throw your waste in Red dustbin. Thank you for using WhichBin.")
        context = {"dustbin_color":dustbin_color, "btn_clicked":btn_clicked}
        return render(request, 'WhichCan/index.html', context)
    
    
    context = {"dustbin_color":dustbin_color,"btn_clicked":btn_clicked}
    return render(request, 'WhichCan/index.html', context)