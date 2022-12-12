from django.shortcuts import render, redirect
from django.contrib import messages
from django.http.response import HttpResponseNotFound, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.urls import reverse
from django.conf import settings

from WhichCan.models import Contact, Donate

# Create your views here.
def index(request):
    dustbin_color = 'dustbins.jpg'
    context = {"dustbin_color":dustbin_color}
    return render(request,'WhichCan/index.html',context)

def about(request):
    return render(request,'WhichCan/about.html')

def donate(request):
    context = {"stripe_publishable_key":settings.STRIPE_PUBLISHABLE_KEY}
    return render(request,'WhichCan/donate.html',context)

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


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        description = request.POST.get("description")
        contact_us = Contact.objects.create(name=name, email=email, description=description)
        messages.success(request,"Your query has been submitted successfully. You will get reply within 1-2 day(s). Team WhichBin")
        return render(request, "WhichCan/contact.html",{"btn_submit":"clicked"})
    else:
        return render(request, "WhichCan/contact.html",{"btn_submit":""})

def paymentSuccess(request):
    session_id = request.GET.get('session_id')
    if session_id is None:
        return HttpResponseNotFound()

    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.retrieve(session_id)

    donate = Donate.objects.filter(stripe_payment_intent=session_id).first()
    donate.stripe_payment_intent = session.payment_intent
    donate.has_paid = True
    donate.save()
    messages.success(request,"Thank you for donating. We appreciate your contribution, Team WhichBin")
    return redirect("/")

def paymentFailed(request):
    messages.warning(request,"Your payment was cancelled. If in case amount is deducted from your account please click on contact us. Team WhichBin")
    return redirect("/")


@csrf_exempt
def create_checkout_session(request):

    request_data = json.loads(request.body)
    email = request_data["email"]
    amount = request_data["amount"]
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        customer_email = request_data['email'],
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                    'name': email,
                    },
                    'unit_amount': int(amount)*100,
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success')) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('failed')),
    )

    donate = Donate.objects.create(email=email, amount=amount, stripe_payment_intent=checkout_session.id)

    return JsonResponse({'sessionId': checkout_session.id})