from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import LoginForm, CustomUserCreationForm, EditUserForm, EditAdminForm


class UserListView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = 'users'
    template_name = "users/user_list.html"


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'member'
    template_name = 'users/user_detail.html'


class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    template_name = "users/user_create.html"
    success_url = reverse_lazy('users:user_list')
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        response = super(UserCreateView, self).form_valid(form)
        if response:
            if form.cleaned_data['group'] == "Користувач":
                group = Group.objects.get(name='Користувач')
            else:
                group = Group.objects.get(name='Модератор')
            group.user_set.add(self.object)
        return response


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    context_object_name = 'member'
    template_name = "users/user_update.html"
    form_class = EditUserForm
    success_url = reverse_lazy('users:user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['index'] = self.object.id
        return context

    def form_valid(self, form):
        response = super(UserUpdateView, self).form_valid(form)
        if response:
            self.object.groups.clear()
            if form.cleaned_data['group'] == "Користувач":
                group = Group.objects.get(name='Користувач')
            else:
                group = Group.objects.get(name='Модератор')
            group.user_set.add(self.object)
        return response


class AdminUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    context_object_name = 'member'
    template_name = "users/user_update.html"
    form_class = EditAdminForm
    success_url = reverse_lazy('users:user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['index'] = self.object.id
        return context


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    context_object_name = 'member'
    success_url = reverse_lazy('users:user_list')
    template_name = 'users/user_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['index'] = self.object.id
        return context


class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        post_data = form.cleaned_data
        user = authenticate(username=post_data['username'],
                            password=post_data['password'])
        if user is not None:
            login(self.request, user)

            if user.is_staff:
                return HttpResponseRedirect(reverse_lazy('users:user_list'))
            else:
                return HttpResponseRedirect(reverse_lazy('config:config_list'))

        else:
            messages.error(self.request, 'Невірний логін чи пароль. Спробуйте знов.')
            return HttpResponseRedirect(reverse_lazy('users:login'))


@login_required
@staff_member_required
def password_change(request, pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Пароль було успішно змінено!")
            return redirect('users:user_details', pk)
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'users/password_reset_confirm.html', {'form': form, 'index': pk})
