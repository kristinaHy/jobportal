from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_employer = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    @property
    def is_complete(self):
        return all([self.phone_number, self.address, self.skills])

class JobCategory(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Job(models.Model):
    JOB_TYPES = [
        ('FT', 'Full-time'),
        ('PT', 'Part-time'),
        ('CN', 'Contract'),
        ('IN', 'Internship'),
        ('RM', 'Remote'),
    ]

    EXPERIENCE_LEVELS = [
        ('EN', 'Entry Level'),
        ('IN', 'Intermediate'),
        ('SE', 'Senior'),
        ('EX', 'Executive'),
    ]

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    benefits = models.TextField(blank=True)
    location = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    job_type = models.CharField(max_length=2, choices=JOB_TYPES, default='FT')
    experience_level = models.CharField(max_length=2, choices=EXPERIENCE_LEVELS, default='EN')
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True, blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    application_deadline = models.DateField(default=timezone.now)
    views_count = models.PositiveIntegerField(default=0)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=0.0
    )

    def __str__(self):
        return self.title

    def is_expired(self):
        return self.application_deadline < timezone.now().date()

class Application(models.Model):
    STATUS_CHOICES = [
        ('AP', 'Applied'),
        ('RE', 'Reviewed'),
        ('IN', 'Interviewing'),
        ('OF', 'Offered'),
        ('AC', 'Accepted'),
        ('RE', 'Rejected'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='AP')
    applied_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('job', 'applicant')

    def __str__(self):
        return f"{self.applicant.username} applied for {self.job.title}"
