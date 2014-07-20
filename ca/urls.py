from django.conf.urls import patterns, url, include
from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView
from ca import views

sqs = SearchQuerySet().facet('degree').facet('university').facet('major').facet('academic_professional')

urlpatterns = patterns('',
        url(r'^$', views.home, name = 'home'),
        url(r'^articles/$', views.articles, name = 'articles'),
        url(r'^article_detail/(?P<article_id>\d+)/$', views.article_detail, name = 'article_detail'),
        url(r'^register/$', views.register, name = 'register'),
        url(r'^login/$', views.user_login, name = 'login'),
        url(r'^logout/$', views.user_logout, name = 'logout'),
        url(r'^profile/$', views.profile, name = 'profile'),
        url(r'^edit_profile/$', views.edit_profile, name = 'edit_profile'),
        url(r'^program_search/', views.search_haystack, name = 'program_search'),
        url(r'^program_detail/(?P<program_id>\d+)/$', views.program_detail, name = 'program_detail'),
        url(r'^add_fav_program', views.add_fav_program, name = 'add_fav_program'),
        url(r'^rm_fav_program', views.rm_fav_program, name = 'rm_fav_program'),
        )
urlpatterns += patterns('haystack.views',
        url(r'^search/$', FacetedSearchView(form_class=FacetedSearchForm, searchqueryset=sqs), name='search'),
        )

