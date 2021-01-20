from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType

# Create your views here.
from django.urls import reverse_lazy
from django.utils.datetime_safe import date
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView
from django_datatables_view.base_datatable_view import BaseDatatableView

from django import forms
from .models import Event


class EventListView(LoginRequiredMixin, TemplateView):
    template_name = 'event/list.html'


class EventListJson(LoginRequiredMixin, BaseDatatableView):
    columns = ['id', 'title', 'description', 'date', 'owner', 'participants']
    order_columns = ['id', 'title', 'description', 'date', 'owner', 'participants']
    max_display_length = 30

    def render_column(self, row, column):
        if column == 'participants':
            return str(row.participants_count())
        else:
            return super().render_column(row, column)

    def get_initial_queryset(self):
        today = date.today()
        data = Event.objects.extra(select={'now': 'date = %s',
                                           'upcoming': 'date > %s',
                                           'gone': 'date < %s'},
                                   select_params=(today, today, today),
                                   order_by=['-now', '-upcoming', '-gone', 'date'])
        return data

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(date__icontains=search) |
                Q(owner__email__icontains=search)
            )
        return qs


class MyEventListView(LoginRequiredMixin, TemplateView):
    template_name = 'event/mylist.html'


class MyEventListJson(LoginRequiredMixin, BaseDatatableView):
    columns = ['id', 'title', 'description', 'date', 'owner', 'participants']
    order_columns = ['id', 'title', 'description', 'date', 'owner', 'participants']
    max_display_length = 30

    def render_column(self, row, column):
        if column == 'participants':
            return str(row.participants_count())
        else:
            return super().render_column(row, column)

    def get_initial_queryset(self):
        # order Event first that equal today and upcoming (tomorrow) and gone (yesterday)
        today = date.today()
        data = Event.objects.extra(select={'now': 'date = %s',
                                           'upcoming': 'date > %s',
                                           'gone': 'date < %s'},
                                   select_params=(today, today, today),
                                   order_by=['-now', '-upcoming', '-gone', 'date']).filter(owner=self.request.user)
        return data

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(date__icontains=search) |
                Q(owner__email__icontains=search)
            )
        return qs


class EventCreateView(LoginRequiredMixin, CreateView):
    fields = ('title', 'description', 'date', 'owner', 'participants')
    model = Event
    template_name = 'event/form.html'

    def get_form(self, form_class=None):
        form = super(EventCreateView, self).get_form()
        form.fields['description'] = forms.CharField(widget=forms.Textarea)
        form.fields['date'] = forms.DateField(widget=forms.SelectDateWidget)
        form.fields['owner'].required = False
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(EventCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        temp = super(EventCreateView, self).post(request, *args, **kwargs)

        if self.object:
            # add permission to access this object
            content_type = ContentType.objects.get(app_label='core', model='event')
            perm = Permission.objects.create(codename='can_create_' + str(self.object.id),
                                             name='Can edit instance with id ' + str(self.object.id),
                                             content_type=content_type)
            self.request.user.user_permissions.add(perm)
        else:
            return temp

        return redirect(self.get_success_url())

    def get_success_url(self):
        if self.request.POST.get('another', None):
            return reverse_lazy('core:event_add')
        return reverse_lazy('core:myevent_list')


class EventDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'event'
    model = Event
    template_name = 'event/detail.html'

    def post(self, request, pk):
        event = Event.objects.get(pk=pk)
        if request.POST.get('signup', None):
            event.participants.add(request.user)
        if request.POST.get('withdraw', None):
            event.participants.remove(request.user)
        event.save()
        return redirect('core:event_list')


class EventUpdateView(LoginRequiredMixin, UpdateView):
    fields = ('title', 'description', 'date', 'owner', 'participants')
    model = Event
    template_name = 'event/form.html'

    def get(self, request, *args, **kwargs):
        # check on permission
        flag = self.request.user.has_perm('core.can_create_' + str(self.get_object().id))
        if flag:
            return super(EventUpdateView, self).get(request, *args, **kwargs)
        else:
            return HttpResponse("You Do not Have Access")

    def post(self, request, *args, **kwargs):
        # check on permission
        flag = self.request.user.has_perm('core.can_create_' + str(self.get_object().id))
        if flag:
            return super(EventUpdateView, self).post(request, *args, **kwargs)
        else:
            return HttpResponse("You Do not Have Access")

    def get_form(self, form_class=None):
        form = super(EventUpdateView, self).get_form()
        form.fields['description'] = forms.CharField(widget=forms.Textarea)
        form.fields['date'] = forms.DateField(widget=forms.SelectDateWidget)
        form.fields['owner'].required = False
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(EventUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('core:myevent_list')

