import requests
import json
import urllib
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from coinbase.wallet.client import Client
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from wmbitcoin.forms import DepositForm, WithdrawForm
from wmbitcoin.models import TransactionID, CommentTransaction, NestedCommentTransaction
from wmcomment.models import BaseComment, NestedComment
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.decorators import login_required

api_key = 'J4LzfXkH3UnvqbiW'
api_secret = 'lCbEISzRQAMXYqNFlzo9F3sVUyLWI4w1'
client = Client(api_key, api_secret)
main_address = '1DsRGPTtrBHiSAbeu7828Ad42G22emWegq'
account = client.get_primary_account()
btc_to_bits_conversion = 1000000

STATUS_ACTIVE =0
STATUS_COMPLETED =1
STATUS_EXPIRED =2

#0.00000395 = 0.001 
btc_to_upvotes = 0.00000395
btc_to_eur =253.16
#get_spot_price
def bitcointest(request):

	accounts = client.get_accounts()
	accounts = client.get_currencies()
	#final = accounts.get_addresses()
	
	return render_to_response("test.html",
		{'accounts':accounts},
		context_instance=RequestContext(request)
		)

@login_required
def deposit(request):

	if request.method == 'POST':
		form = DepositForm(request.POST)
		account_holder = request.user

		if form.is_valid():
			deposit_upvotes = form.cleaned_data['deposit_amount']
			deposit_amount_btc = deposit_upvotes * btc_to_upvotes
			deposit_amount_eur = int(deposit_upvotes / 1000)
			print("-------------------")
			print(str(deposit_amount_btc))
			muuttuja = client.create_order(amount=deposit_amount_btc, currency="BTC", name="#Order")
			#if muuuttuja.status == 'completed'
			id = muuttuja.id
			btc_amount =  float(muuttuja.bitcoin_amount.amount)
			#created = muuttuja.created_at
			#expires = muuttuja.expires_at
			
			##### LUODAAN ID JOKA TARKASTETAAN JA POISTETAAN CALLBACKISSA.
			transactionid = TransactionID(user = request.user, tid = id, amount = btc_amount,status = STATUS_ACTIVE)
			
			print("status" + str(transactionid.status))
			transactionid.save()
			print("ID:" +id)
			print("AMOUNT:" +str(btc_amount))

			return render_to_response('profile_btc.html', 
				{'form':form, 'muuttuja':muuttuja,'a_eur' :deposit_amount_eur},
				context_instance=RequestContext(request)
				)
		else:
			return HttpResponse('Invalid Shit')
	else:
		form = DepositForm()

	return render_to_response('profile_btc.html', 
		{'form':form},
		context_instance=RequestContext(request)
		)

'''
@login_required
def withdraw(request):
	
	if request.method == 'POST':
		form = WithdrawForm(request.POST)
		account_holder = request.user

		if form.is_valid():
			withdrawal_address = form.cleaned_data['withdrawal_address']
			withdrawal_amount = form.cleaned_data['withdrawal_amount']
			account.send_money(to=withdrawal_address, amount=withdrawal_amount, currency='BTC')
			account_holder.balance -= withdrawal_amount * btc_to_bits_conversion
			return render_to_response('btcwithdraw.html', 
				{'form':form},
				context_instance=RequestContext(request)
				)
		else:
			return HttpResponse('Invalid Shit')
	else:
		form = WithdrawForm()

	return render_to_response('btcwithdraw.html', 
		{'form':form},
		context_instance=RequestContext(request)
		)
'''


