from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmployeeForm
from .models import Employee
from django.core.paginator import EmptyPage, PageNotAnInteger,Paginator
from django.db.models  import Q
from .filters import EmployeeFilter
from .utils import render_to_pdf
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def dashboard(request):
    username = request.user.username
    user_id = request.user.id 
    print(f"Home view accessed by user: {username}")  # This will be logged in the server log
    context = {
        'username': username,
    }
    return render(request, 'employee/Dashboard.html', context)

def emp(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('employee:show')
            except:
                pass
    else:
        form = EmployeeForm()
    return render(request,'employee/index.html',{'form':form})

def show(request):
    employees = Employee.objects.all().order_by('id')
    paginator = Paginator(employees,2)
    page=request.GET.get('page')
    paged_employees=paginator.get_page(page)
    context = {
        'employees': paged_employees,
        'emp': employees,
    }
    return render(request,"employee/show.html",context)

def showall(request):
    employees = Employee.objects.all().order_by('id')
    return render(request,"employee/show.html",{'employees':employees})



def edit(request, id):
    employee = Employee.objects.get(id=id)

    return render(request,'employee/edit.html', {'employee':employee})

def update(request, id):
    employee = Employee.objects.get(id=id)
    form = EmployeeForm(request.POST, request.FILES, instance=employee)
    if form.is_valid():
        form.save()
        return redirect('employee:show')
    return render(request, 'employee/edit.html', {'employee': employee})

def destroy(request, id):
    employee = get_object_or_404(Employee, id=id)
    employee.delete()
    return redirect('employee:show')


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
           employees=Employee.objects.filter(Q(ename__icontains=keyword) | Q(eemail__icontains=keyword) | Q(econtact__icontains=keyword))
           employees_count = employees.count()
        else:
           employees = Employee.objects.all()
           employees_count = employees.count()
           return redirect("employee:showall")

    context = {
    'employees'      : employees,
    'employees_count' : employees_count,
    }
    return render(request,'employee/show.html',context)

def doc(request,id):
    template_name = "employee/pdf.html"
    records = Employee.objects.get(id=id)

    return render_to_pdf(
        template_name,
        {
            "record": records,
        },
    )