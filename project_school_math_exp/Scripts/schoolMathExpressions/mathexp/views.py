from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from .models import  *
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import *

# Create your views here.
def logout_view(request): 
    logout(request)
    return redirect('home')
@login_required
def home(request):   
    context = {"name": "User", "title": "Система помощи ученикам школьникам в изучении математики"}
    return render(request, "mathexp/home.html", context)
def get_auth(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Loginform(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if form.is_valid() and user is not None:
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            return HttpResponse("invalid credentials")
    # if a GET (or any other method) we'll create a blank form
    else:
        form = Loginform()
    return render(request, 'registration/login.html', {'form': form})
class StudentList(LoginRequiredMixin, ListView):
    model = Student
    template_name = "mathexp/student_list.html"
class StudentCreate(LoginRequiredMixin, CreateView):
    model = Student
    template_name = "mathexp/student_create_form.html"
    form_class = StudentForm
class StudentUpdate(LoginRequiredMixin, UpdateView):
    model = Student
    template_name = "mathexp/student_update_form.html"
    form_class = StudentForm
class StudentDelete(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = "mathexp/student_delete_form.html"
    success_url = reverse_lazy('studentlist')
    