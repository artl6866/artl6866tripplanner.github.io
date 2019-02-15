from django.shortcuts import render, HttpResponse, redirect
from.models import *
from django.contrib import messages
from datetime import datetime
import bcrypt
from ..app_one.models import *

def main(request):
    context = {
        'user_name' : User.objects.get(id=request.session['user_id']),
        'my_trips' : Trip.objects.filter(user_travel = request.session['user_id']),
        'other_trips' : Trip.objects.exclude(user_travel = request.session['user_id']),
    }
    return render(request,'trip_app/index.html', context)
    
def add(request):
    context = {}
    return render(request,'trip_app/add.html',context)

def processadd(request):
    if request.method == 'POST':
        errors = Trip.objects.trip_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/trip/processadd')
    
    if request.method == 'POST':
        add_user = User.objects.get(id=request.session['user_id'])
        trip = Trip.objects.create(destination = request.POST['destination'], description = request.POST['description'], startdate = request.POST['startdate'], end_date = request.POST['end_date'], user_create = add_user )
        trip.user_travel.add(add_user)
        return redirect('/trip')

    elif request.method =='GET':
        return render(request,'trip_app/add.html')




def show(request, id):
    trip = Trip.objects.get(id=id)
    all_trips = User.objects.filter(user_destination = id)

    context = {
        'my_trip' : trip,
        'trip_joined' : Trip.objects.filter(id=request.session['user_id']),
        'alluser' : all_trips.exclude(id=trip.user_create.id)

    }
    return render(request,'trip_app/show.html',context)

def join(request, id):
    if 'user_id' not in request.session:
        return redirect('/trip')
    trip = Trip.objects.get(id=id)
    userjoined = User.objects.get(id=request.session['user_id'])
    tripjoined = trip.user_travel.add(userjoined)
    trip.save()
    return redirect('/trip')

def delete(request, id):
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=id)
    trip.delete()
    return redirect('/trip')

def cancel(request, id):
    userjoined = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=id)
    trip.user_travel.remove(userjoined)
    return redirect('/trip')