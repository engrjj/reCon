from django.shortcuts import render, redirect
from django.http import JsonResponse
from contractors.models import Contractor
from contractors.models import Project
from contractors.models import Photos
from contractors.models import Update
from users.models import User

from decimal import Decimal
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login_page(request):
    return render(request,'login.html')

def login_process(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'contractor_id' in request.session:
        del request.session['contractor_id']
    if request.method == 'POST':
        contractor = Contractor.objects.filter(email=request.POST['email'])
        if contractor:
            logged_user = contractor[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['contractor_id'] = logged_user.id
                is_valid=True
                is_contractor=True
                data = {
                    'is_valid': is_valid,
                    'is_contractor': is_contractor
                }
                return JsonResponse(data)
            else:
                is_valid=False
                data = {
                    'is_valid': is_valid
                }
                return JsonResponse(data)
        elif not contractor:
            user = User.objects.filter(email=request.POST['email'])
            if user:
                logged_user = user[0]
                if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                    request.session['user_id'] = logged_user.id
                    is_valid=True
                    is_contractor=False
                    data = {
                        'is_valid': is_valid,
                        'is_contractor': is_contractor
                    }
                    return JsonResponse(data)
                else:
                    is_valid=False
                    data = {
                        'is_valid': is_valid
                    }
                    return JsonResponse(data)
        else:
            is_valid=False
            data = {
                'is_valid': is_valid,
            }
            return JsonResponse(data)
        
    is_valid=False
    data = {
    'is_valid': is_valid,
    }
    return JsonResponse(data)



def contractor_registration(request):
    return render(request, 'conreg.html')

def contractor_process(request):
    if request.method == 'POST':
        errors = Contractor.objects.validator(request.POST)
        if len(errors) > 0:
            is_valid = False
            data = {
                'is_valid': is_valid,
                'errors': errors
            }

            return JsonResponse(data)
        
        else:
            company_name = request.POST['company_name']
            specialization = request.POST['specialization']
            mobile = request.POST['mobile']
            email = request.POST['email']
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            logged_user = Contractor.objects.create(
                company_name = company_name,
                specialization = specialization,
                mobile = mobile,
                email = email,
                password = pw_hash,
            )
            request.session['contractor_id'] = logged_user.id
            is_valid = True
            data = {
                'is_valid': is_valid
            }
            return JsonResponse(data)

def contractor_dashboard(request):
    if 'contractor_id' in request.session:
        contractor = Contractor.objects.get(id=request.session['contractor_id'])
        context = {
            'contractor': contractor,
            'projects': contractor.projects.all()
        }

        return render(request, 'condash.html', context)
    else:
        return redirect('/')

def contractor_profile(request, contractor_id):
    contractor = Contractor.objects.get(id=contractor_id)
    if 'contractor_id' in request.session:
        context = {
            'contractor': contractor,
        }
        return render(request, 'cProfile.html', context)
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'contractor': contractor,
            'user': user
        }
        return render(request, 'cProfile.html', context)
    else:
        return redirect('/')

def edit_profile(request, contractor_id):
    if 'contractor_id' in request.session:
        contractor = Contractor.objects.get(id=request.session['contractor_id'])
        context = {
            'contractor': contractor,
        }
        return render(request, 'editCProfile.html', context)
    else:
        return redirect('/')
    
def edit_profile_process(request, contractor_id):
    if request.method == 'POST':
        contractor = Contractor.objects.get(id=contractor_id)
        errors = Contractor.objects.validator(request.POST, contractor)
        if len(errors) > 0:
            is_valid = False
            data = {
                'is_valid': is_valid,
                'errors': errors
            }

            return JsonResponse(data)
        
        else:
            company_name = request.POST['company_name']
            specialization = request.POST['specialization']
            mobile = request.POST['mobile']
            email = request.POST['email']
            company_description = request.POST['company_description']
            contractor.logo = contractor.logo
            if 'logo' in request.FILES:
                if contractor.logo:
                    contractor.remove_logo()
                logo = request.FILES['logo']
                contractor.logo = logo
            
            contractor.company_name = company_name
            contractor.specialization = specialization
            contractor.mobile = mobile
            contractor.email = email
            contractor.company_description = company_description
            contractor.save()

            is_valid = True
            data = {
                'is_valid': is_valid,
                'contractor_id': contractor_id
            }
            return JsonResponse(data)
    
def upload_contractor_image(request, contractor_id):
    if request.method == 'POST':
        contractor = Contractor.objects.get(id=contractor_id)
        if 'image' in request.FILES:
            image = request.FILES['image']
            caption = request.POST['caption']
            Photos.objects.create(
                image=image,
                caption=caption,
                contractor=contractor,
            )
        return redirect(f'/contractor/profile/{contractor_id}')

def create_project(request):
    if 'contractor_id' in request.session:
        contractor = Contractor.objects.get(id=request.session['contractor_id'])
        context = {
            'contractor': contractor,
        }
        return render(request, 'createProj.html', context)
    else:
        return redirect('/')
    

def create_process(request):
    if request.method == 'POST':
        errors = Project.objects.validator(request.POST)
        if len(errors) > 0:
            is_valid = False
            data = {
                'is_valid': is_valid,
                'errors': errors
            }

            return JsonResponse(data)
        
        else:
            contractor = Contractor.objects.get(id=request.session['contractor_id'])
            project_name = request.POST['project_name']
            project_description = request.POST['project_description']
            project_cost = Decimal(request.POST['project_cost'])
            completion_date = request.POST['completion_date']
            Project.objects.create(
                project_name = project_name,
                project_description = project_description,
                project_cost = project_cost,
                completion_date = completion_date,
                contractor = contractor
            )
            is_valid = True
            data = {
                'is_valid': is_valid
            }
            return JsonResponse(data)

def show_project(request, project_id):
    project = Project.objects.get(id=project_id)
    updates = project.updates.all().order_by('-date')
    if 'contractor_id' in request.session:
        contractor = Contractor.objects.get(id=request.session['contractor_id'])
        context = {
            'contractor': contractor,
            'project': project,
            'updates': updates,
        }
        return render(request, 'showProj.html', context)
    elif 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'user': user,
            'project': project,
            'contractor': project.contractor,
            'updates': updates
        }
        return render(request, 'showProj.html', context)
    else:
        return redirect('/')
    
