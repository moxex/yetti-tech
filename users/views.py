from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth


# User Registration View
def registerUser(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('hello_world')
        else:
            print(form.errors)
        
    else:
        form = UserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'users/registerUser.html', context)


# Login View
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('Hello World')
        else:
            messages.error(request, 'Invalid login credentials.')
            return redirect('login')
    return render(request, 'users/login.html')


# Logout View
def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out.')
    return redirect('home')


@login_required(login_url='login')
def helloWorld(request):
    return render(request, 'hello_world.html')
