# views.py
from .forms import RegisterForm
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render
from django.urls import reverse


# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)

        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Student')
            user.groups.add(group)
            user.is_staff = True
            user.save()

            return redirect(reverse('admin:login'))
    else:
        form = RegisterForm()
    return render(response, "registration/register.html", {"form": form})
