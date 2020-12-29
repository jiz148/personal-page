from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class OwnerListView(ListView):
    """
    Sub-class the List View for owners
    """
    pass


class OwnerDetailView(DetailView):
    """
    Sub-class the Detail View for owners
    """
    pass


class OwnerCreateView(LoginRequiredMixin, CreateView):
    """
    Sub-class the Create View for owners
    """

    # Saves the form instance, sets the current object for the view, and redirects to get_success_url().
    def form_valid(self, form):
        o = form.save(commit=False)
        o.owner = self.request.user
        o.save()
        return super().form_valid(form)


class OwnerUpdateView(LoginRequiredMixin, UpdateView):
    """
    Sub-class the Update View for owners
    """
    pass


class OwnerDeleteView(LoginRequiredMixin, DeleteView):
    """
    Sub-class the Delete View for owners
    restrict a User from deleting other user's data.
    """

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)
