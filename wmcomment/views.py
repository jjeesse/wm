from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from wmcomment.models import BaseComment
from wmcomment.forms import CommentForm, NestedCommentForm
from wmposts.models import BasePost
from django.template import RequestContext
from django.http.response import HttpResponse

def add_comment(request, pk):
	
	
	post = BasePost.objects.get(pk=int(pk))
	comments = BaseComment.objects.filter(linked_post=post)
	if request.method == 'POST':
		form = CommentForm(request.POST)
		
		comment = request.POST.get("content")
		print("--------------")
		print(comment)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.linked_post = post
			comment.linked_user = request.user
		
			comment.save()
			post.noc += 1
			post.save()
			return HttpResponseRedirect('')  # , pk=BasePost.pk)
	else:
		form = CommentForm()
		
	
	return render_to_response('singlepost.html',
		{'form':form, 'post': post, 'comments' : comments},
		context_instance=RequestContext(request)
		)
	
	
def add_nested_comment(request, pk):

	base_comment = BaseComment.objects.get(pk=int(pk))
	nested_comments = NestedComment.objects.filter(nested_linked_comment=base_comment)
	
	
	post = BasePost.objects.get(pk=base_comment.linked_post)
	
	comments = BaseComment.objects.filter(linked_post=post)
	 
	if request.method == 'POST':
		nested_form = NestedCommentForm(request.POST)
		nested_comment = request.POST.get('nested_content')
		
		if form.is_valid():
				nested_comment = nested_form.save(commit=False)
				nested_comment.nested_linked_comment = base_comment
				nested_comment.nested_linked_user = request.user
				nested_comment.save()
				return render_to_response('singlepost.html',
					{'nested_form':nested_form,'base_comment':base_comment, 'nested_comments':nested_comments,'comments' :comments},
					context_instance=RequestContext(request)
					)
	else:
		form = NestedCommentForm()
		
	return render_to_response('singlepost.html',
		{'nested_form':nested_form,'base_comment':base_comment, 'nested_comments':nested_comments,'comments' :comments},
		context_instance=RequestContext(request)
		)

	
	
	