from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='in'),
    url(r'^register$', views.register, name='reg'),
    url(r'^register_val$', views.register_val, name='regval'),
    url(r'^dashboard$', views.dashboard, name='dash'),
    url(r'^signin$', views.signin, name='sign'),
    url(r'^signin_val$', views.signin_val, name='signval'),
    url(r'^users/show/(?P<id>\d+)$', views.show, name='ushow'),
    url(r'^users/new$', views.new, name='unew'),
    url(r'^users/edit/(?P<id>\d+)$', views.edit, name='edit'),
    url(r'^users/profile$', views.profile, name='profile'),
    url(r'^change$', views.change, name='pwchange'),
    url(r'^update$', views.update, name='uupdate'),
    url(r'^save$', views.save, name='usave'),
    url(r'^destroy/(?P<id>\d+)$', views.destroy, name='udestroy'),
    url(r'^logoff$', views.logoff, name='ulogoff'),
    url(r'^post_msg$', views.post_msg, name='post_msg'),
    url(r'^post_cmt', views.post_cmt, name='post_cmt'),
]