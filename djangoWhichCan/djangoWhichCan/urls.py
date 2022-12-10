from django.contrib import admin
from django.urls import path, include

admin.site.site_header="WhichCan Admin"
admin.site.site_title="WhichCan Admin Panel"
admin.site.index_title="Welcome to WhichCan Admin Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('WhichCan.urls')),
]
