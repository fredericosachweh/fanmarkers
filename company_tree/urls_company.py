from django.conf.urls.defaults import *
from django.views.generic import create_update, list_detail

from models import Company
from forms import CompanyForm


company_view = {
			"queryset": Company.objects.all(),
			"template_name": "view_company.html",
			"template_object_name": "company",
		}


urlpatterns = patterns('',
	(r'^$',					"company_tree.views_company.make_list"),
	(r'^(?P<object_id>\d{1,4})/$',		list_detail.object_detail, company_view),
	(r'^new/$',				create_update.create_object, {"form_class": CompanyForm, "template_name": "new_company.html"}),
	(r'^edit/(?P<object_id>\d{1,4})/$',	create_update.update_object, {"form_class": CompanyForm, "template_name": "edit_company.html"}),
)
