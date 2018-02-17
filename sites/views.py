from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView

from sites.models import Site
from sites.services import SummaryService


class SiteList(ListView):
    template_name = 'sites/list.html'
    context_object_name = 'sites'
    model = Site


class SiteDetail(DetailView):
    template_name = 'sites/detail.html'
    context_object_name = 'site'
    model = Site


class SummaryBase(TemplateView):
    template_name = 'sites/summary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aggregated_data'] = self.get_aggregated_data()
        return context

    def get_aggregated_data(self):
        """Should return the iterable of dicts
        i.e [{'site_name': "Demo Site", "agg_value_a": 12.0, "agg_value_b": 23.0}]
        """
        raise NotImplementedError


class Summary(SummaryBase):
    def get_aggregated_data(self):
        return SummaryService().get_summary_data()


class SummaryAverage(SummaryBase):
    def get_aggregated_data(self):
        return SummaryService().get_average_data()

