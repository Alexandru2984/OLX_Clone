from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile

class Command(BaseCommand):
    help = 'Creează utilizatori de test pentru dezvoltare'

    def handle(self, *args, **options):
        users_data = [
            {
                'username': 'ion_popescu',
                'email': 'ion.popescu@email.ro',
                'first_name': 'Ion',
                'last_name': 'Popescu',
                'password': 'parola123',
                'profile': {
                    'phone': '+40 721 123 456',
                    'city': 'București',
                    'county': 'București',
                    'bio': 'Vând diverse obiecte din casă.',
                }
            },
            {
                'username': 'maria_ionescu',
                'email': 'maria.ionescu@email.ro',
                'first_name': 'Maria',
                'last_name': 'Ionescu',
                'password': 'parola123',
                'profile': {
                    'phone': '+40 731 234 567',
                    'city': 'Cluj-Napoca',
                    'county': 'Cluj',
                    'bio': 'Pasionată de mode și frumusețe.',
                }
            },
            {
                'username': 'alex_tech',
                'email': 'alex.tech@email.ro',
                'first_name': 'Alexandru',
                'last_name': 'Teodoriu',
                'password': 'parola123',
                'profile': {
                    'phone': '+40 742 345 678',
                    'city': 'Timișoara',
                    'county': 'Timiș',
                    'bio': 'Expert în tehnologie și gadgeturi.',
                }
            },
            {
                'username': 'ana_casa',
                'email': 'ana.casa@email.ro',
                'first_name': 'Ana',
                'last_name': 'Căsărău',
                'password': 'parola123',
                'profile': {
                    'phone': '+40 753 456 789',
                    'city': 'Iași',
                    'county': 'Iași',
                    'bio': 'Vând mobilier și decorațiuni pentru casă.',
                }
            },
            {
                'username': 'radu_auto',
                'email': 'radu.auto@email.ro',
                'first_name': 'Radu',
                'last_name': 'Automobil',
                'password': 'parola123',
                'profile': {
                    'phone': '+40 764 567 890',
                    'city': 'Constanța',
                    'county': 'Constanța',
                    'bio': 'Specialist în piese auto și moto.',
                }
            }
        ]

        self.stdout.write('Creez utilizatori de test...')

        for user_data in users_data:
            # Verific dacă utilizatorul există deja
            if User.objects.filter(username=user_data['username']).exists():
                self.stdout.write(f'- Utilizatorul {user_data["username"]} există deja')
                continue

            # Creez utilizatorul
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )

            # Actualizez profilul (va fi creat automat prin signal)
            profile = user.profile
            profile_data = user_data['profile']
            profile.phone = profile_data['phone']
            profile.city = profile_data['city']
            profile.county = profile_data['county']
            profile.bio = profile_data['bio']
            profile.save()

            self.stdout.write(f'✓ Creat utilizatorul: {user.username} ({user.get_full_name()})')

        self.stdout.write(
            self.style.SUCCESS(
                f'\nTerminat! Au fost creați {User.objects.count() - 1} utilizatori de test.'
                f'\n(Plus admin-ul existent)'
                f'\n\nToți utilizatorii au parola: parola123'
                f'\nPoți să te conectezi cu orice utilizator de mai sus.'
            )
        )

        # Afișez lista utilizatorilor
        self.stdout.write('\n=== UTILIZATORI DISPONIBILI ===')
        self.stdout.write('Username: admin | Password: admin123 (Superuser)')
        for user_data in users_data:
            self.stdout.write(f'Username: {user_data["username"]} | Password: parola123')
