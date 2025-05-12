from django.db import models
from django.urls import reverse
from user_management.models import Profile

class Commission(models.Model):
    
    STATUS_CHOICES=[
        ('Open', 'Open'),
        ('Full', 'Full'),
        ('Completed', 'Completed'),
        ('Discontinued', 'Discontinued'),
    ]
           
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="Open")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    def get_absolute_url(self):
        return reverse('commissions:commission_detail', args=[self.pk])
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['created_on']
    
class Job(models.Model):
    
    STATUS_CHOICES=[
        ('Open', 'Open'),
        ('Full', 'Full'),
    ]
    
    commission = models.ForeignKey(Commission, on_delete=models.CASCADE, related_name="jobs")
    role = models.CharField(max_length=255)
    manpower_required = models.IntegerField()
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, default="Open")
    
    class Meta:
        ordering = [
            models.Case(
                models.When(status='Open', then=0),
                models.When(status='Full', then=1),
                default=2,
                output_field=models.IntegerField(),
            ),
            '-manpower_required',
            'role',
        ]
        
class JobApplication(models.Model):
    
    STATUS_CHOICES=[
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="applications")
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='Pending')
    applied_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = [
                models.Case(
                    models.When(status = 'Pending', then=0),
                    models.When(status = 'Accepted', then=1),
                    models.When(status = 'Rejected', then=2),
                    default=3,
                    output_field=models.IntegerField()            
                ),
                '-applied_on',
            ]