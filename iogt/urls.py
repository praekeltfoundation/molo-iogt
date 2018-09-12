import os

from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django_cas_ng import views as cas_views
from wagtail.contrib.wagtailsitemaps.views import sitemap
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls
from molo.profiles.views import RegistrationDone
from molo.profiles.forms import DoneForm

from iogt.views import health_iogt


urlpatterns = []
# implement CAS URLs in a production setting
if settings.ENABLE_SSO:
    urlpatterns += [
        url(r'^admin/login/', cas_views.login),
        url(r'^admin/logout/', cas_views.logout),
        url(r'^admin/callback/', cas_views.callback),
    ]


urlpatterns += [
    url(r'^django-admin/', include(admin.site.urls)),
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^meta/', include('molo.usermetadata.urls',
        namespace='molo.usermetadata', app_name='molo.usermetadata')),
    url(r'^profiles/register/done/',
        login_required(RegistrationDone.as_view(
            template_name="profiles/done.html",
            form_class=DoneForm
        )),
        name='registration_done'),
    url(r'^profiles/', include('molo.profiles.urls',
        namespace='molo.profiles')),
    url(r'^commenting/', include('molo.commenting.urls',
        namespace='molo.commenting', app_name='molo.commenting')),
    url(r'', include('django_comments.urls')),
    url(r'^commenting/comment_done/',
        TemplateView.as_view(template_name="comments/comment_done.html"),
        name='comment_done'),
    url(r'^surveys/', include('molo.surveys.urls',
        namespace='molo.surveys', app_name='molo.surveys')),
    url(r'^polls/', include('molo.polls.urls',
        namespace='molo.polls', app_name='molo.polls')),
    url('^', include('django.contrib.auth.urls')),
    url(r'^robots\.txt$', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain')),
    url(r'^sitemap\.xml$', sitemap),
    url(r'^health/$', health_iogt, name='health_iogt'),
    url(r'', include('molo.core.urls')),
    url(r'', include(wagtail_urls)),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL + 'images/',
        document_root=os.path.join(settings.MEDIA_ROOT, 'images'))
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
