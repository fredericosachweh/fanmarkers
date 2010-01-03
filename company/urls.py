from django.conf.urls.defaults import *

urlpatterns = patterns('company',
        url(
            r'^$',
            "views.make_list",
                                                           name="list-company",
        ),
        
        url(
            r'^(?P<pk>\d*)-(?P<slug>[a-z0-9\-]*).html$',
            "views.view",
                                                           name="view-company",
        ),
        
        url(
            r'^new/$',
            "views.new",
                                                            name="new-company",
        ),
        
        url(
            r'^edit-(?P<pk>\d{1,4})/$',
            "views.edit",
                                                           name="edit-company",
        ),
        
        url(
            r'^(?P<pk>\d*).kmz$',
            "views.kml",
                                                            name="kml-company",
        ),
)
