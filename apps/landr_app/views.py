# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from .models import User,Recipe
from django.contrib import messages


def index(request):


	return render(request,'landr_app/index.html')

def register(request):
	response=User.objects.register(

		request.POST['first_name'],
		request.POST['last_name'],
		request.POST['email'],
		request.POST['password'],
		request.POST['conf_password']

			)
	print response
	if response['valid']:
		request.session['user_id']=response['user'].id
		return redirect('/success')

	else:
		for error_message in response['errors']:
			messages.add_message(request,messages.ERROR,error_message)
		return redirect('/')


def login(request):

	response=User.objects.login(

		request.POST['email'],
		request.POST['password']

			)
	print response
	if response['valid']:
		request.session['user_id']=response['user'].id
		return redirect('/success')

	else:
		for error_message in response['errors']:
			messages.add_message(request,messages.ERROR,error_message)
		return redirect('/')



def success(request):

	if 'user_id' not in request.session:
		return redirect('/')

	context={

		'user':User.objects.get(id=request.session['user_id']),
	}


	return render(request,'landr_app/success.html',context)


def logout(request):

	request.session.clear()
	return redirect('/')


def create(request):
	current_user=User.objects.get(id=request.session['user_id'])
	return render(request,'landr_app/success.html',{'user':user})

def recipe(request):
	