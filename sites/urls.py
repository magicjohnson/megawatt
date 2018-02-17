from django.urls import path, re_path

from sites import views

urlpatterns = [
    path('', views.SiteList.as_view(), name='index'),
    path('sites/', views.SiteList.as_view(), name='site-list'),
    re_path('site/(?P<pk>\w+)/', views.SiteDetail.as_view(), name='site-detail'),
    path('summary/', views.Summary.as_view(), name='summary'),
    path('summary-average/', views.SummaryAverage.as_view(), name='summary-average'),

]


