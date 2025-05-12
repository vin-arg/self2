from django import forms
from .models import Commission, JobApplication, Job
from django.forms import inlineformset_factory

class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ['title', 'description', 'status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['role', 'manpower_required', 'status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

JobFormSet = inlineformset_factory(
    Commission,
    Job,
    form=JobForm,
    extra=1
)