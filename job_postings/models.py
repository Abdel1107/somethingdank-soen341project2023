from django.db import models


# Create your models here.
class JobPosting(models.Model):
    JOB_TYPE_CHOICES = [('Full-time', 'Full-time'), ('Part-time', 'Part-time'), ('Contract', 'Contract'),
                        ('Temporary', 'Temporary'), ('Volunteer', 'Volunteer'), ('Internship', 'Internship'),
                        ('Other', 'Other')]

    JOB_CATEGORY_CHOICES = {('Education', 'Education'), ('Business', 'Business'), ('Healthcare', 'Healthcare'),
                            ('Technology', 'Technology'), ('Arts and entertainment', 'Arts and entertainment'),
                            ('Other', 'Other')}

    job_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    job_type = models.CharField(max_length=255, choices=JOB_TYPE_CHOICES)
    job_category = models.CharField(max_length=255, choices=JOB_CATEGORY_CHOICES)
    location = models.CharField(max_length=255)
    salary = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    application_deadline = models.DateField()
    contact_info = models.CharField(max_length=255)

    def __str__(self):
        return self.title