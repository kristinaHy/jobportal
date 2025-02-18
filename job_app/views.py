from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm

from django.db.models import Q

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LogoutView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Job, Application, JobCategory
from .forms import JobForm, ApplicationForm


class JobListView(ListView):
    model = Job
    template_name = 'job_list.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        queryset = Job.objects.filter(is_active=True).order_by('-posted_on')
        
        # Apply search
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
            
        # Apply filters
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
            
        job_type = self.request.GET.get('job_type')
        if job_type:
            queryset = queryset.filter(job_type=job_type)
            
        experience_level = self.request.GET.get('experience_level')
        if experience_level:
            queryset = queryset.filter(experience_level=experience_level)
            
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all()
        context['job_types'] = Job.JOB_TYPES
        context['experience_levels'] = Job.EXPERIENCE_LEVELS
        return context


class JobDetailView(DetailView):
    model = Job
    template_name = 'job_detail.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['has_applied'] = Application.objects.filter(
                job=self.object, 
                applicant=self.request.user
            ).exists()
        return context

class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = 'post_job.html'
    success_url = reverse_lazy('job_list')

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        messages.success(self.request, 'Job posted successfully!')
        return super().form_valid(form)

class JobUpdateView(LoginRequiredMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'post_job.html'
    success_url = reverse_lazy('job_list')

    def form_valid(self, form):
        messages.success(self.request, 'Job updated successfully!')
        return super().form_valid(form)

class JobDeleteView(LoginRequiredMixin, DeleteView):
    model = Job
    template_name = 'job_confirm_delete.html'
    success_url = reverse_lazy('job_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Job deleted successfully!')
        return super().delete(request, *args, **kwargs)

class ApplyJobView(LoginRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'apply_job.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = get_object_or_404(Job, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        job = get_object_or_404(Job, pk=self.kwargs['pk'])
        form.instance.job = job
        form.instance.applicant = self.request.user
        messages.success(self.request, 'Application submitted successfully!')
        return super().form_valid(form)


    def get_success_url(self):
        job_id = self.kwargs['pk']
        return reverse_lazy('job_detail', kwargs={'pk': job_id})





class ApplicantsListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'job_app/applicants_list.html'
    context_object_name = 'applications'

    def get_queryset(self):
        job = get_object_or_404(Job, pk=self.kwargs['pk'])
        return Application.objects.filter(job=job)

class ViewApplicantView(LoginRequiredMixin, DetailView):
    model = Application
    template_name = 'job_app/view_applicants.html'
    context_object_name = 'application'

def signup(request):
    return render(request, 'registration/signup.html')

@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'profile_edit.html', {
        'form': form,
        'csrf_token': request.META.get('CSRF_COOKIE')
    })







def update_application_status(request, pk):
    if request.method == 'POST':
        application = get_object_or_404(Application, pk=pk)
        new_status = request.POST.get('status')
        if new_status in dict(Application.STATUS_CHOICES).keys():
            application.status = new_status
            application.save()
            messages.success(request, 'Application status updated successfully!')
        else:
            messages.error(request, 'Invalid status selected')
        return redirect('applicants_list', pk=application.job.id)
