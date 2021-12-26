"""schoolMathExpressions URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mathexp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name="home"),
    path('accounts/login/', views.get_auth, name="login"),
    path("accounts/logout/", views.logout_view, name="logout"),
    
    path("student/list",views.StudentList.as_view(), name="studentlist"),
    path("student/create", views.StudentCreate.as_view(), name="studentcreate"),
    path("student/update/<pk>", views.StudentUpdate.as_view(), name="studentupdate"),
    path("student/delete/<pk>", views.StudentDelete.as_view(), name="studentdelete"),
    path("mathexpressions/create", views.check_math_expression, name="mathexpressionscreate"),
    path("mathexpressions/list", views.math_expressions_list, name="mathexplist"),
]
