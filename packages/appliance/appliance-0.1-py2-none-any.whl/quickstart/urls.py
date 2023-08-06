from django.conf.urls import url
import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    url(r'^api/v1/books/$', views.book_list),
    url(r'^api/v1/appliances/$', views.appliances),
    url(r'^api/v1/appliances/(?P<appliance_id>[0-9]+)/$', views.appliances),
    url(r'^api/v1/books/(?P<pk>[0-9]+)/$', views.book_list),
    url(r'^api/v1/doc/$', views.index),
]

urlpatterns = format_suffix_patterns(urlpatterns)
