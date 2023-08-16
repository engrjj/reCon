from django.shortcuts import render, redirect
from django.http import JsonResponse
from users.models import User
from contractors.models import Contractor
from contractors.models import Project

import bcrypt

# Create your views here.
def user_registration(request):
    return render(request,'userreg.html')

def user_process(request):
    if request.method == 'POST':
        errors = User.objects.validator(request.POST)
        email = request.POST['email']
        if Contractor.objects.filter(email=email).exists():
            errors['email'] = "Email is already in use."
        if len(errors) > 0:
            is_valid = False
            data = {
                'is_valid': is_valid,
                'errors': errors
            }
            return JsonResponse(data)
        
        else:
            first_name = request.POST['fname']
            last_name = request.POST['lname']
            email = request.POST['email']
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            logged_user = User.objects.create(
                first_name = first_name,
                last_name = last_name,
                email = email,
                password = pw_hash,
            )
            request.session['user_id'] = logged_user.id
            is_valid = True
            data = {
                'is_valid': is_valid
            }
            return JsonResponse(data)
        
def user_dashboard(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'user': user,
            'projects': user.projects.all()
        }

        return render(request, 'userdash.html', context)
    else:
        return redirect('/')

def add_project(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        errors = {}
        if len(request.POST['project_code']) < 5:
            errors['project_code'] = "Please use a valid code."
            is_valid = False
            data = {
                'is_valid': is_valid,
                'errors': errors
                }
            return JsonResponse(data)
        else:
            project_code = request.POST['project_code']
            project = Project.objects.filter(project_code=project_code).first()
            is_valid = True
            if not project:
                errors['project_code'] = "No project with this code."
                is_valid = False
            if is_valid and user in project.owners.all():
                errors['project_code'] = "You already added this project."
            if len(errors) > 0:
                is_valid = False
                data = {
                    'is_valid': is_valid,
                    'errors': errors
                }
                return JsonResponse(data)
            else:
                project.owners.add(user)
                data = {
                    'is_valid': is_valid
                }
                return JsonResponse(data)
            
def remove_project(request, project_id):
    project = Project.objects.get(id=project_id)
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        project.owners.remove(user)
        return redirect('/user/dashboard')
    
def contractor_list(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        all_contractors = Contractor.objects.all()
        if 'sort' in request.session:
            if request.session['sort'] == 1:
                all_contractors = Contractor.objects.all().order_by('company_name')
            elif request.session['sort'] == 2:
                all_contractors = Contractor.objects.all().order_by('specialization')
        else:
            request.session['sort'] = 0
        context = {
            'all_contractors': all_contractors,
            'user': user,
            'sort': request.session['sort']
        }
        del request.session['sort']
        return render(request, 'contractorlist.html', context)
    else:
        return redirect('/')
    
def sort(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        if request.POST['sort'] == "1":
            request.session['sort'] = 1
        elif request.POST['sort'] == "2":
            request.session['sort'] = 2
        return redirect('/user/browse')
    else:
        return redirect('/')