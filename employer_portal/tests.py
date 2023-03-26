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


class UpdateJobPostingTestCase(TestCase):
    def setUp(self):
        # create a test user and log them in
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        # create a test job posting
        self.job_posting = JobPosting.objects.create(
            title='Test Job',
            employer=self.user,
            company_name='Test Company',
            job_type='Full-time',
            job_category='Technology',
            location='Test Location',
            salary='Test Salary',
            description='Test Description',
            requirements='Test Requirements',
            application_deadline='2023-04-01',
            contact_info='Test Contact Info',
        )

    def test_update_job_posting(self):
        # call the view function that updates the job posting
        response = self.client.post('/update_job_posting/', {
            'job_id': self.job_posting.pk,
            'title': 'Updated Test Job',
            'company_name': 'Updated Test Company',
            'job_type': 'Part-time',
            'job_category': 'Business',
            'location': 'Updated Test Location',
            'salary': 'Updated Test Salary',
            'description': 'Updated Test Description',
            'requirements': 'Updated Test Requirements',
            'application_deadline': '2023-04-02',
            'contact_info': 'Updated Test Contact Info',
        })

        # assert that the job posting was updated successfully
        self.assertEqual(response.status_code, 302)
        self.job_posting.refresh_from_db()
        self.assertEqual(self.job_posting.title, 'Updated Test Job')
        self.assertEqual(self.job_posting.company_name, 'Updated Test Company')
        self.assertEqual(self.job_posting.job_type, 'Part-time')
        self.assertEqual(self.job_posting.job_category, 'Business')
        self.assertEqual(self.job_posting.location, 'Updated Test Location')
        self.assertEqual(self.job_posting.salary, 'Updated Test Salary')
        self.assertEqual(self.job_posting.description, 'Updated Test Description')
        self.assertEqual(self.job_posting.requirements, 'Updated Test Requirements')
        self.assertEqual(str(self.job_posting.application_deadline), '2023-04-02')
        self.assertEqual(self.job_posting.contact_info, 'Updated Test Contact Info')


class DeleteJobPostingTestCase(TestCase):
    def setUp(self):
        # create a test user and a test job posting
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.job_posting = JobPosting.objects.create(
            title='Test Job',
            employer=self.user,
            company_name='Test Company',
            job_type='Full-time',
            job_category='Technology',
            location='Test Location',
            salary='Test Salary',
            description='Test Description',
            requirements='Test Requirements',
            application_deadline='2023-04-01',
            contact_info='Test Contact Info',
        )

    def test_delete_job_posting(self):
        # log in as the test user and delete the test job posting
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(f'/delete_job_posting/{self.job_posting.pk}/')

        # assert that the job posting was deleted successfully
        self.assertEqual(response.status_code, 302)
        self.assertEqual(JobPosting.objects.count(), 0)