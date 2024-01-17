from django.shortcuts import render, redirect,HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from .models import Slider, Service, Doctor, Faq, Gallery
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DetailView, TemplateView
from django.core.mail import send_mail
from django.contrib import messages
from .models import Slider, Service, Doctor, Faq, Gallery

class CustomLoginView(LoginView):
    template_name = 'admin/login.html'
    success_message = "You have successfully logged in."
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Invalid username or password.")
        return response

class HomeView(LoginRequiredMixin, ListView):
    template_name = 'hospital/index.html'
    queryset = Service.objects.all()
    context_object_name = 'services'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['sliders'] = Slider.objects.all()
        context['experts'] = Doctor.objects.all()
        return context

    # Add this method to handle the login form on the home page
    def post(self, request, *args, **kwargs):
        # Assume you have a login form on the home page, handle it here
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in.")
        else:
            messages.error(request, "Invalid username or password.")
        
        return redirect('home')



class ServiceListView(ListView):
    queryset = Service.objects.all()
    template_name = "hospital/services.html"


class ServiceDetailView(DetailView):
    queryset = Service.objects.all()
    template_name = "hospital/service_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["services"] = Service.objects.all()
        return context


class DoctorListView(ListView):
    template_name = 'hospital/team.html'
    queryset = Doctor.objects.all()
    paginate_by = 8


class DoctorDetailView(DetailView):
    template_name = 'hospital/team-details.html'
    queryset = Doctor.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doctors"] = Doctor.objects.all()
        return context


class FaqListView(ListView):
    template_name = 'hospital/faqs.html'
    queryset = Faq.objects.all()


class GalleryListView(ListView):
    template_name = 'hospital/gallery.html'
    queryset = Gallery.objects.all()
    paginate_by = 9


class ContactView(TemplateView):
    template_name = "hospital/contact.html"

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if subject == '':
            subject = "Heartcare Contact"

        if name and message and email and phone:
            send_mail(subject+"-"+phone,message,email,['rushikeshpawar638@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, " Email hasbeen sent successfully...")

        return redirect('contact')
