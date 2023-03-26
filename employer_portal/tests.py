from django.test import TestCase
from django.contrib.auth.models import User
from job_postings.models import JobPosting


# Create your tests here.
class AddJobPostingTestCase(TestCase):
    def test_add_job_posting(self):
        # create a test user and log them in
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        # call the view function that adds a job posting
        response = self.client.post('/create_job_posting/', {
            'title': 'Test Job',
            'company_name': 'Test Company',
            'job_type': 'Full-time',
            'job_category': 'Technology',
            'location': 'Test Location',
            'salary': 'Test Salary',
            'description': 'Test Description',
            'requirements': 'Test Requirements',
            'application_deadline': '2023-04-01',
            'contact_info': 'Test Contact Info',
        })

        # assert that the job posting was created successfully
        self.assertEqual(response.status_code, 302)
        self.assertEqual(JobPosting.objects.count(), 1)
        job_posting = JobPosting.objects.first()
        self.assertEqual(job_posting.title, 'Test Job')
        self.assertEqual(job_posting.employer, user)