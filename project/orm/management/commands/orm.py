from orm.models import CustomUser
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Q, Count, Avg, Min, Max, Value, Case, When, CharField, Sum, F
from django.db.models.functions import Concat, ExtractYear

class Command(BaseCommand):
    help = 'Display all users'

    def handle(self, *args, **options):
        # result = CustomUser.objects.all()
        #2 result = CustomUser.objects.filter(email__endswith='gmail.com')
        # result = CustomUser.objects.filter(city='Almaty')
        # result = CustomUser.objects.all().exclude(city="Almaty")
        # result = CustomUser.objects.filter(salary__gt=500000)
        # result = CustomUser.objects.filter(country="Kazakhstan", department=CustomUser.Department.IT)
        # result = CustomUser.objects.filter(birth_date__isnull=True)
        # result = CustomUser.objects.filter(first_name__startswith='A')
        # result = CustomUser.objects.count()
        # 10 result = CustomUser.objects.order_by('-date_joined')[:20] 
        # result = CustomUser.objects.values('city').distinct()
        # result = CustomUser.objects.filter(department=CustomUser.Department.SALES).count()
        # result = CustomUser.objects.filter(last_login__gte=timezone.now()-timezone.timedelta(days=7))
        # result = CustomUser.objects.filter(Q(first_name__icontains='bek') | Q(last_name__icontains='bek'))
        # result = CustomUser.objects.filter(salary__gte=300000, salary__lte=700000) 
        # result = CustomUser.objects.filter(department__in=[CustomUser.Department.IT, CustomUser.Department.HR, CustomUser.Department.FINANCE])
        # result = CustomUser.objects.values('department').annotate(count=Count('id'))
        # result = CustomUser.objects.values('department').annotate(count=Count('id')).order_by('-count')
        # result = CustomUser.objects.values('city').annotate(count=Count('id')).order_by('-count')[:5]
        # 20 result = CustomUser.objects.filter(last_login__isnull=True)
        # result = CustomUser.objects.aggregate(average_salary=Avg('salary'))
        # result = CustomUser.objects.aggregate(min_salary=Min('salary'), max_salary=Max('salary'))
        # result = CustomUser.objects.filter(phone__icontains='+7')
        # result = CustomUser.objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name')).values('full_name')
        # result = CustomUser.objects.annotate(birth_year=ExtractYear('birth_date')).values('birth_year').order_by('birth_year')
        # result = CustomUser.objects.filter(birth_date__month=5)
        # result = CustomUser.objects.filter(role=CustomUser.Role.MANAGER, salary__gt=400000)
        # result = CustomUser.objects.filter(Q(department=CustomUser.Department.HR) | Q(role=CustomUser.Role.EMPLOYEE))
        # result = CustomUser.objects.values('city').annotate(count=Count('id')).filter(is_active=True).order_by('-count')
        # 30 result = CustomUser.objects.all().order_by('date_joined')[:10]
        # result = CustomUser.objects.filter(city__startswith='A', salary__gt=300000)
        # result = CustomUser.objects.filter(Q(department__isnull=True)|Q(department=None))
        # result = CustomUser.objects.values('country').annotate(count=Count('id'), avg_salary=Avg('salary')).order_by('-count')
        # result = CustomUser.objects.filter(is_staff=True).order_by('-last_login')
        # result = CustomUser.objects.exclude(email__icontains='example.com')

        # avg_salary = CustomUser.objects.aggregate(average_salary=Avg('salary'))
        # result = CustomUser.objects.filter(salary__gt=avg_salary['average_salary'])

        # 37 will be 0 because email = models.EmailField(unique=True)
        
        # result = CustomUser.objects.annotate(
        #     salary_level=Case(
        #         When(salary__lt=300000, then=Value('low')),
        #         When(salary__gte=300000, salary__lte=700000, then=Value('medium')),
        #         When(salary__gt=700000, then=Value('high')),
        #         default=Value('unknown'),
        #         output_field=CharField()
        #     )
        # ).order_by('salary_level', 'salary')

        # result = CustomUser.objects.filter(date_joined__year=2025) hardcode
        # 40 result = CustomUser.objects.values("department").annotate(sum=Sum('salary')).order_by('-sum')
        # result = CustomUser.objects.filter(department=CustomUser.Department.IT, last_login__isnull=True)
        # result = CustomUser.objects.filter(Q(city__isnull=True) | Q(city=""), country="Kazakhstan")
        # result = CustomUser.objects.filter(birth_date__lt=timezone.datetime(1990, 1, 1), salary__isnull=False)
        # result = CustomUser.objects.annotate(years_since_joined=ExtractYear(timezone.now()) - ExtractYear('date_joined')).values('first_name', 'last_name', 'years_since_joined')
        # result = CustomUser.objects.filter(department=CustomUser.Department.SALES, salary__gt=350000, email__endswith='@gmail.com')
        # result = CustomUser.objects.all().order_by('country', '-salary')
        # result = CustomUser.objects.values('role').annotate(count=Count('id')).filter(count__gt=100)
        # result = CustomUser.objects.filter(last_login__lt=F('date_joined'))
        
        # result = CustomUser.objects.values('first_name', 'last_name').annotate(is_senior=Case(
        #     When(birth_date__lt=timezone.datetime(1985, 1, 1), then=True),
        #     default=False,
        #     output_field=CharField()
        # ))
        result = CustomUser.objects.values('department').annotate(average_salary=Avg('salary'), count=Count('id')).order_by('-average_salary').filter(count__gt=20)
        print(result)
        # print(result.count())