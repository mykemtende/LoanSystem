from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings

from . import views
from . import views_admin

from . import views_home
from . import views_message
from . import views_profile
from . import views_detail
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns(
    '',
    url(r'^$', views_home.welcome_view, name='welcome'),
    url(r'^login/$', views_home.login_view, name='index'),
    url(r'^logout/$', views_home.logout_view, name='logout'),
    url(r'^register/$', views_home.register_view, name='register'),
    url(r'^setup/$', views_home.setup_view, name='setup'),
    url(r'^approval/$', views_home.approval_view, name='approval'),

    url(r'^error/denied/$', views_home.error_denied_view, name='error/denied'),

    url(r'^admin/users/$', views_admin.users_view, name='admin/users'),
    url(r'^admin/createemployee/$', views_admin.createemployee_view, name='admin/createemployee'),
    url(r'^admin/add_organization/$', views_admin.add_organization_view, name='admin/add_organization'),

    url(r'^message/list/$', views_message.list_view, name='message/list'),
    url(r'^message/new/$', views_message.new_view, name='message/new'),


    url(r'^profile/$', views_profile.profile_view, name='profile'),
    url(r'^profile/update/$', views_profile.update_view, name='profile/update'),
    url(r'^profile/password/$', views_profile.password_view, name='profile/password'),
    

    url(r'^customerapproval/$', views_home.customers_view, name='customer'),

    url(r'^loan/$', views.loan, name='loan'),
    url(r'^detail/list/$', views_detail.list_view, name='detail/list'),
    url(r'^detail/apply/$', views_detail.apply_view, name='detail/apply'),
    url(r'^detail/loanapplicationform/$', views_detail.apply_view, name='detail/loanapplicationform'),
) 