def edit_project(request, project_id):
    project = Project.objects.get(id=project_id)
    if 'contractor_id' in request.session:
        contractor = Contractor.objects.get(id=request.session['contractor_id'])
        context = {
            'contractor': contractor,
            'project': project,
        }
        return render(request, 'editProj.html', context)
    else:
        return redirect('/')
        
def edit_process(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        errors = Project.objects.validator(request.POST, project)
        if len(errors) > 0:
            is_valid = False
            data = {
                'is_valid': is_valid,
                'project_id': project_id,
                'errors': errors
            }

            return JsonResponse(data)
        
        else:
            project_name = request.POST['project_name']
            project_description = request.POST['project_description']
            project_cost = Decimal(request.POST['project_cost'])
            completion_date = request.POST['completion_date']

            project.project_name = project_name
            project.project_description = project_description
            project.project_cost = project_cost
            project.completion_date = completion_date
            project.save()

            is_valid = True
            data = {
                'is_valid': is_valid,
                'project_id': project_id
            }
            return JsonResponse(data)


def upload_project_image(request, project_id):
    if request.method == 'POST':
        project = Project.objects.get(id=project_id)
        if 'image' in request.FILES:
            image = request.FILES['image']
            caption = request.POST['caption']
            Photos.objects.create(
                image=image,
                caption=caption,
                project=project,
            )
        return redirect(f'/contractor/projects/{project.id}')

def create_update(request, project_id):
    if 'contractor_id' in request.session:
        contractor = Contractor.objects.get(id=request.session['contractor_id'])
        project = Project.objects.get(id=project_id)
        context = {
            'contractor': contractor,
            'project': project,
        }
        return render(request, 'createupdate.html', context)
    else:
        return redirect('/')
    
def update_process(request, project_id):
    if request.method == 'POST':
        errors = Update.objects.validator(request.POST)
        if len(errors) > 0:
            is_valid = False
            data = {
                'is_valid': is_valid,
                'project_id': project_id,
                'errors': errors
            }

            return JsonResponse(data)
        else:
            project = Project.objects.get(id=project_id)
            update_description = request.POST['update_description']
            date = request.POST['date']
            update = Update.objects.create(
                update_description = update_description,
                date = date,
                project = project
            )
            is_valid = True
            data = {
                'is_valid': is_valid,
                'project_id': project_id,
                'update_id': update.id,
            }
            return JsonResponse(data)
        
def show_update(request, project_id, update_id):
    project = Project.objects.get(id=project_id)
    update = Update.objects.get(id=update_id)
    if 'contractor_id' in request.session:
        contractor = Contractor.objects.get(id=request.session['contractor_id'])
        context = {
            'contractor': contractor,
            'project': project,
            'update': update,
        }
        return render(request, 'showUpdate.html', context)
    elif 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'user': user,
            'project': project,
            'update': update,
        }
        return render(request, 'showUpdate.html', context)
    else:
        return redirect('/')

