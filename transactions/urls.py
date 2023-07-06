from django.contrib import admin
from django.urls import path

from transactions.views import TransactionsView, CreateTransactionView, CancelTransactionView, ConfirmTransactionView

app_name = 'transactions'

urlpatterns = [
    path('', TransactionsView.as_view(), name='transactions'),
    path('create-transaction/', CreateTransactionView.as_view(), name='create_transaction'),
    path('transaction/<int:pk>/confirm/', ConfirmTransactionView.as_view(), name='confirm_transaction'),
    path('transaction/<int:pk>/cancel/', CancelTransactionView.as_view(), name='cancel_transaction')

]
