from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from listings.models import Listing
from categories.models import Category
import random

class Command(BaseCommand):
    help = 'Creează anunțuri de test pentru dezvoltare'

    def handle(self, *args, **options):
        # Verific dacă avem utilizatori și categorii
        users = User.objects.exclude(username='admin')
        categories = Category.objects.filter(parent__isnull=False)  # Doar subcategoriile
        
        if not users.exists():
            self.stdout.write(self.style.ERROR('Nu există utilizatori! Rulează mai întâi: python manage.py create_test_users'))
            return
            
        if not categories.exists():
            self.stdout.write(self.style.ERROR('Nu există categorii! Rulează mai întâi: python manage.py populate_categories'))
            return

        listings_data = [
            {
                'title': 'iPhone 13 Pro 128GB Albastru',
                'description': 'iPhone 13 Pro în stare foarte bună, folosit 6 luni. Bateria 95%. Include toate accesoriile originale: încărcător, căști, husă silicon. Nu sunt zgârieturi pe ecran, doar urme minore de folosire pe spatele telefonului.',
                'price': 3500,
                'condition': 'very_good',
                'category_name': 'Telefoane mobile',
                'city': 'București',
                'county': 'București',
                'phone': '+40 721 123 456',
                'is_negotiable': True
            },
            {
                'title': 'Laptop Gaming ASUS ROG Strix G15',
                'description': 'Laptop de gaming performant: AMD Ryzen 7, RTX 3060, 16GB RAM, SSD 512GB. Perfect pentru jocuri și aplicații grele. Vine cu geantă de transport și mouse gaming.',
                'price': 4200,
                'condition': 'very_good',
                'category_name': 'Laptopuri',
                'city': 'Cluj-Napoca',
                'county': 'Cluj',
                'phone': '+40 731 234 567',
                'is_negotiable': True
            },
            {
                'title': 'Apartament 2 camere, mobilat complet',
                'description': 'Apartament 2 camere în zona centrală, mobilat și utilat modern. Bucătărie echipată, living spațios, dormitor confortabil. Ideal pentru cuplu sau familie mică. Parcare inclusă.',
                'price': 85000,
                'condition': 'very_good',
                'category_name': 'Apartamente vânzare',
                'city': 'Timișoara',
                'county': 'Timiș',
                'phone': '+40 742 345 678',
                'is_negotiable': True
            },
            {
                'title': 'Canapea 3 locuri, piele naturală',
                'description': 'Canapea din piele naturală, foarte confortabilă. Folosită doar 2 ani, în stare excelentă. Culoare maro închis, design modern. Perfectă pentru living-ul familiei.',
                'price': 1800,
                'condition': 'very_good',
                'category_name': 'Mobilier',
                'city': 'Iași',
                'county': 'Iași',
                'phone': '+40 753 456 789',
                'is_negotiable': True
            },
            {
                'title': 'Dacia Logan 1.6 MPI, 2019',
                'description': 'Autoturism în stare foarte bună, primul proprietar. Service-uri la zi, ITP valid. Consum redus, ideal pentru oraș. Dotări: AC, geamuri electrice, airbag-uri.',
                'price': 28000,
                'condition': 'very_good',
                'category_name': 'Autoturisme',
                'city': 'Constanța',
                'county': 'Constanța',
                'phone': '+40 764 567 890',
                'is_negotiable': True
            },
            {
                'title': 'Rochie de seară, mărimea M',
                'description': 'Rochie elegantă pentru evenimente speciale. Culoare negru cu detalii aurii. Purtată o singură dată la o nuntă. Material de calitate, croială perfectă.',
                'price': 250,
                'condition': 'very_good',
                'category_name': 'Îmbrăcăminte femei',
                'city': 'București',
                'county': 'București',
                'phone': '+40 721 123 456',
                'is_negotiable': False
            },
            {
                'title': 'Bicicletă de munte Trek 29"',
                'description': 'Bicicletă de munte Trek în stare foarte bună. Cadru aluminiu, suspensie față, 21 viteze Shimano. Perfectă pentru trasee de munte și plimbări urbane.',
                'price': 1200,
                'condition': 'good',
                'category_name': 'Biciclete',
                'city': 'Brașov',
                'county': 'Brașov',
                'phone': '+40 731 234 567',
                'is_negotiable': True
            },
            {
                'title': 'Console PlayStation 5 + 3 jocuri',
                'description': 'PlayStation 5 în garanție, stare perfectă. Include 3 jocuri: Spider-Man, FIFA 24, Call of Duty. Un al doilea controller inclus. Toate cutiile și accesoriile originale.',
                'price': 2800,
                'condition': 'new',
                'category_name': 'Console jocuri',
                'city': 'Cluj-Napoca',
                'county': 'Cluj',
                'phone': '+40 742 345 678',
                'is_negotiable': False
            }
        ]

        self.stdout.write('Creez anunțuri de test...')
        created_count = 0

        for listing_data in listings_data:
            # Găsesc categoria
            try:
                category = Category.objects.get(name=listing_data['category_name'])
            except Category.DoesNotExist:
                self.stdout.write(f'- Categoria "{listing_data["category_name"]}" nu există')
                continue

            # Aleg un utilizator random
            user = random.choice(users)

            # Verific dacă anunțul există deja
            if Listing.objects.filter(title=listing_data['title']).exists():
                self.stdout.write(f'- Anunțul "{listing_data["title"]}" există deja')
                continue

            # Creez anunțul
            listing = Listing.objects.create(
                title=listing_data['title'],
                slug=slugify(listing_data['title']),
                description=listing_data['description'],
                price=listing_data['price'],
                condition=listing_data['condition'],
                category=category,
                owner=user,
                city=listing_data['city'],
                county=listing_data['county'],
                phone=listing_data['phone'],
                email=user.email,
                is_negotiable=listing_data['is_negotiable'],
                status='active'
            )

            created_count += 1
            self.stdout.write(f'✓ Creat anunțul: "{listing.title}" (de {user.get_full_name()})')

        self.stdout.write(
            self.style.SUCCESS(
                f'\nTerminat! Au fost create {created_count} anunțuri de test.'
                f'\nAcum poți vedea anunțurile pe pagina principală!'
            )
        )
