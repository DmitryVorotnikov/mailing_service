from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from blog.models import Article


class BlogListView(ListView):
    model = Article

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(is_published=True)

        return queryset


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Article

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)

        # Увеличение счетчика просмотров
        self.object.number_of_views += 1
        self.object.save()

        return self.object
