from django.shortcuts import render
from django.views.generic import View


class TransactionsList(View):
    template_name = 'transactions/transactions_list.html'
