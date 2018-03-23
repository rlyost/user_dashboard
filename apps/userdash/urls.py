from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='in'),
    url(r'^register$', views.register, name='reg'),
    url(r'^dashboard$', views.dashboard, name='dash'),
    url(r'^dashboard/admin$', views.admin, name='admin'),
    url(r'^signin$', views.signin, name='sign'),
    url(r'^users/show/(?P<id>\d+)$', views.show, name='ushow'),
    url(r'^users/new$', views.new, name='unew'),
    url(r'^users/edit/(?P<id>\d+)$', views.aedit, name='aedit'),
    url(r'^users/edit$', views.uedit, name='uedit'),
    url(r'^create$', views.create, name='ucreate'),
    url(r'^update$', views.update, name='uupdate'),
    url(r'^destroy/(?P<id>\d+)$', views.destroy, name='udestroy'),
]