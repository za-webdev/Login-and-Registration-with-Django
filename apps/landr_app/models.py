# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9+-._]+@[a-zA-Z0-9+-._]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
	def register(self,first_name,last_name,email,password,conf_password):
		response={
			'valid':True,
			'errors':[],
			'user':None
		}
		#for first name
		if len(first_name)<1:
			response['errors'].append('First name is required')
		elif len(first_name)<2:
			response['errors'].append(' First Name must be greater than 2 characters or more')
			#for last name
		if len(last_name)<1:
			response['errors'].append('Last name is required')
		elif len(last_name)<2:
			response['errors'].append(' Last Name must be greater than 2 characters or more')
			#for email
		if len(email)<1:
			response['errors'].append('Email is required')
		elif not EMAIL_REGEX.match(email):
			response['errors'].append('Invalid Email')
		else:
			email_list=User.objects.filter(email=email.lower())
			if len (email_list)>0:
				response['errors'].append('Email already exist')
		
			#for password
		if len(password)<1:
			response['errors'].append('Password is required')
		elif len(password)<8:
			response['errors'].append(' Password must be greater than 8 characters or more')

			#for conf password
		if len(conf_password)<1:
			response['errors'].append('Please confirm the password')
		if conf_password != password:
			response['errors'].append('Confirm password must match password')

		if len(response['errors'])>0:
			response['valid']=False

		else:
			user=User.objects.create(
				first_name=first_name,
				last_name=last_name,
				email=email.lower(),
				password=bcrypt.hashpw(password.encode(),bcrypt.gensalt())

			)
			response['user']=user

		return response


	def login(self,email,password):

		response={
			'valid':True,
			'errors':[],
			'user':None
		}
		#for email
		if len(email)<1:
			response['errors'].append('Email is required')
		elif not EMAIL_REGEX.match(email):
			response['errors'].append('Email is required')
		else:
			email_list=User.objects.filter(email=email.lower())
			if len (email_list)==0:
				response['errors'].append('Email doesnot exist')
		#for password
		if len(password)<1:
			response['errors'].append('Password is required')
		elif len(password)<8:
			response['errors'].append(' Password must be greater than 8 characters or more')

		if len(response['errors'])==0:
			hashed_pw = email_list[0].password
			if bcrypt.checkpw(password.encode(),hashed_pw.encode()):
				response['user']=email_list[0]
			else:
				response['errors'].append('Incorrect Password')

		if len(response['errors'])>0:
			response['valid']=False

		return response

class RecipeManager(models.Model):
	def addRecipe(self,recipeData,user):
		errors=[]

		if len(recipeData['name'])<1:
			errors.append('Recipe name is required')

		elif len(recipeData['name'])<3:
			errors.append('must be 3 characters')

		if len(recipeData['ingredients'])<1:
			errors.append('ingredients are required for a recipe')

		else:
			ingredients=recipeData['ingredients'].split(',')
			valid=True
			if len(ingredients)<3:
				valid=False	
			for ingredient in ingredients:
			if len(ingredient.split(" "))<3:
				valid=False

			if not valid:
				errors.append('Ingredient invalid, each ingredient should be separated by space and have amount and ')

			if len(recipeData['instructions'])<1:
					errors.append('Instructions are required for a recipe')

			if len(recipeData['instructions'])<10:
					errors.append('10 characters or more')


			if len(errors)>0:
				return (False,error)


			list_of_ingredients=[]
			for ingredient in ingredients:
				i=ingredient.split(' ')
				list_of_ingredients.append([' '.join])
			# (" ".join(i[:-2])).lstrip(" "),i[-2],i[-1])

			return(True)


			# (" ".join(i[:-2])).lstrip(" "),i[-2],i[-1])






class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email=models.CharField(max_length=255)
	password=models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects=UserManager()

	def __repr__(self):
		return "<User object: {} {} {}>".format(self.first_name, self.last_name, self.email, self.password)




class Ingredient(models.Model):
	name=models.CharField(max_length=255)

class Recipe(models.Model):
	name=models.CharField(max_length=255)
	instructions=models.TextField(max_length=2000)
	creator=models.Foreignkey(User,related_name='my_recipes')
	likes=models.ManyToManyField(User,related_name='liked_recipes')
	objects=RecipeManager()

class Amount(models.Model):
	amount=models.IntegerField()
	units=models.CharField(max_length=255)
	ingredient=model.Foreignkey(Ingredient,related_name='recipes_used')
	recipe=model.Foreignkey(Recipe,related_name='ingredients')



