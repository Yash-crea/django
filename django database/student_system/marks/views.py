from django.shortcuts import render
from .models import Mark
from .forms import MarkInputForm, MarkUpdateForm

def index(request):
    active_section = request.GET.get('section', 'home')
    
    # Home Data
    num_students = Mark.objects.values('student_id').distinct().count()
    num_modules = Mark.objects.values('module_code').distinct().count()
    
    # Initialize forms
    input_form = MarkInputForm()
    update_form = MarkUpdateForm()
    view_marks = None
    
    if request.method == 'POST':
        # Input Mark
        if 'input_submit' in request.POST:
            input_form = MarkInputForm(request.POST)
            if input_form.is_valid():
                input_form.save()
                active_section = 'input_mark'
        
        # Update Mark
        elif 'update_search' in request.POST:
            module_code = request.POST.get('module_code')
            student_id = request.POST.get('student_id')
            date = request.POST.get('date')
            try:
                mark = Mark.objects.get(
                    module_code=module_code,
                    student_id=student_id,
                    date=date
                )
                update_form = MarkUpdateForm(instance=mark)
            except Mark.DoesNotExist:
                update_form = MarkUpdateForm()
            active_section = 'update_mark'
        
        elif 'update_submit' in request.POST:
            update_form = MarkUpdateForm(request.POST)
            if update_form.is_valid():
                update_form.save()
                active_section = 'update_mark'
        
        # View Mark
        elif 'view_submit' in request.POST:
            module_code = request.POST.get('module_code')
            view_marks = Mark.objects.filter(module_code=module_code)
            active_section = 'view_mark'
    
    context = {
        'active_section': active_section,
        'num_students': num_students,
        'num_modules': num_modules,
        'input_form': input_form,
        'update_form': update_form,
        'view_marks': view_marks,
    }
    return render(request, 'marks/index.html', context)
