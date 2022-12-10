from django.urls import path, include
from WhichCan import views

urlpatterns = [
    path('',views.index, name="Index"),
    path('about/',views.about, name="About"),
    path('findDustbin/',views.findDustbin, name="findDustbin"),
]
