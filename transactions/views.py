from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView

from transactions.services.handling_transaction_confirmation_services import send_transaction_confirmation
from transactions.forms import TransactionForm
from transactions.models import TransactionStatuses, Transaction


class TransactionsView(LoginRequiredMixin, View):
    login_url = reverse_lazy('users:login')
    template_name = 'transactions/transactions.html'
    form_class = TransactionForm

    def get(self, request):
        service_accounts = request.user.service_accounts.select_related('network', 'cryptocurrency')
        service_accounts_addresses = service_accounts.values_list('wallet_address', flat=True)

        for_review_transactions = Transaction.objects.filter(
            recipient_address__in=service_accounts_addresses,
            status=TransactionStatuses.PROCESSING
        )

        user_transactions = request.user.transactions.order_by('-created_at')

        form = self.form_class(
            sender_address_queryset=service_accounts,
            initial={"sender": request.user}
        )

        context = {
            "service_accounts": service_accounts,
            "form": form,
            "transactions": user_transactions,
            "transaction_statuses": TransactionStatuses,
            "for_review_transactions": for_review_transactions
        }

        return render(request, self.template_name, context=context)


class CreateTransactionView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('users:login')
    form_class = TransactionForm
    success_url = reverse_lazy('transactions:transactions')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        service_accounts = self.request.user.service_accounts.select_related('network', 'cryptocurrency')
        kwargs['sender_address_queryset'] = service_accounts
        return kwargs

    def form_valid(self, form):
        wallet_address = form.cleaned_data['sender_address'].wallet_address
        recipient_address = form.cleaned_data['recipient_address']

        if wallet_address == recipient_address:
            messages.error(self.request, 'Unable to create a transaction with the same address')
            return redirect(self.get_success_url())

        form.instance.sender_address = wallet_address
        form.save()
        messages.success(self.request, 'Transaction was created successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Form error. Check inputs')
        return super().form_invalid(form)


class CancelTransactionView(LoginRequiredMixin, View):
    login_url = reverse_lazy('users:login')

    def post(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk)
        service_accounts_addresses = request.user.service_accounts.values_list('wallet_address', flat=True)

        if transaction.recipient_address in service_accounts_addresses:
            transaction.status = TransactionStatuses.CANCELED
            transaction.save()
            messages.success(request, 'Transaction was canceled')
        else:
            messages.error(request, 'You have no permission for this')
        return redirect("transactions:transactions")


class ConfirmTransactionView(LoginRequiredMixin, View):
    login_url = reverse_lazy('users:login')

    def post(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk)
        service_accounts_addresses = request.user.service_accounts.values_list('wallet_address', flat=True)

        if transaction.recipient_address in service_accounts_addresses:
            confirmation_status: dict = send_transaction_confirmation(
                transaction.sender_address,
                transaction.recipient_address,
                transaction.amount
            )
            if confirmation_status.get("status"):
                transaction.status = TransactionStatuses.ACCEPTED
                transaction.save()

                messages.success(request, 'Transaction was accepted')
            else:
                messages.error(request, 'The transaction was not confirmed')
        else:
            messages.error(request, 'You have no permission for this')

        return redirect("transactions:transactions")
