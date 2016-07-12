from molo.polls import views

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required


urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(
        r'^(?P<poll_id>\d+)/results/$',
        views.poll_results,
        name='results'
    ),
    url(r'^(?P<question_id>\d+)/vote/$',
        login_required(views.VoteView.as_view()),
        name='vote'),
    url(r'^(?P<question_id>\d+)/freetextvote/$',
        login_required(views.FreeTextVoteView.as_view()),
        name='free_text_vote'),
)
