from django.shortcuts import render,redirect,reverse

def index(request):
	return redirect(reverse('front:index'))