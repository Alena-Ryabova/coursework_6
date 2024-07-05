from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from postmails.forms import MailingForm, MessageForm, ManagerMailingForm
from postmails.models import Mailing, Message
from postmails.services import get_mailing_from_cache


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'postmails/mailing_list.html'

    def get_queryset(self):
        # queryset = super().get_queryset()
        return get_mailing_from_cache()


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'postmails/mailing.html'


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('postmails:mailing_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        return self.object

    def get_success_url(self):
        return reverse('postmails:mailing', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        MessageFormset = inlineformset_factory(Mailing, Message, form=MessageForm, extra=1)

        if self.request.method == 'POST':
            context_data['formset'] = MessageFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = MessageFormset(instance=self.object)

        return context_data

    def get_form_class(self):
        user = self.request.user
        if self.object.owner == user or user.is_superuser is True:
            return MailingForm
        elif user.groups.filter(name='moderators').exists():
            return ManagerMailingForm
        else:
            raise Http404("Доступ запрещен")


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('postmails:mailing_list')

    def test_func(self):
        return self.request.user.is_superuser