def edit_update(request, project_id, update_id):
    update = Update.objects.get(id=update_id)
    project = Project.objects.get(id=project_id)
    if 'contractor_id' in request.session:
        contractor = Contractor.objects.get(id=request.session['contractor_id'])
        context = {
            'contractor': contractor,
            'project': project,
            'update': update,
        }
        return render(request, 'editupdate.html', context)
    else:
        return redirect('/')
    
def edit_update_process(request, project_id, update_id):
    update = Update.objects.get(id=update_id)
    if request.method == 'POST':
        errors = Update.objects.validator(request.POST)
        if len(errors) > 0:
            is_valid = False
            data = {
                'is_valid': is_valid,
                'project_id': project_id,
                'update_id': update_id,
                'errors': errors
            }

            return JsonResponse(data)
        
        else:
            update_description = request.POST['update_description']
            date = request.POST['date']

            update.update_description = update_description
            update.date = date
            update.save()

            is_valid = True
            data = {
                'is_valid': is_valid,
                'project_id': project_id,
                'update_id': update_id,
            }
            return JsonResponse(data)

def upload_update_image(request, project_id, update_id):
    if request.method == 'POST':
        update = Update.objects.get(id=update_id)
        project = Project.objects.get(id=project_id)
        if 'image' in request.FILES:
            image = request.FILES['image']
            caption = request.POST['caption']
            Photos.objects.create(
                image=image,
                caption=caption,
                project=project,
                update=update,
            )
        return redirect(f'/contractor/projects/{project_id}/updates/{update_id}')
    
def delete_image(request, image_id):
    if 'contractor_id' in request.session:
        photo = Photos.objects.get(id=image_id)
        project_id = photo.project.id
        photo.delete()
        return redirect(f'/contractor/projects/{project_id}')
    else:
        return redirect('/')

def delete_update_image(request, image_id):
    if 'contractor_id' in request.session:
        photo = Photos.objects.get(id=image_id)
        project_id = photo.project.id
        update_id = photo.update.id
        photo.delete()
        return redirect(f'/contractor/projects/{project_id}/updates/{update_id}')
    else:
        return redirect('/')

def delete_contractor_image(request, image_id):
    if 'contractor_id' in request.session:
        photo = Photos.objects.get(id=image_id)
        contractor_id = photo.contractor.id
        photo.delete()
        return redirect(f'/contractor/profile/{contractor_id}')
    else:
        return redirect('/')

def delete_contractor_logo(request, contractor_id):
    if 'contractor_id' in request.session:
        contractor = Contractor.objects.get(id=contractor_id)
        contractor.remove_logo()
        return redirect(f'/contractor/profile/{contractor_id}/edit')
        

def delete_update(request, project_id, update_id):
    if 'contractor_id' in request.session:
        update = Update.objects.get(id=update_id)
        update.delete()
        return redirect(f'/contractor/projects/{project_id}')
    else:
        return redirect('/')
    
def delete_project(request, project_id):
    if 'contractor_id' in request.session:
        project = Project.objects.get(id=project_id)
        project.delete()
        return redirect(f'/contractor/dashboard')
    else:
        return redirect('/')

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'contractor_id' in request.session:
        del request.session['contractor_id']
    return redirect('/')