from django.contrib import admin
from wmbitcoin.models import  Transaction, Withdrawal,TransactionID

# AdminSite Registration
admin.site.register(Transaction)
admin.site.register(Withdrawal)
admin.site.register(TransactionID)