from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Donate(models.Model):
    email = models.EmailField(verbose_name='Customer Email', null=True, blank=True)
    amount = models.FloatField(default=0,verbose_name='Amount')
    stripe_payment_intent = models.CharField(max_length=200, null=True, blank=True)
    has_paid = models.BooleanField(default=False,verbose_name='Payment Status')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
