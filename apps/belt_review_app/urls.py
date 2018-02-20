from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^books$', views.books),
    url(r'^books/(?P<book_id>\d+)$', views.book_id),
    url(r'^users/(?P<user_id>\d+)$', views.user),
    url(r'^books/add$', views.add),
    url(r'^addreview$', views.addreview),
    url(r'^logout$', views.logout),
    url(r'^delete/(?P<review_id>\d+)$', views.delete),
]
