from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime
from django.db import transaction
from ...models import Chump, ChumpMedia

class Command(BaseCommand):

    help = "Import chumps data from Astro's geocities archive and update the database"

    def handle(self, *args, **options):
        # get json from http://localhost:4321/chumps.json
        import requests
        response = requests.get('http://localhost:4321/chumps.json')
        chumps_data = response.json()
        #         {
        #     "name": "Toilet Truck Tumbles: Bridge Blocks Bowls in Big Blow",
        #     "date": "2025-02-14",
        #     "thanks": "Thank you Buddy!",
        #     "url": "#",
        #     "image": "/images/chumps/2025-02-14.png",
        #     "streak": 42,
        #     "localisedDate": "Friday 14 February 2025",
        #     "dateBasic": "14/02/2025"
        # },

        from chumps.models import Chump, ChumpMedia
        for chump_data in chumps_data:
            print(f"Processing chump: {chump_data['name']} on {chump_data['date']}")

            existing_chump = Chump.objects.filter(name=chump_data['name'], date=chump_data['date']).first()
            if existing_chump:
                print(f"Chump already exists: {existing_chump.name} on {existing_chump.date}")
                continue

            chump, created = Chump.objects.update_or_create(
                name=chump_data['name'],
                date=chump_data['date'],
                defaults={
                    'thanks': chump_data['thanks'],
                    'url': chump_data['url'],
                    'slug': chump_data['slug']
                }
            )
            if chump_data.get('image'):
                ChumpMedia.objects.update_or_create(
                    chump=chump,
                    media_type='image',
                    media_order=0,
                    defaults={
                        'media': chump_data['image'],
                    }
                )
