from django.db import models
from django import forms

class customer(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(primary_key=True)
    passwd = models.CharField(max_length=25)
    doj = models.DateTimeField()
    class Meta:
        ordering =('-doj',)

    def __str__(self):
        return self.email

class seller(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(primary_key=True)
    passwd = models.CharField(max_length=25)
    doj = models.DateTimeField()
    class Meta:
        ordering =('-doj',)

    def __str__(self):
        return self.email

class product(models.Model):
    product_name = models.CharField(max_length=50)
    product_id = models.IntegerField(primary_key=True)
    picture = models.FileField(upload_to='images/')
    price = models.IntegerField()
    description = models.TextField(max_length=2500)
    male_category = models.BooleanField(default=False)
    female_category = models.BooleanField(default=False)
    product_seller = models.ForeignKey(seller, on_delete=models.CASCADE)
    doa = models.DateTimeField()
    class Meta:
        ordering = ('doa',)
    def __str__(self):
        return str(self.product_id)

class cart(models.Model):
    user = models.ForeignKey(customer, on_delete=models.CASCADE)
    prod = models.ForeignKey(product, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.name

class user_signupForm(forms.ModelForm):
    name = models.CharField(max_length=50)
    email = models.EmailField(primary_key=True)
    passwd = models.CharField(max_length=25)
    class Meta:
        model = customer
        exclude = ('doj',)

class seller_signupForm(forms.ModelForm):
    name = models.CharField(max_length=50)
    email = models.EmailField(primary_key=True)
    passwd = models.CharField(max_length=25)
    class Meta:
        model = seller
        exclude = ('doj',)

class loginForm(forms.Form):
    email = forms.EmailField()
    passwd = forms.CharField(widget=forms.PasswordInput)

class productForm(forms.ModelForm):
    name = models.CharField(max_length=50)
    id = models.IntegerField(primary_key=True)
    picture = models.FileField(upload_to='images/')
    price = models.IntegerField()
    description = models.TextField()
    male_category = models.BooleanField(default=False)
    female_category = models.BooleanField(default=False)
    product_seller = models.ForeignKey(seller, on_delete=models.CASCADE)

    class Meta:
        model = product
        exclude = ('product_seller','doa',)

