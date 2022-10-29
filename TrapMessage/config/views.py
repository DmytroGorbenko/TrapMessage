import time
from braces.views import GroupRequiredMixin

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render

from .utils import SNMPTrap
from .models import Config


@login_required
def send(request, pk):
    config = Config.objects.get(pk=pk)
    config.users.add(request.user)
    trap = SNMPTrap(config.ip, str(config.udp), config.community)

    count = 1
    start_time = time.time()
    for i in range(0, count):
        trap.send()
    end_time = time.time()
    send_time = (end_time - start_time) / count
    traps_per_sec = count / (end_time - start_time)

    context = {"name": config.name,
               "ip": config.ip,
               "udp": config.udp,
               "community": config.community,
               "time": send_time,
               "traps": traps_per_sec,
               "message": "SNMP Trap Test: Trap-message was sent successfully!"}

    return render(request, template_name="config/send.html", context=context)


@login_required
def send_list(request):
    context = {'configs': request.user.configs.all()}
    return render(request, template_name="config/send_list.html", context=context)


class ConfigListView(LoginRequiredMixin, ListView):
    model = Config
    context_object_name = 'configs'
    template_name = "config/config_list.html"


class ConfigDetailView(LoginRequiredMixin, DetailView):
    model = Config
    context_object_name = 'config'
    template_name = "config/config_details.html"


class ConfigCreateView(GroupRequiredMixin, CreateView):
    group_required = u"mod"
    model = Config
    fields = ['name', 'ip', 'udp', 'community']
    template_name = "config/config_create.html"
    success_url = reverse_lazy('config:config_list')


class ConfigUpdateView(GroupRequiredMixin, UpdateView):
    group_required = u"mod"
    model = Config
    context_object_name = 'config'
    fields = ['name', 'ip', 'udp', 'community']
    template_name = "config/config_update.html"


class ConfigDeleteView(GroupRequiredMixin, DeleteView):
    group_required = u"mod"
    model = Config
    context_object_name = 'config'
    success_url = reverse_lazy('config:config_list')
