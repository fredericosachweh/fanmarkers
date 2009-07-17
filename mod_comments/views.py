from django.contrib.auth.decorators import login_required
from django.contrib.comments.models import Comment
from django.http import Http404
from django.shortcuts import get_object_or_404
import django.contrib.comments.views.moderation as moderation

@login_required
def delete(request, comment_id):
	comment = get_object_or_404(Comment, pk=comment_id)
	
	if request.user == comment.user or request.user.is_superuser:
		return moderation.delete(request, comment_id)
	else:
		raise Http404
		
def post(request, next=None):
	if request.POST["anon"]:
		pass
