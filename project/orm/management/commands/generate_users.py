from django.core.management.base import BaseCommand
from faker import Faker
from orm.models import CustomUser
from django.contrib.auth.hashers import make_password
import random
from django.utils import timezone

class Command(BaseCommand):
    help = 'Generate fake users'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10000, help='Number of users to generate')

    def handle(self, *args, **options):
        count = options['count']
        fake = Faker()
        departments = [choice[0] for choice in CustomUser.Department.choices]
        roles = [choice[0] for choice in CustomUser.Role.choices]
        
        # Хешируем пароль один раз вместо count раз
        hashed_password = make_password('12345')

        tz = timezone.get_current_timezone()

        users = []
        self.stdout.write(f'Generating {count} users...')
        
        for i in range(count):
            if i % 1000 == 0:
                self.stdout.write(f'Progress: {i}/{count}')
                
            user = CustomUser(
                email=fake.unique.email(),
                username=fake.unique.user_name(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone=fake.phone_number(),
                city=fake.city(),
                country=fake.country(),
                department=random.choice(departments),
                role=random.choice(roles),
                birth_date=fake.date_of_birth(minimum_age=20, maximum_age=65),
                salary=round(random.uniform(30000, 150000), 2),
                is_active=random.choice([True, False]),
                is_staff=random.choice([True, False]),
                date_joined=fake.date_time_this_decade(tzinfo=tz, before_now=True),
                last_login=fake.date_time_this_decade(tzinfo=tz, before_now=True),
                password=hashed_password  # Используем готовый хеш
            )
            users.append(user)

        self.stdout.write('Saving to database...')
        CustomUser.objects.bulk_create(users, batch_size=1000)
        self.stdout.write(self.style.SUCCESS(f'Successfully generated {count} users'))