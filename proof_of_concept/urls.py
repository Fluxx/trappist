from django.conf.urls.defaults import patterns, include, url
from other_app import app
from trappist import Trappist

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

extra_patterns = patterns('',
    url(r'^reports/(?P<id>\d+)/$', 'credit.views.report', name='credit-reports'),
    url(r'^charge/$', 'credit.views.charge', name='credit-charge'),
)

urlpatterns = patterns('', Trappist(app).mounted_at('foo')
    # Examples:
    # TODO: Look at passing arguments from Django URLConf to the Flask app.
    # url(r'^foo', include(other_app.trappist.urls)),
    # url(r'^proof_of_concept/', include('proof_of_concept.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
