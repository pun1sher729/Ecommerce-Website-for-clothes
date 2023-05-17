from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponseRedirect
from datetime import datetime

def index(request):
    if request.method == 'GET':
        try:
            cur_email = request.session.get("email")
            if cur_email != None:
                login=1
            else:
                login=0
        except:
            request.session["email"] = None
            login=0
        if login==0:
            return render(request,'index.html', {'login':login, 'cur_email':cur_email})
        elif login==1 and 'seller' in request.session:
            if request.session['seller'] == True:
                return redirect("seller_home")
        else:
            return render(request,'index.html', {'login':login, 'cur_email':cur_email})

def user_login_view(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            email = cd.get("email")
            passwd = cd.get("passwd")
            check_if_user_exists = customer.objects.filter(email=email).exists()
            if check_if_user_exists:
                user = customer.objects.get(email=email)
                if passwd == user.passwd:
                    request.session["email"] = email
                    return redirect('index')
                else:
                    return render(request, 'user_login.html', {"op": "Wrong password"})
            else:
                return render(request, 'user_login.html', {"op": "Email not found"})
        else:
            error_string = ' '.join([' '.join(x for x in l) for l in list(form.errors.values())])
            return render(request, 'user_login.html', {"op": error_string})
    elif request.method == 'GET':
        return render(request,'user_login.html')

def logout(request):
    request.session['email'] = None
    return redirect("index")

def user_signup_view(request):
    if request.method == 'POST':
        form = user_signupForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post = form.save(commit=False)
            post.doj = datetime.now()
            post.save()
            return redirect('user_login_view')
        else:
            error_string = ' '.join([' '.join(x for x in l) for l in list(form.errors.values())])
            return render(request, 'user_signup.html', {"op": error_string})
    elif request.method=='GET':
        return render(request,'user_signup.html')

def seller_login_view(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            email = cd.get("email")
            passwd = cd.get("passwd")
            check_if_user_exists = seller.objects.filter(email=email).exists()
            if check_if_user_exists:
                user = seller.objects.get(email=email)
                if passwd == user.passwd:
                    request.session["email"] = email
                    request.session['seller'] = True
                    return redirect('seller_home')
                else:
                    return render(request, 'seller_login.html', {"op": "Wrong password"})
            else:
                return render(request, 'seller_login.html', {"op": "Email not found"})
        else:
            error_string = ' '.join([' '.join(x for x in l) for l in list(form.errors.values())])
            return render(request, 'seller_login.html', {"op": error_string})
    elif request.method == 'GET':
        return render(request,'seller_login.html')

def seller_logout(request):
    request.session['email'] = None
    request.session['seller'] = False
    return redirect("seller_login_view")

def seller_signup_view(request):
    if request.method == 'POST':
        form = seller_signupForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post = form.save(commit=False)
            post.doj = datetime.now()
            post.save()
            return redirect('seller_login_view')
        else:
            error_string = ' '.join([' '.join(x for x in l) for l in list(form.errors.values())])
            return render(request, 'seller_signup.html', {"op": error_string})
    elif request.method=='GET':
        return render(request,'seller_signup.html')

def add_product_view(request):
    if request.method == 'GET' and request.session['seller']==True:
        return render(request, "add_product.html",  {'login':1, 'cur_email':request.session['email']})
    elif request.method == 'POST' and request.session['seller']==True:
        form = productForm(request.POST, request.FILES)
        #print(request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
            cur_seller = seller.objects.get(email=request.session['email'])
            post = form.save(commit=False)
            post.product_seller = cur_seller
            post.doa = datetime.now()
            post.save()
        else:
            print(form.errors)
        return render(request, "add_product.html", {'login':1, 'cur_email':request.session['email']})

def male_category_view(request):
    if request.method == 'GET' and request.session['email'] != None:
        male_products = product.objects.filter(male_category=True)
        products = []
        for i in male_products:
            products.append(i)
        print(products)
        return render(request, "male_category.html", {'login':1,'cur_email':request.session['email'],'products':products})
    elif request.method == 'GET'  and request.session['email'] == None:
        male_products = product.objects.filter(male_category=True)
        products = []
        for i in male_products:
            products.append(i)
        print(products)
        return render(request, "male_category.html", {'login':0,'products':products})

def female_category_view(request):
    if request.method == 'GET' and request.session['email'] != None:
        female_products = product.objects.filter(female_category=True)
        products = []
        for i in female_products:
            products.append(i)
        print(products)
        return render(request, "female_category.html", {'login':1,'cur_email':request.session['email'],'products':products})
    elif request.method == 'GET'  and request.session['email'] == None:
        female_products = product.objects.filter(female_category=True)
        products = []
        for i in female_products:
            products.append(i)
        print(products)
        return render(request, "female_category.html", {'login':0,'products':products})

def add_to_cart_view(request):
    if request.method == 'POST' and request.session['email'] != None:
        if 'add' in request.POST:
            product_id = request.POST['add']
            prod = product.objects.get(product_id=product_id)
            user = customer.objects.get(email=request.session['email'])
            post = cart.objects.create(user=user, prod=prod)
            post.save()
        return redirect(request.META.get('HTTP_REFERER'))
    elif request.method == 'POST' and request.session['email'] == None:
        if 'add' in request.POST:
            return redirect('user_login_view')

def view_cart(request):
    if request.method == 'GET' and request.session['email'] != None:
        cur_user = customer.objects.get(email=request.session['email'])
        cart_items = cart.objects.filter(user=cur_user)
        products = []
        for item in cart_items:
            products.append(item.prod)
        print(products)
        return render(request, "view_cart.html", {'login':1,'cur_email':request.session['email'], 'products':products })
    elif request.method == 'POST' and request.session['email'] != None:
        if 'checkout' in request.POST:
            cur_user = customer.objects.get(email=request.session['email'])
            cart_items = cart.objects.filter(user=cur_user)
            total = 0
            products = []
            for item in cart_items:
                products.append(item.prod)
                total += item.prod.price
            print(total)
            return render(request, "view_cart.html", {'login':1,'cur_email':request.session['email'], 'products':products,'checkout_header': "Total", 'total':'₹'+str(total)})

def search(request):
    if request.method == 'POST':
        search_param = request.POST['Search']
        prods = product.objects.all()
        out = []
        for p in prods:
            if search_param in p.product_name:
                out.append(p)
        if request.session['email'] != None:
            return render(request, "search.html", {'login':1, 'cur_email':request.session['email'], "out":out, })
        else:
            return render(request, "search.html", {'login':0,'out':out})

def seller_home(request):
    if request.method == 'GET':
        if request.session['email'] and request.session['seller']== True:
            return render(request, "seller_home.html", {'login':1, 'cur_email':request.session['email']})
        else:
            return redirect('index')

def list_seller_products(request):
    if request.method == 'GET':
        if request.session['email'] and request.session['seller']== True:
            cur_email = request.session['email']
            cur_seller = seller.objects.get(email=cur_email)
            out = product.objects.filter(product_seller=cur_seller)
            products = []
            for i in out:
                products.append(i)
    return render(request, "view_products.html", {'login':1,'cur_email':request.session['email'],'products':products})