from django.core.management.base import BaseCommand
import pandas as pd
from django.db import transaction

from transactions.models import Cryptocurrency, Network


class Command(BaseCommand):

    def handle(self, **options):
        if not Cryptocurrency.objects.exists() and not Network.objects.exists():
            crypto_df = pd.read_csv('static/excel/crypto_data.csv')

            unique_networks = crypto_df['network'].unique().tolist()
            networks_objects = [
                Network(name=network) for network in unique_networks
            ]

            with transaction.atomic():
                Network.objects.bulk_create(networks_objects)

                created_networks = Network.objects.in_bulk(unique_networks,
                                                           field_name='name')

                cryptos = [
                    Cryptocurrency(network=created_networks[network], name=currency_name)
                    for network, currency_name in crypto_df.itertuples(index=False)
                ]

                Cryptocurrency.objects.bulk_create(cryptos)
