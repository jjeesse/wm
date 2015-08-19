from django import forms
from wmbitcoin.models import Transaction

class DepositForm(forms.Form):
	deposit_amount = forms.FloatField()

class WithdrawForm(forms.Form):
	withdrawal_address = forms.CharField(label='Withdraw Address', max_length=64)
	withdrawal_amount = forms.FloatField()
	
class TransactionForm(forms.Form):
	class Meta:
		model = Transaction
		fields= ['sender', 'recipient', 'related_post', 'date_sent'] 