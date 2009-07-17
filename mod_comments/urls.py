from django.conf.urls.defaults import *
 
urlpatterns = patterns('',
	url(r'^delete/(?P<comment_id>\d+)/$',		'mod_comments.views.delete', name="delete-comment"),
	(r'',						include('django.contrib.comments.urls')),
)
