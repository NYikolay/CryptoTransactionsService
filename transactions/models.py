from django.db import models
from django.contrib.auth.models import User


class TransactionStatuses(models.TextChoices):
    PROCESSING = "PROCESSING"
    CANCELED = "CANCELED"
    ACCEPTED = "ACCEPTED"


class Network(models.Model):
    name = models.CharField(
        max_length=25,
        unique=True,
        verbose_name='Blockchain network'
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Network'
        verbose_name_plural = 'Networks'


class Cryptocurrency(models.Model):
    network = models.ForeignKey(
        Network,
        on_delete=models.PROTECT,
        related_name='currencies',
        verbose_name='Blockchain network'
    )
    name = models.CharField(max_length=25, unique=True, verbose_name='Cryptocurrency name')

    def __str__(self) -> str:
        return f'{self.name} | {self.network.name}'

    class Meta:
        verbose_name = 'Cryptocurrency'
        verbose_name_plural = 'Cryptocurrenies'


class ServiceAccount(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.PROTECT, 
        related_name='service_accounts'
    )
    wallet_address = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Wallet Address'
    )
    sub_account_id = models.CharField(
        max_length=10,
        verbose_name='subaccountID'
    )
    network = models.ForeignKey(
        Network,
        on_delete=models.PROTECT,
        related_name='accounts',
        verbose_name='Blockchain network'
    )
    cryptocurrency = models.ForeignKey(
        Cryptocurrency,
        on_delete=models.PROTECT,
        related_name='accounts',
        verbose_name='Cryptocurrency'
    )

    def __str__(self) -> str:
        return f'Service account of {self.user.username} | Network: {self.network.name} | Crypto: {self.cryptocurrency.name}'

    class Meta:
        verbose_name = 'Service Account'
        verbose_name_plural = 'Service Accounts'


class Transaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions', verbose_name='Sender User')
    sender_address = models.CharField(max_length=255, verbose_name='Sender Wallet Address')
    recipient_address = models.CharField(max_length=255, verbose_name='Recipient Wallet Address')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Amount')
    status = models.CharField(
        max_length=10,
        default=TransactionStatuses.PROCESSING,
        choices=TransactionStatuses.choices,
        verbose_name='Transaction status'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Transaction created')

    def __str__(self) -> str:
        return f'Transaction from {self.sender_address} to {self.recipient_address} | amount: {self.amount}'
