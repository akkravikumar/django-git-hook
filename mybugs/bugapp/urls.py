from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^results/$', views.indexhome, name='indexhome'),
	url(r'^add_ui_bug$', views.addUiBug, name='add_ui_bug'),
	url(r'^read_bugs$',views.readBugs, name='readbugs'),
	url(r'^deletebug$', views.deleteBug, name='deletebug'),
	url(r'^$', views.index, name='index')
]
