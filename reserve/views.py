# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from .forms import *
from .models import *
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePageView(TemplateView):
    template_name = 'reserve/homepage.html'


class ContactView(TemplateView):
    template_name = 'reserve/contact.html'


class AboutView(TemplateView):
    template_name = 'reserve/about.html'


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('reserve:homepage'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SignUpForm()
        return context

    def post(self, request, *args, **kwargs):

        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return HttpResponseRedirect(reverse('reserve:signup_done'))

        return render(request, self.template_name, {'form': form})


class SignUpDoneView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login/'
    redirect_field_name = None
    raise_exception = False
    template_name = 'registration/signup_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username
        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login/'
    redirect_field_name = None
    raise_exception = False
    template_name = 'registration/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class EditView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login/'
    redirect_field_name = None
    raise_exception = False
    template_name = 'registration/edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProfileForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = Profile.objects.get(user__pk=self.request.user.pk)
            profile.user.first_name = form.cleaned_data.get('firstname')
            profile.user.last_name = form.cleaned_data.get('lastname')
            profile.user.email = form.cleaned_data.get('email')
            profile.phone = form.cleaned_data.get('phone')
            profile.birth_date = form.cleaned_data.get('birth_date')
            profile.save()
            profile.user.save()

            return HttpResponseRedirect(reverse('reserve:profile'))

        return render(request, self.template_name, {'form': form})


class SearchView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login/'
    redirect_field_name = None
    raise_exception = False
    template_name = 'reserve/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BookForm()
        return context

    def post(self, request, *args, **kwargs):
        form = BookForm(request.POST)
        if form.is_valid():
            data = {}
            for key in form.cleaned_data:
                if form.cleaned_data[key] is not None:
                    data.update({key: form.cleaned_data[key]})
            if not data['authors__in'].exists():
                del data['authors__in']
            books = Book.objects.filter(**data).distinct()
            context = super().get_context_data(**kwargs)
            context['books'], context['form'], context['method'] = books, form, request.method
            return render(request, self.template_name, context)

        else:
            return render(request, self.template_name, {'form': form})


class DetailsView(LoginRequiredMixin, DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = None
    template_name = 'reserve/details.html'
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
