from django.conf.urls import patterns, url

from notebooks import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^twitter_license', views.twitter_license, name='twitter_license'),
    url(r'^ipython_license', views.ipython_license, name='ipython_license'),
    url(r'^django_license', views.django_license, name='django_license'),
    url(r'^add_notebook', views.add_notebook, name='add_notebook'),
    url(r'^register', views.register, name='register'),
    url(r'^user_login', views.user_login, name='user_login'),
    url(r'^user_logout', views.user_logout, name='user_logout'),
    url(r'^profile_page/(?P<username>\w+)', views.profile_page, name ='profile_page'),
    url(r'^category_page/(?P<category>\w+)', views.category_page, name ='category_page'),
    url(r'^like_notebook', views.like_notebook, name='like_notebook'),
    url(r'^notebook_viewer/(?P<user>\w+)/(?P<id>[\d-]+)/(?P<slug>[\w-]+)', views.notebook_viewer, name ='notebook_viewer')
)