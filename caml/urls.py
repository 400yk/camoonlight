from django.views.generic import RedirectView
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'caml.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', RedirectView.as_view(url='/ca/')), 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ca/', include('ca.urls', namespace = 'ca')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