@csrf_exempt
def CallBack(request):

	##IHAN VITUN VAARA TAPA HYI SAATANA. mutta ne saanu jsonia toimimaan niin piti soveltaa, etta paasee kokeilemaan  korjatkaa joku joka osaa
	##json pistais saada: data = json.loads(request.body), mutta ei toimi :(
	## Pitaa myos lisata jotenki tiedot kayttajalle tidot kuinka paljon on ostanut ja milloinkin.
		
	i = str(request.body).find('uuid')
	##tarkastettava id, pitaa teha uudestaan
	#voidaan myos tarkastaa enemman tietoja kun saadaan json toimimaan.
	s = str(str(request.body)[i+7:][:36])
	statusindex = str(request.body).find('status')
	status  = str(request.body)[statusindex+9:][:12]
	stat= status.find('completed') 	# Jos completed =0, muuten -1
	#nama kaikki paremmin!!! 
	if TransactionID.objects.filter(tid = s).exists(): # Jos id on tietokannassa, eli tilaus on tehty ja voimassa.
	
		if not stat == -1: ## jos completed

			tID = TransactionID.objects.get(tid = s)
			print("id status :" + str(tID.status))
			if tID.status == STATUS_ACTIVE:
				user = tID.user
				amount_to_load =(tID.amount / btc_to_upvotes)
				user.balance += int(amount_to_load) ## pitaa katsoa pyoristyyko varmasti oikein.
				user.save()
				tID.status = STATUS_COMPLETED
				tID.save()
				print("Succesfully added " + str(int(amount_to_load)) +" upvotes = "+ str(tID.amount) +" BTC = " + str(tID.amount * btc_to_eur)+ " EUR")
			else:
				print("status not active")
		else:
			print("Not completed")
						
	else:
		print('Transaction id doesnt exist')

	return HttpResponse(status = 200) ## status = 200 ei tarvita mutta olkoot siina kaikkien iloksi


@login_required(login_url='/signin')
def comment_upvote(request):

	print('step1')
	context = RequestContext(request)
	comment_id = None
	comment_upvotes = None

	if request.method == 'GET':
		comment_id = request.GET['comment_id']
		comment_upvoter = request.user
		comment = BaseComment.objects.get(pk=comment_id)
		original_commenter = comment.linked_user
		comment_upvotes = comment.comment_upvotes
		now = timezone.now()
		print('request.method == GET')

		if not CommentTransaction.objects.filter(sender=comment_upvoter, related_comment=comment).exists():
			print("exists")
			if comment_upvoter.balance > 0:
				print("pass this shit")
				newCommentUpvote = CommentTransaction(sender=comment_upvoter, recipient=original_commenter, related_comment=comment, date_sent=now)
				newCommentUpvote.save()
				original_commenter.balance += 1
				comment_upvoter.balance -= 1
				original_commenter.save()
				comment_upvoter.save()
				comment_upvotes = comment.comment_upvotes + 1
				comment.comment_upvotes = comment_upvotes
				comment.save()
			else:
			##pass #tahan joku popup etta balance =0, osta lisaa
				print("Balance = 0")
		else:
			print("Like NOT Successfull")
			
	return HttpResponse(comment_upvotes)


@login_required(login_url='/signin')
def nested_comment_upvote(request):

	print('step1')
	context = RequestContext(request)
	nested_comment_id = None
	nested_comment_upvotes = None
	print('step2')

	if request.method == 'GET':
		print('step2b')
		nested_comment_id = request.GET['nested_comment_id']
		print (nested_comment_id)
		print('step3')
		nested_upvoter = request.user
		nested_comment = NestedComment.objects.get(pk=nested_comment_id)
		original_nested_commenter = NestedComment.nested_linked_user
		nested_upvotes = nested_comment.nested_comment_upvotes
		now = timezone.now()
		print('step4a')

		if not NestedCommentTransaction.objects.filter(sender=nested_upvoter, related_nested_comment=nested_comment).exists():
			if nested_upvoter.balance > 0:
				print('step4')
				newNestedCommentUpvote = NestedCommentTransaction(sender=nested_upvoter, recipient=original_nested_commenter, related_nested_comment=nested_comment, date_sent=now)
				newNestedCommentUpvote.save()
				original_nested_commenter.balance += 1
				nested_upvoter.balance -= 1
				original_nested_commenter.save()
				nested_upvoter.save()
				nested_upvotes = nested_comment.nested_comment_upvotes + 1
				nested_comment.nested_comment_upvotes = nested_upvotes
				nested_comment.save()
			else:
			##pass #tahan joku popup etta balance =0, osta lisaa
				print("Balance=0")
		else:
			print("like not succesful")
			
	return HttpResponse(nested_comment_upvotes)












