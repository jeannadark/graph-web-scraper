from django.shortcuts import render
from django.http import HttpResponse


def guide(request):
	return render(request, template_name="guidelines.html")
