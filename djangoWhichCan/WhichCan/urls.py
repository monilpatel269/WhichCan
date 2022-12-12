from django.urls import path, include
from WhichCan.views import *
from WhichCan import views

urlpatterns = [
    path('',views.index, name="Index"),
    path('about/',views.about, name="About"),
    path('contact/',views.contact, name="Contact"),
    path('donate/',views.donate, name="donate"),
    path('findDustbin/',views.findDustbin, name="findDustbin"),
    path('api/checkout-session/', create_checkout_session, name='api_checkout_session'),
    path('success/', views.paymentSuccess, name='success'),
    path('failed/', views.paymentFailed, name='failed'),
]
