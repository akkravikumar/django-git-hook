from django.conf.urls import url

from . import views

urlpatterns = [
	# url(r'^viewmain/$', views.indexhome, name='indexhome'),
	url(r'^login_auth/$', views.indexhome, name='indexhome'),
	url(r'^authenticate/$', views.authenticate, name='authenticate'),
	url(r'^add_ui_bug$', views.addUiBug, name='add_ui_bug'),
	url(r'^deletebug$', views.deleteBug, name='deletebug'),
	url(r'^read_bugs$',views.readBugs, name='readbugs'),
	url(r'^$', views.index, name='index')
]
