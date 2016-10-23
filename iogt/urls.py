import os

from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls
from molo.profiles.views import RegistrationDone
from molo.profiles.forms import DateOfBirthForm


# implement CAS URLs in a production setting
if settings.ENABLE_SSO:
    urlpatterns = patterns(
        '',
        url(r'^admin/login/', 'django_cas_ng.views.login'),
        url(r'^admin/logout/', 'django_cas_ng.views.logout'),
        url(r'^admin/callback/', 'django_cas_ng.views.callback'),
    )
else:
    urlpatterns = patterns('', )

urlpatterns += patterns(
    '',
    url(r'^django-admin/', include(admin.site.urls)),
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^meta/', include('molo.usermetadata.urls',
                           namespace='molo.usermetadata',
                           app_name='molo.usermetadata')),

    url(r'^profiles/register/done/',
        login_required(RegistrationDone.as_view(
            template_name="profiles/done.html",
            form_class=DateOfBirthForm
        )),
        name='registration_done'),
    url(r'^profiles/', include('molo.profiles.urls',
        namespace='molo.profiles')),

    url(r'^commenting/', include('molo.commenting.urls',
        namespace='molo.commenting',
        app_name='molo.commenting')),

    url(r'', include('django_comments.urls')),

    url(r'^commenting/comment_done/',
        TemplateView.as_view(
            template_name="comments/comment_done.html"
        ),
        name='comment_done'),

    url(r'^polls/', include('molo.polls.urls',
                            namespace='molo.polls',
                            app_name='molo.polls')),
    url('^', include('django.contrib.auth.urls')),
    url(r'', include('molo.core.urls')),
    url(r'', include(wagtail_urls)),
)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL + 'images/',
        document_root=os.path.join(settings.MEDIA_ROOT, 'images'))
