from django.conf.urls import url
from . import views
from search import views as views_search

app_name = 'users'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^logout/$', views.logout_user_view, name='logout'),
    url(r'^login/$', views.UserLoginFormView.as_view(), name='login'),
    url(r'^userinfo/$', views.user_info, name='user-info'),
    url(r'^userinfo/update/$', views.user_info_update, name='user-info-update'),
    url(r'^userinfo/changepassword/$', views.user_info_change_password, name='user-info-change-password'),
]
