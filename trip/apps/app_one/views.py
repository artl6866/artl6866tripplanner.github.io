from django.shortcuts import render, HttpResponse, redirect
from.models import *
from django.contrib import messages
import bcrypt
# Create your views here.
def main(request):
    if not 'user_id' in request.session:
        request.session['user_id'] = None
    #check session if logged in
    if request.session['user_id'] == None:
        return render (request,'app_one/index.html')

    else:
    #if not logged in, they should be redirect/shown to login page.
    #after logging into main page, user should view my dogs page with their own information.
        return redirect('/trip')

#POST request to process a user's registration form submission.
def register(request):
    if request.method =='POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
        
        else:
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            just_registered = User.objects.create(fname=request.POST['fname'],lname=request.POST['lname'],email=request.POST['email'], password=hashed_pw.decode())
            request.session["username"] = just_registered.fname
            request.session["user_id"] = just_registered.id
            return redirect("/trip")

    return redirect("/")

# def display(request):
#     context = {
#         "allusers" :User.objects.all(),
#     }

#     return render(request, 'app_one/display.html',context)

def login(request):
    if request.method =='POST':
        user_logging_in = User.objects.filter(email=request.POST['email'])

        if len(user_logging_in) == 0:
            messages.error(request,"No matching user")
        elif not bcrypt.checkpw(request.POST['pw'].encode(), user_logging_in[0].password.encode()):
            messages.error(request,'Password is incorrect')
        else:
            request.session["username"] = user_logging_in[0].fname
            request.session["user_id"] = user_logging_in[0].id
            messages.success(request,"Successfully logged in")
            return redirect("/trip")


    return redirect("/")

def logout(request):
    request.session['username'] = None
    request.session['user_id'] = None
    request.session.clear()
    
    return redirect('/')
