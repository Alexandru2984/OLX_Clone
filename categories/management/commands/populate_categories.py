from django.core.management.base import BaseCommand
from django.utils.text import slugify
from categories.models import Category

class Command(BaseCommand):
    help = 'Populează baza de date cu categorii de test'

    def handle(self, *args, **options):
        categories_data = [
            {'name': 'Electronice & IT', 'icon': 'laptop', 'subcategories': [
                'Telefoane mobile', 'Laptopuri', 'Desktop-uri', 'Tablete',
                'Console jocuri', 'Accesorii telefoane', 'Software'
            ]},
            {'name': 'Auto, Moto, Ambarcațiuni', 'icon': 'car', 'subcategories': [
                'Autoturisme', 'Motociclete', 'Piese auto', 'Anvelope',
                'Ambarcațiuni', 'Remorci', 'Utilaje agricole'
            ]},
            {'name': 'Imobiliare', 'icon': 'home', 'subcategories': [
                'Apartamente vânzare', 'Case vânzare', 'Terenuri vânzare',
                'Apartamente închiriere', 'Case închiriere', 'Spații comerciale'
            ]},
            {'name': 'Modă & Frumusețe', 'icon': 'tshirt', 'subcategories': [
                'Îmbrăcăminte femei', 'Îmbrăcăminte bărbați', 'Încălțăminte',
                'Accesorii', 'Ceasuri', 'Bijuterii', 'Cosmetice'
            ]},
            {'name': 'Casă & Grădină', 'icon': 'couch', 'subcategories': [
                'Mobilier', 'Electronice casnice', 'Decorațiuni',
                'Unelte & Scule', 'Grădină', 'Bricolaj'
            ]},
            {'name': 'Sport & Timp liber', 'icon': 'futbol', 'subcategories': [
                'Echipamente sport', 'Biciclete', 'Fitness',
                'Pescuit', 'Vânătoare', 'Camping', 'Jocuri'
            ]},
            {'name': 'Copii & Bebeluși', 'icon': 'baby', 'subcategories': [
                'Îmbrăcăminte copii', 'Jucării', 'Cărțuci & Scaune auto',
                'Echipamente bebeluși', 'Cărți pentru copii'
            ]},
            {'name': 'Animale', 'icon': 'paw', 'subcategories': [
                'Câini', 'Pisici', 'Animale de fermă',
                'Accesorii animale', 'Hrană animale'
            ]},
            {'name': 'Locuri de muncă', 'icon': 'briefcase', 'subcategories': [
                'IT & Software', 'Vânzări', 'Marketing',
                'Construcții', 'HoReCa', 'Transport'
            ]},
            {'name': 'Servicii', 'icon': 'tools', 'subcategories': [
                'Reparații', 'Construcții', 'Curățenie',
                'Transport', 'Evenimente', 'Educație'
            ]},
        ]

        self.stdout.write('Creez categoriile...')
        
        for category_data in categories_data:
            # Creez categoria principală
            parent_category, created = Category.objects.get_or_create(
                name=category_data['name'],
                defaults={
                    'slug': slugify(category_data['name']),
                    'icon': category_data['icon'],
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(f'✓ Creată categoria: {parent_category.name}')
            else:
                self.stdout.write(f'- Categoria există deja: {parent_category.name}')
            
            # Creez subcategoriile
            for subcategory_name in category_data['subcategories']:
                subcategory, sub_created = Category.objects.get_or_create(
                    name=subcategory_name,
                    parent=parent_category,
                    defaults={
                        'slug': slugify(subcategory_name),
                        'is_active': True
                    }
                )
                
                if sub_created:
                    self.stdout.write(f'  ✓ Creată subcategoria: {subcategory.name}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Terminat! Au fost create {Category.objects.count()} categorii în total.'
            )
        )
