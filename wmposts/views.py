import random
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from wmposts.models import BasePost
from wmposts.forms import UploadFileForm
from wmuser.models import BaseUser
from wmcomment.forms import CommentForm, NestedCommentForm
from wmcomment.models import BaseComment, NestedComment
from wmbitcoin.models import Transaction
from wmbitcoin.forms import TransactionForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.utils import timezone

# -*- coding: UTF-8 -*-

def index(request):
	# Get all from model instance. Save to variable
	post_list = BasePost.objects.order_by('date_added').reverse()  # Jarjestetaan paivamaaran mukaa.
	template = 'index.html'
	page_template = 'index_entries.html'

	if request.method == 'POST':
		user= request.user
		user.balance +=10;
		user.save()


	if request.is_ajax():
		template = page_template 

	if request.user.is_authenticated():
		upvoter = request.user
		return render_to_response(template,
			{'post_list':post_list, 'balance' :upvoter.balance, 'page_template':page_template},
			context_instance=RequestContext(request)
			)

	return render_to_response(template,
		{'post_list': post_list, 'page_template':page_template},
		context_instance=RequestContext(request)
		)

def justin(request):
	# Get all from model instance. Save to variable
	post_list = BasePost.objects.order_by('date_added').reverse()  # Jarjestetaan paivamaaran mukaa.
	template = 'justin.html'
	page_template = 'justin_entries.html'

	if request.is_ajax():
		template = page_template 

	if request.user.is_authenticated():
		upvoter = request.user
		return render_to_response(template,
			{'post_list':post_list, 'balance' :upvoter.balance, 'page_template':page_template},
			context_instance=RequestContext(request)
			)

	return render_to_response(template,
		{'post_list': post_list, 'page_template':page_template},
		context_instance=RequestContext(request)
		)



@login_required(login_url='/signin')
def upvote(request):

	context = RequestContext(request)
	post_id = None
	upvotes = None
	if request.method == 'GET':
		post_id = request.GET['post_id']
		
		upvoter = request.user
		
		post = BasePost.objects.get(pk=post_id)  
		uploader = post.uploader

		upvotes = post.upvotes
		now = timezone.now()
		# # jos ei ole tykannyt
		if not Transaction.objects.filter(sender=upvoter, related_post=post).exists():
			if upvoter.balance > 0:
				p = Transaction(sender=upvoter, recipient=uploader, related_post=post, date_sent = now)
				p.save()
				uploader.balance += 1
				upvoter.balance -= 1
				upvoter.save()
				uploader.save()
				upvotes = post.upvotes + 1
				post.upvotes = upvotes
				post.save()
				
			else:
				##pass #tahan joku popup etta balance =0, osta lisaa
				print("Balance=0")
		else:
			print("like not succesful")
			
	return HttpResponse(upvotes)


def singlepost(request, pk):
	post = BasePost.objects.get(pk=int(pk))
	comments = BaseComment.objects.filter(linked_post=post).order_by('posted_on').reverse()
	
	nested_comments = []
	print("singlepost")
	for c in comments:
		nested_comments += NestedComment.objects.filter(nested_linked_comment = c )

	if request.method == 'POST':
		print("post")
		
		
		if request.POST.get('comment_content'):
			print("comment")
			form = CommentForm(request.POST)
			nested_form = NestedCommentForm()
			comment = request.POST.get("comment_content")
			print("-------------- normnal comment")
			print(comment)
			print("errores")
			
			if form.is_valid():
				print("is valid")
				comment = form.save(commit=False)
				comment.linked_post = post
				comment.linked_user = request.user
			#	comment.posted_on = timezone.now()
			
				comment.save()
				post.noc += 1
				post.save()
				
				return HttpResponseRedirect('')  # , pk=BasePost.pk)
			print(form.errors)
			
						
		elif request.POST.get('nested_content'):
			
			form = CommentForm()
			nested_form = NestedCommentForm(request.POST)
			nested_comment = request.POST.get('nested_content')
			id = request.POST.get('base_comment_hidden')
			base_comment = BaseComment.objects.get(pk=int(id))
			nested_comments = NestedComment.objects.filter(nested_linked_comment=base_comment)
			
		
			print("-------------- nested comment")
			print(nested_comment)
			
			if nested_form.is_valid():
				print("is valid")
				nested_comment = nested_form.save(commit=False)
				nested_comment.nested_linked_comment = base_comment
				nested_comment.nested_linked_user = request.user
				nested_comment.save()
				#return render_to_response('singlepost.html',
				#	{'nested_form':nested_form,'form':form, 'base_comment':base_comment, 'nested_comments':nested_comments,'comments' :comments},
				#	context_instance=RequestContext(request)
				#	)
				return HttpResponseRedirect('') 
		
	else:
		form = CommentForm()
		nested_form = NestedCommentForm()
			
	return render_to_response('singlepost.html',
		{'post' :post,'nested_form':nested_form,'form':form, 'nested_comments':nested_comments,'comments' :comments},
		context_instance=RequestContext(request)
		)


@login_required(login_url='/signin')
def submit(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES) 
		uploader = request.user
		
		if form.is_valid():
			instance = form.save(commit=False)
			instance.uploader = uploader  # Asettaa kayttajan postille
			instance.post_content = request.FILES['post_content']
			instance.save()
			return HttpResponseRedirect('../')
	else:
		form = UploadFileForm()
	return render_to_response('submit.html',
		{'form': form},
		context_instance=RequestContext(request)
		)

def random(request):

	all_post_list = BasePost.objects.order_by('date_added').reverse()
	randomized_list = all_post_list.order_by('?')

	page_template = 'post_random_entries.html'

	if request.is_ajax():
		template = page_template 

	return render_to_response('post_random.html',
		{'randomized_list':randomized_list, 'page_template': page_template},
		context_instance=RequestContext(request)
		)


