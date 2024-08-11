from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Student
from django.template import loader
from .forms import Studentform, NewUserForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

#logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/login/")

#login form
def user_login(request):
    login_context = {
        "form":AuthenticationForm()
    }
    
    if (request.method == 'GET'):
        return render(request, 'user/login.html', login_context)
    
    elif (request.method == 'POST'):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/")  # Add this 'return' statement
            else:
                messages.error(request,"Invalid username or password.")
                return render(request, 'user/login.html', login_context) 
        else:
            messages.error(request,"Credientials not found please register")
            return render(request, 'user/login.html', login_context)

#registration form
def user_signup(request):

    context ={
        'form': NewUserForm()
    }
    
    if (request.method == 'GET'):
        return render(request, 'user/signup.html', context)
    
    elif (request.method == 'POST'):
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect("/login/") # redirect example
        else:
            messages.error(request, "Invalid sign-up information.")
            return render(request, 'user/signup.html', context)

#display all data

def display_all(request):
    stu_context = {
        'students': Student.objects.all().values()
    }
    return render(request, 'display.html',stu_context )
    

# Create student 
def create_student(request):

    if(request.method=='GET'):
        context ={
            'form':Studentform()
        }
        return render(request, 'create_student.html', context)
    elif (request.method=='POST'):
        form=Studentform(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
        
#update data
def view_student(request, student_id):
    
    if (request.method == 'GET'):
        try:
            to_update_student_item = Student.objects.get(id=student_id)
        except:
            return HttpResponse(f'No such item found with id {student_id}')
        else:
            to_update_form = Studentform(instance=to_update_student_item)

            context ={
                'form': to_update_form,
                'student_id_number': student_id
            }

            return render (request, 'update.html',context )
        
    elif (request.method == 'POST'):
        try:
            to_update_student_item = Student.objects.get(id=student_id)
        except:
            return HttpResponse(f'No such item found with id {student_id}')
        else:
            to_update_form = Studentform(request.POST, instance=to_update_student_item)
            if to_update_form.is_valid():
                to_update_form.save()
                return HttpResponseRedirect('/')
            
#delete item
def delete_item(request, student_id):

    if (request.method == 'GET'):
        return render(request, 'delete.html', {})
        
    elif (request.method == 'POST'):
        try:
            to_update_student_item = Student.objects.get(id=student_id)
        except:
            return HttpResponse(f'No such item found with id {student_id}')
        else:
            to_update_student_item.delete()
            return HttpResponseRedirect('/') 
        
#rest api
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentSerializer

@api_view(['GET', 'POST'])
def student_list(request):
    if request.method == 'GET':
        students=Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    
    elif request.method=='POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def student_detail(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
