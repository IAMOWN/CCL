from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import (
    Tag,
    CosmicAuthor,
    LibraryRecord,
    DiscourseSeries,
)

from .forms import (
    CreateTagForm,
    UpdateTagForm,
    CreateDiscourseSeriesForm,
    UpdateDiscourseSeriesForm,
    CreateCosmicAuthorForm,
    UpdateCosmicAuthorForm,
    CreateLibraryRecordForm,
    UpdateLibraryRecordForm,
)


# FUNCTIONS
def get_current_year():
    return datetime.now().year


# ####################### TAG VIEWS #######################
class TagList(LoginRequiredMixin, ListView):
    model = Tag
    template_name = 'library/tags.html'
    context_object_name = 'tags'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = get_current_year()
        context['title'] = 'Library Record Tags'

        return context


# ####################### Tag - Detail View #######################
class TagDetail(LoginRequiredMixin, DetailView):
    model = Tag
    template_name = 'library/tag_detail.html'
    context_object_name = 'tag'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = get_current_year()
        context['title'] = f"Tag: {Tag.objects.get(pk=self.kwargs['pk'])}"

        return context


# ####################### Tag - Create View #######################
class TagCreate(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = CreateTagForm
    template_name = 'library/tag_form.html'
    reverse_lazy('tags')

    def form_valid(self, form):
        message = form.instance.tag
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Tag "{message}" has been added'
        )
        return super(TagCreate, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(TagCreate, self).get_context_data(**kwargs)
        context['page_type'] = 'Create'
        context['year'] = get_current_year()

        return context


# ####################### Tag - Update View #######################
class TagUpdate(LoginRequiredMixin, UpdateView):
    model = Tag
    form_class = UpdateTagForm
    template_name = 'library/tag_form.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TagUpdate, self).get_context_data(**kwargs)
        context['page_type'] = 'Update'
        context['year'] = get_current_year()

        return context


# ####################### Tag - Delete View #######################
class TagDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tag
    template_name = 'library/tag_confirm_delete.html'
    success_url = reverse_lazy('tags')

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(TagDelete, self).get_context_data(**kwargs)
        context['year'] = get_current_year()

        return context


# ####################### DISCOURSE SERIES VIEWS #######################
class DiscourseSeriesList(LoginRequiredMixin, ListView):
    model = DiscourseSeries
    template_name = 'library/discourse_series.html'
    context_object_name = 'discourse_series'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = get_current_year()
        context['title'] = 'Library Record Discourse Series Titles'

        return context


# ####################### Discourse Series - Detail View #######################
class DiscourseSeriesDetail(LoginRequiredMixin, DetailView):
    model = DiscourseSeries
    template_name = 'library/discourse_series_detail.html'
    context_object_name = 'discourse_series'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = get_current_year()
        context['title'] = f"Discourse Series: {DiscourseSeries.objects.get(pk=self.kwargs['pk'])}"

        return context


# ####################### Discourse Series - Create View #######################
class DiscourseSeriesCreate(LoginRequiredMixin, CreateView):
    model = DiscourseSeries
    form_class = CreateDiscourseSeriesForm
    template_name = 'library/discourse_series_form.html'

    def form_valid(self, form):
        message = form.instance.discourse_series
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Discourse Series "{message}" has been added'
        )
        return super(DiscourseSeriesCreate, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(DiscourseSeriesCreate, self).get_context_data(**kwargs)
        context['page_type'] = 'Create'
        context['year'] = get_current_year()

        return context


# ####################### Discourse Series - Update View #######################
class DiscourseSeriesUpdate(LoginRequiredMixin, UpdateView):
    model = DiscourseSeries
    form_class = UpdateDiscourseSeriesForm
    template_name = 'library/discourse_series_form.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DiscourseSeriesUpdate, self).get_context_data(**kwargs)
        context['page_type'] = 'Update'
        context['year'] = get_current_year()

        return context


# ####################### Discourse Series - Delete View #######################
class DiscourseSeriesDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = DiscourseSeries
    template_name = 'library/discourse_series_confirm_delete.html'
    success_url = reverse_lazy('discourse-series')

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(DiscourseSeriesDelete, self).get_context_data(**kwargs)
        context['year'] = get_current_year()

        return context


# ####################### COSMIC AUTHOR VIEWS #######################
class CosmicAuthorList(LoginRequiredMixin, ListView):
    model = CosmicAuthor
    template_name = 'library/authors.html'
    context_object_name = 'authors'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = get_current_year()
        context['title'] = 'Cosmic Authors'

        return context


# ####################### Cosmic Author - Detail View #######################
class CosmicAuthorDetail(LoginRequiredMixin, DetailView):
    model = CosmicAuthor
    template_name = 'library/author_detail.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = get_current_year()
        context['title'] = f"Cosmic Author: {CosmicAuthor.objects.get(pk=self.kwargs['pk'])}"

        return context


# ####################### Cosmic Author - Create View #######################
class CosmicAuthorCreate(LoginRequiredMixin, CreateView):
    model = CosmicAuthor
    form_class = CreateCosmicAuthorForm
    template_name = 'library/author_form.html'

    def form_valid(self, form):
        message = form.instance.author
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Cosmic Author "{message}" has been added'
        )
        return super(CosmicAuthorCreate, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(CosmicAuthorCreate, self).get_context_data(**kwargs)
        context['page_type'] = 'Create'
        context['year'] = get_current_year()

        return context


# ####################### Cosmic Author - Update View #######################
class CosmicAuthorUpdate(LoginRequiredMixin, UpdateView):
    model = CosmicAuthor
    form_class = UpdateCosmicAuthorForm
    template_name = 'library/author_form.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CosmicAuthorUpdate, self).get_context_data(**kwargs)
        context['page_type'] = 'Update'
        context['year'] = get_current_year()

        return context


# ####################### Cosmic Author - Delete View #######################
class CosmicAuthorDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CosmicAuthor
    template_name = 'library/author_confirm_delete.html'
    success_url = reverse_lazy('authors')

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(CosmicAuthorDelete, self).get_context_data(**kwargs)
        context['year'] = get_current_year()

        return context


# ####################### LIBRARY RECORD VIEWS #######################
class LibraryRecordList(ListView):
    model = LibraryRecord
    template_name = 'library/library_records.html'
    context_object_name = 'library_records'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = get_current_year()
        context['title'] = 'Library Records'

        return context


# ####################### Cosmic Author - Detail View #######################
class LibraryRecordDetail(DetailView):
    model = LibraryRecord
    template_name = 'library/library_record_detail.html'
    context_object_name = 'library_record'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = get_current_year()
        context['title'] = f"Library Record: {LibraryRecord.objects.get(pk=self.kwargs['pk'])}"

        return context


# ####################### Cosmic Author - Create View #######################
class LibraryRecordCreate(LoginRequiredMixin, CreateView):
    model = LibraryRecord
    form_class = CreateLibraryRecordForm
    template_name = 'library/library_record_form.html'

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.year_communicated = form.instance.date_communicated.year
        form.save()

        message = form.instance.title
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Library Record "{message}" has been added'
        )
        return super(LibraryRecordCreate, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(LibraryRecordCreate, self).get_context_data(**kwargs)
        context['page_type'] = 'Create'
        context['year'] = get_current_year()

        return context


# ####################### Cosmic Author - Update View #######################
class LibraryRecordUpdate(LoginRequiredMixin, UpdateView):
    model = LibraryRecord
    form_class = UpdateLibraryRecordForm
    template_name = 'library/library_record_form.html'

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.year_communicated = form.instance.date_communicated.year
        form.save()

        message = form.instance.title
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'The Library Record "{message}" has been updated'
        )
        return super(LibraryRecordUpdate, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(LibraryRecordUpdate, self).get_context_data(**kwargs)
        context['page_type'] = 'Update'
        context['year'] = get_current_year()

        return context


# ####################### Cosmic Author - Delete View #######################
class LibraryRecordDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = LibraryRecord
    template_name = 'library/library_record_confirm_delete.html'
    success_url = reverse_lazy('library_records')

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(LibraryRecordDelete, self).get_context_data(**kwargs)
        context['year'] = get_current_year()

        return context
