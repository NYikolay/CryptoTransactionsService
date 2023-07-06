from django.contrib import admin
from transactions.forms import ServiceAccountAdminForm
from transactions.models import Transaction, ServiceAccount, Network, Cryptocurrency

@admin.register(ServiceAccount)
class ServiceAccountAdmin(admin.ModelAdmin):
    form = ServiceAccountAdminForm


admin.site.register(Transaction)
admin.site.register(Network)
admin.site.register(Cryptocurrency)
