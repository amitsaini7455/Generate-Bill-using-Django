from django.shortcuts import render, redirect, get_object_or_404
from .models import Receipt 
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
from .models import Receipt


@login_required(login_url='/login/')
def receipts(request):
    if request.method == 'POST': 
        data = request.POST
        name = data.get('name')
        price = data.get('price')
        quantity = data.get('quantity')
        total = float(price) * int(quantity)

        Receipt.objects.create(
            name=name,
            price=price,
            quantity=quantity,
            total=total
        )
        return redirect('/')

    queryset = Receipt.objects.all()
    if request.GET.get('search'):
        queryset = queryset.filter(name__icontains=request.GET.get('search'))

    total_sum = sum(receipt.total for receipt in queryset)
    context = {'receipts': queryset, 'total_sum': total_sum}
    return render(request, 'receipts.html', context)

@login_required(login_url='/login/')
def update_receipt(request, id):
    queryset = get_object_or_404(Receipt, id=id)  # Use get_object_or_404 for better error handling

    if request.method == 'POST':
        data = request.POST 
        name = data.get('name')
        price = data.get('price')
        quantity = data.get('quantity')
        total = float(price) * int(quantity)

        queryset.name = name
        queryset.price = price
        queryset.quantity = quantity
        queryset.total = total
        queryset.save()
        return redirect('/')

    context = {'receipt': queryset}
    return render(request, 'update_receipt.html', context)

@login_required(login_url='/login/')
def delete_receipt(request, id):
    queryset = get_object_or_404(Receipt, id=id)
    if request.method == "POST":
        queryset.delete()
        return redirect('/')
    return render(request, 'confirm_delete.html', {'receipt': queryset})

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=username)
        if not user_obj.exists():
            messages.error(request, "Username not found")
            return redirect('/login/')
        user_obj = authenticate(username=username, password=password)
        if user_obj:
            login(request, user_obj)
            return redirect('receipts')
        messages.error(request, "Wrong Password")
        return redirect('/login/')
    return render(request, "login.html")

def register_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=username)
        if user_obj.exists():
            messages.error(request, "Username is taken")
            return redirect('/register/')
        user_obj = User.objects.create(username=username)
        user_obj.set_password(password)
        user_obj.save()
        messages.success(request, "Account created")
        return redirect('/login')
    return render(request, "register.html")

def custom_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/login/')
def pdf(request):
    if request.method == 'POST':
        data = request.POST 
        name = data.get('name')
        price = data.get('price')
        quantity = data.get('quantity')
        total = float(price) * int(quantity)

        Receipt.objects.create(
            name=name,
            price=price,
            quantity=quantity,
            total=total
        )
        return redirect('pdf')

    queryset = Receipt.objects.all()
    if request.GET.get('search'):
        queryset = queryset.filter(name__icontains=request.GET.get('search'))

    total_sum = sum(receipt.total for receipt in queryset)
    context = {'receipts': queryset, 'total_sum': total_sum}
    return render(request, 'pdf.html', context)
