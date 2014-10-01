from django.conf.urls import patterns, url, include
from django.views.generic.base import TemplateView
from tm.views import Home, ShoppingBag,RegistrationView,activate,category
from tm.forms import UserAuthenticationForm

urlpatterns = patterns('',
                       url(r'^$', Home.as_view(), name='home'),
                       url(r'^shopping-bag/$', ShoppingBag.as_view(), name='shopping-bag'),
                       #url(r'^accounts/', include('registration.backends.default.urls'),name='accounts'),
                       url(r'^accounts/register/$',RegistrationView.as_view(),name='registration_register'),
                       url(r'^register/complete/$',TemplateView.as_view(template_name='registration/registration_complete.html'),name='registration_complete'),
                       url(r'^activate/(?P<activation_key>\w+)/$', activate, name='registration_activate'),
                       url(r'^activation/complete/$', TemplateView.as_view(template_name="registration/activation_complete.html"), name='registration_activation_complete'),
                       url(r'^login/$', 'django.contrib.auth.views.login',{'template_name': 'registration/login.html', 'authentication_form': UserAuthenticationForm}, name='auth_login'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout',{'template_name': 'registration/logout.html'}, name='auth_logout'),
                       url(r'^password_reset/$', 'django.contrib.auth.views.password_reset',name='auth_password_reset'),
                       url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done',name='auth_password_reset_done'),
                       url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$','django.contrib.auth.views.password_reset_confirm',name='auth_password_reset_confirm'),
                       url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete',name='auth_password_reset_complete'),
                       url(r'^category/$', category,name='category'),
                        )