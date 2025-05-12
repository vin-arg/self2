from django.db.models import Case, When, IntegerField, Sum
from django.shortcuts import render, get_object_or_404, redirect
from .models import Commission, Job, JobApplication
from .forms import JobApplicationForm, CommissionForm, JobFormSet
from django.contrib.auth.decorators import login_required

def commission_list(request):
    commissions = Commission.objects.order_by(
        Case(
            When(status='Open', then=0),
            When(status='Full', then=1),
            When(status='Completed', then=2),
            When(status='Discontinued', then=3),
            output_field=IntegerField()
        ),
        '-created_on'
    )
    ctx = {
        'commissions': commissions
    }
    
    if request.user.is_authenticated:
        profile = request.user.profile
        ctx.update({
            'user_commissions': Commission.objects.filter(author=profile),
            'applied_commissions': Commission.objects.filter(
                jobs__applications__applicant=profile
            ).distinct().order_by('-created_on')
        })
        
    return render(request, 'commission_list.html', ctx)

def commission_detail(request, pk):
    commission = get_object_or_404(Commission, pk=pk)
    jobs = Job.objects.filter(commission=commission)
    
    if request.method == 'POST' and request.user.is_authenticated:
        job_id = request.POST.get('job')
        job = get_object_or_404(Job, id=job_id)

        accepted_count = JobApplication.objects.filter(job=job, status='Accepted').count()
        if accepted_count < job.manpower_required:
            already_applied = JobApplication.objects.filter(job=job, applicant=request.user.profile).exists()
            if not already_applied:
                form = JobApplicationForm(request.POST)
                if form.is_valid():
                    application = form.save(commit=False)
                    application.job = job
                    application.applicant = request.user.profile
                    application.save()
        return redirect('commissions:commission_detail', pk=pk)

    total_manpower = sum(job.manpower_required for job in jobs)
    open_manpower = 0
    job_data = []
    
    
    for job in jobs:
        accepted_count = JobApplication.objects.filter(job=job, status='Accepted').count()
        remaining = job.manpower_required - accepted_count
        open_manpower += remaining

        can_apply = (
            request.user.is_authenticated and
            remaining > 0 and
            not JobApplication.objects.filter(job=job, applicant=request.user.profile).exists()
        )

        job_data.append({
            'object': job,
            'remaining_positions': remaining,
            'can_apply': can_apply,
            'form': JobApplicationForm(initial={'status': 'Pending'}) if can_apply else None,
        })

    can_edit = request.user.is_authenticated and commission.author == request.user.profile

    
    ctx = {
        'commission': commission,
        'jobs': jobs,
        'total_manpower': total_manpower,
        'open_manpower': total_manpower - open_manpower,
        'can_edit': can_edit
    }
    
    return render(request, 'commission_detail.html', ctx)

def commission_create(request):
    form = CommissionForm()
    
    if request.method == 'POST':
        form = CommissionForm(request.POST)
        formset = JobFormSet(request.POST, queryset=Job.objects.none())

        if form.is_valid():
            commission = form.save(commit=False)
            commission.author = request.user.profile
            commission.save()

            if formset.is_valid():
                for job_form in formset:
                    if job_form.cleaned_data:
                        job = job_form.save(commit=False)
                        job.commission = commission
                        job.save()

            return redirect('commissions:commission_detail', pk=commission.pk)
    else:
        form = CommissionForm()
        formset = JobFormSet(queryset=Job.objects.none())

    return render(request, 'commission_form.html', {'commission_form': form,'job_formset': formset})

def commission_update(request, pk):
    commission = get_object_or_404(Commission, pk=pk)
    
    if commission.author != request.user.profile:
        return redirect('commissions:commission_list')
    
    if request.method == 'POST':
        form = CommissionForm(request.POST, instance=commission)
        formset = JobFormSet(request.POST, instance=commission)

        if form.is_valid() and formset.is_valid():
            commission = form.save()
            formset.save()

            if commission.jobs.exclude(status='Full').count() == 0:
                commission.status = 'Full'
                commission.save()

            return redirect('commissions:commission_detail', pk=commission.pk)
    else:
        form = CommissionForm(instance=commission)
        formset = JobFormSet(instance=commission)
    
    ctx = {
    'commission_form': form,
    'job_formset': formset,
    'commission': commission,
    'editing': True
    }

    return render(request, 'commission_form.html', ctx)
    
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    applications = JobApplication.objects.filter(job=job).select_related('applicant')

    is_owner = job.commission.author == request.user.profile

    if request.method == 'POST' and is_owner:
        for application in applications:
            status_key = f'status_{application.id}'
            new_status = request.POST.get(status_key)
            if new_status and new_status != application.status:
                application.status = new_status
                application.save()
        return redirect('commissions:job_detail', job_id=job.id)
    
    ctx = {'job': job,
           'applications': applications,
           'is_owner': is_owner,}

    return render(request, 'job_detail.html', ctx)