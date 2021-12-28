from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from .models import  *
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import *
from django.contrib.auth import logout
from django.db.models import Sum
from .calculator import *

# Create your views here.
# view для кнопки выхода авторизованного пользователя
@login_required
def logout_view(request): 
    logout(request)
    return redirect('home')

# view для кнопки выхода авторизованного пользователя
@login_required
def home(request):   
    context = {"name": "User", "title": "Система помощи ученикам школьникам в изучении математики"}
    return render(request, "mathexp/home.html", context)
def get_auth(request):
    # прописываем POST запрос как условие
    if request.method == 'POST':
        # создаем экземпляр формы и вносим полученные данные
        form = Loginform(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if form.is_valid() and user is not None:
            # проверка на валидность и, если всё ок, то срабатывает редирект на главную страницу
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            return HttpResponse("invalid credentials")
    # если же был GET-запрос, либо сработало любое другое условие, то пользователь возвращается на страницу авторизации
    else:
        form = Loginform()
    return render(request, 'registration/login.html', {'form': form})

# view для формы отправки математического выражения
@login_required
def check_math_expression(request):
# прописываем POST запрос как условие
    if request.method == 'POST':
        # создаем экземпляр формы и вносим полученные данные
        form = MathExpressionsForm(request.POST)
        name = request.POST["name"]
        mathExpression = request.POST["mathExpression"]
        ResolveNumber = request.POST["ResolveNumber"]
        # К переменным из формы добавляем новые: В studentQuery сохраняем выгрузку по всем объектам таблицы Student
        studentQuery = Student.objects.all()
        # В nameStudent сохраняем выгрузку из Student именно по выбранному ученику
        nameStudent = studentQuery.get(pk=name)
        # дальнейшие действия, если форма прошла проверку django на валидность
        
        if form.is_valid():
            # сначала проверяем корректно ли был составлен пример
            checkValidExpression = checkMathExp.check_valid(mathExpression)
            # объявляем переменную, которая содерижт часть текста из строки, которую вовзращает функция check_valid() при некорректно составленном примере
            invalid = 'Выражение невалидно'
            # если в ответе checkMathExp.check_valid(mathExpression) нет строки с содержанием 'Выражение невалидно', то выполняются следующие действия
            if invalid not in checkValidExpression:
                # Пример вычисляется в  checkMathExp.eval_math(mathExpression) и ответ записывается в переменную checkValidResolve
                checkValidResolve = checkMathExp.eval_math(mathExpression)
                # Если ответ из функции eval_math() совпал с ответом, который внес пользователь и которы был записан в ResolveNumber, то:
                if str(checkValidResolve) == ResolveNumber:
                    # объявляется переменная mathExpressionQueryInstance, которая загружает в таблицу MathExpressions полученные данные
                    mathExpressionQueryInstance = MathExpressions(name=nameStudent, 
                                                                  mathExpression=mathExpression, 
                                                                  validExpression=1, 
                                                                  nonvalidExpression=0, 
                                                                  validMathResolve=1, 
                                                                  nonvalidMathResolve=0
                                                                  )
                    # данные сохраняются
                    mathExpressionQueryInstance.save()
                    # объявляется resolveResponseYes, в которой записывается ответ, отображаемый для пользователя на страницей с формой для мат. выражения
                    resolveResponseYes = 'Да, ответ ' + str(ResolveNumber) + ' правильный'
                    # пользователь преходит на ту же страницу с обновленными данными
                    return render(request, 'mathexp/mathexpressions_create_form.html', {'form': form,
                                                                                        'namestudent': nameStudent, 
                                                                                        'mathExpression': mathExpression, 
                                                                                        'checkValidExpression': 'Да',
                                                                                        'checkValidResolve': resolveResponseYes
                                                                                        }
                                  )
                else:
                    # Те же действия, но, если ответ в примере и ответ указанный пользователем не совпали
                    mathExpressionQueryInstance = MathExpressions(name=nameStudent, 
                                                                  mathExpression=mathExpression, 
                                                                  validExpression=1, 
                                                                  nonvalidExpression=0, 
                                                                  validMathResolve=0, 
                                                                  nonvalidMathResolve=1
                                                                  )
                    mathExpressionQueryInstance.save()
                    resolveResponsNo = 'Нет, ответ ' + str(ResolveNumber) + ' неверный. Правильный ответ: ' + str(checkValidResolve)
                    return render(request, 'mathexp/mathexpressions_create_form.html', {'form': form,
                                                                                        'namestudent': nameStudent,
                                                                                        'mathExpression': mathExpression,
                                                                                        'checkValidExpression': 'Да',
                                                                                        'checkValidResolve': resolveResponsNo
                                                                                        }
                                  )
            elif invalid in checkValidExpression:
                # также формируется ответ как в примерах выше, но, при условии, что сам пример был составлен некорректно
                mathExpressionQueryInstance = MathExpressions(name=nameStudent,
                                                              mathExpression=mathExpression,
                                                              validExpression=0,
                                                              nonvalidExpression=1,
                                                              validMathResolve=0,
                                                              nonvalidMathResolve=0
                                                              )
                mathExpressionQueryInstance.save()
                return render(request, 'mathexp/mathexpressions_create_form.html', {'form': form,
                                                                                    'namestudent': nameStudent,
                                                                                    'mathExpression': mathExpression,
                                                                                    'checkValidExpression': 'Нет',
                                                                                    'checkValidResolve': 'Неизвестно, так как пример составлен некорректно'
                                                                                    }
                              )

    else:
        # любом другом случае просто формируется страница с формой
        form = MathExpressionsForm()
    return render(request, 'mathexp/mathexpressions_create_form.html', {'form': form})

# view для выгрузки результатов учеников
@login_required
@permission_required('mathexp.view_mathexpressions', raise_exception=True)
def math_expressions_list(request):
  # прописываем POST запрос как условие
    if request.method == 'POST':
        # создаем экземпляр формы и вносим полученные данные
        form = MathExpressionsListForm(request.POST)
        name = request.POST["name"]
        # К переменным из формы добавляем новые: В studentQuery сохраняем выгрузку по всем объектам таблицы Student
        studentQuery = Student.objects.all()
        # В nameStudent сохраняем выгрузку из Student именно по выбранному ученику
        nameStudent = studentQuery.get(pk=name)
        # дальнейшие действия, если форма прошла проверку django на валидность
        if form.is_valid():
            # Чтобы разделить выгрузку по всем ученикам и по отдельности я добавил ученика с именем "Все ученики" в таблицу Students
            # Ниже объявил переменную со строкой "ученики" в значении.
            # Она нужна для проверки всех ли учеников хочет посмотреть пользователь или только кого-то конкретно
            allStudents = 'ученики'
            if allStudents in str(nameStudent):
                # Если условие выполнено, то, значит, пользователь выбрал всех учеников
                # В students_data получаем данные по всем элементам таблицы Student кроме строки с "Все ученики", id у нее 6, поэтому exclude(pk=6)
                students_data = Student.objects.values().exclude(pk=6)
                # В math_expressions_result собираем агрегированные данные с результатами по всем ученикам, у которых они есть.
                # В эту выборку не попадают те, которые ни разу не вносили на свое имя мат.выражения
                math_expressions_result = MathExpressions.objects.values('name_id').annotate(Sum('validExpression'),
                                                                                             Sum('nonvalidExpression'),
                                                                                             Sum('validMathResolve'),
                                                                                             Sum('nonvalidMathResolve')
                                                                                             ).order_by('name_id')
                # Данные для выгрузки в таблицу на странице собираеются в context
                context = {'form': form, 
                           'students_exp_list': students_data,
                           'math_expressions_result': math_expressions_result
                           }
                return render(request, 'mathexp/math_expressions_list.html',
                              context
                              )
            elif allStudents not in str(nameStudent):
                # Если условие выполнено, то, значит, пользователь выбрал ученика
                # В students_data получаем данные по всем элементам таблицы Student кроме строки с "Все ученики", id у нее 6, поэтому exclude(pk=6)
                students_data = Student.objects.values().exclude(pk=6)
                # В math_expressions_result собираем агрегированные данные с результатами по выбранному ученику
                # Для этого добавляется .filter(name_id=name)
                math_expressions_result = MathExpressions.objects.filter(name_id=name).values('name_id').annotate(Sum('validExpression'),
                                                                                                                  Sum('nonvalidExpression'),
                                                                                                                  Sum('validMathResolve'),
                                                                                                                  Sum('nonvalidMathResolve')
                                                                                                                  ).order_by('name_id')
                # Данные для выгрузки в таблицу на странице собираеются в context
                context = {'form': form,
                           'students_exp_list': students_data,
                           'math_expressions_result': math_expressions_result
                           }
                return render(request, 'mathexp/math_expressions_list.html', context)
            # При другом условии просто отправляется форма
            return render(request, 'mathexp/math_expressions_list.html', {'form': form})
    else:
        form = MathExpressionsListForm()
        # При другом условии просто отправляется форма
    return render(request, 'mathexp/math_expressions_list.html', {'form': form})

# класс для выгрузки списка учеников    
class StudentList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'mathexp.view_student'
    model = Student
    template_name = "mathexp/student_list.html"
# класс для создания записи ученика
class StudentCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'mathexp.add_student'
    model = Student
    template_name = "mathexp/student_create_form.html"
    form_class = StudentForm
# класс для изменения записи ученика
class StudentUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'mathexp.change_student'
    model = Student
    template_name = "mathexp/student_update_form.html"
    form_class = StudentForm
# класс для удаления записи ученика
class StudentDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'mathexp.delete_student'
    model = Student
    template_name = "mathexp/student_delete_form.html"
    success_url = reverse_lazy('studentlist')

    
