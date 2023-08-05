# -*- coding: utf-8 -*-
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from formidable.models import Formidable
from django.core.urlresolvers import reverse
from formidable.accesses import get_accesses


class FormidableListView(ListView):

    model = Formidable

    def get_context_data(self):
        context = super(FormidableListView, self).get_context_data()
        context['roles'] = get_accesses()
        return context


class FormidableDetailView(DetailView):

    model = Formidable

    def dispatch(self, request, *args, **kwargs):
        request.session['role'] = kwargs['role']
        return super(FormidableDetailView, self).dispatch(
            request, *args, **kwargs
        )


class FormidableUpdateView(UpdateView):

    model = Formidable
    fields = ['label', 'description']

    def get_success_url(self):
        return reverse('builder:formidable-list')


class FormidableBuilderView(DetailView):

    template_name = 'formidable/formidable_builder.html'
    model = Formidable
