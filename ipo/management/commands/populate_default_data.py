import os
from datetime import date, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from ipo.models import Company, IPO, FAQ, Document

class Command(BaseCommand):
    help = 'Populates the database with default IPO and Company data.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Populating default data...'))

        # Create Companies
        company1, created = Company.objects.get_or_create(name='Tech Innovators Inc.', defaults={'logo_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRgY1-dRCsa1G2RzMV9S8THGC9uSW9rgNGqqA&s'})
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created Company: {company1.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Company already exists: {company1.name}'))

        company2, created = Company.objects.get_or_create(name='Global Pharma Ltd.', defaults={'logo_url': 'https://global-pharma.com/gplogo.png'})
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created Company: {company2.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Company already exists: {company2.name}'))

        company3, created = Company.objects.get_or_create(name='Bluestock Innovations', defaults={'logo_url': 'https://bluestock.in/static/assets/logo/logo.webp'})
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created Company: {company3.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Company already exists: {company3.name}'))

        # Create IPOs
        today = date.today()

        ipo1, created = IPO.objects.get_or_create(
            company=company1,
            open_date=today + timedelta(days=7),
            close_date=today + timedelta(days=10),
            defaults={
                'price_band_lower': Decimal('100.00'),
                'price_band_upper': Decimal('110.00'),
                'issue_size': Decimal('1000.00'),
                'issue_type': 'book_building',
                'status': 'upcoming',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created IPO: {ipo1.company.name} (Upcoming)'))
        else:
            self.stdout.write(self.style.WARNING(f'IPO already exists for {ipo1.company.name} (Upcoming)'))

        # Add Documents for ipo1
        Document.objects.get_or_create(
            ipo=ipo1,
            defaults={'rhp_pdf': 'ipo_documents/rhp/tech_innovators_rhp.pdf', 'drhp_pdf': 'ipo_documents/drhp/tech_innovators_drhp.pdf'}
        )

        ipo2, created = IPO.objects.get_or_create(
            company=company2,
            open_date=today - timedelta(days=3),
            close_date=today + timedelta(days=1),
            defaults={
                'price_band_lower': Decimal('200.00'),
                'price_band_upper': Decimal('210.00'),
                'issue_size': Decimal('500.00'),
                'issue_type': 'fixed_price',
                'status': 'ongoing',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created IPO: {ipo2.company.name} (Ongoing)'))
        else:
            self.stdout.write(self.style.WARNING(f'IPO already exists for {ipo2.company.name} (Ongoing)'))

        ipo3, created = IPO.objects.get_or_create(
            company=company1,
            open_date=today - timedelta(days=30),
            close_date=today - timedelta(days=25),
            listing_date=today - timedelta(days=20),
            defaults={
                'price_band_lower': Decimal('80.00'),
                'price_band_upper': Decimal('90.00'),
                'issue_size': Decimal('1200.00'),
                'issue_type': 'book_building',
                'status': 'listed',
                'ipo_price': Decimal('85.00'),
                'listing_price': Decimal('100.00'),
                'current_market_price': Decimal('95.00'),
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created IPO: {ipo3.company.name} (Listed)'))
        else:
            self.stdout.write(self.style.WARNING(f'IPO already exists for {ipo3.company.name} (Listed)'))

        ipo4, created = IPO.objects.get_or_create(
            company=company3,
            open_date=today + timedelta(days=14),
            close_date=today + timedelta(days=17),
            defaults={
                'price_band_lower': Decimal('250.00'),
                'price_band_upper': Decimal('270.00'),
                'issue_size': Decimal('750.00'),
                'issue_type': 'book_building',
                'status': 'upcoming',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created IPO: {ipo4.company.name} (Upcoming)'))
        else:
            self.stdout.write(self.style.WARNING(f'IPO already exists for {ipo4.company.name} (Upcoming)'))

        ipo5, created = IPO.objects.get_or_create(
            company=company2,
            open_date=today + timedelta(days=21),
            close_date=today + timedelta(days=24),
            defaults={
                'price_band_lower': Decimal('150.00'),
                'price_band_upper': Decimal('160.00'),
                'issue_size': Decimal('400.00'),
                'issue_type': 'fixed_price',
                'status': 'upcoming',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created IPO: {ipo5.company.name} (Upcoming)'))
        else:
            self.stdout.write(self.style.WARNING(f'IPO already exists for {ipo5.company.name} (Upcoming)'))

        # Create FAQs
        faq1, created = FAQ.objects.get_or_create(
            question='What is an IPO?',
            defaults={'answer': 'An Initial Public Offering (IPO) is the process by which a private company can go public by offering its shares to the public.', 'order': 1}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created FAQ: {faq1.question}'))
        else:
            self.stdout.write(self.style.WARNING(f'FAQ already exists: {faq1.question}'))

        faq2, created = FAQ.objects.get_or_create(
            question='How can I apply for an IPO?',
            defaults={'answer': 'You can apply for an IPO through your demat account linked with a brokerage firm via ASBA (Application Supported by Blocked Amount).', 'order': 2}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created FAQ: {faq2.question}'))
        else:
            self.stdout.write(self.style.WARNING(f'FAQ already exists: {faq2.question}'))


        self.stdout.write(self.style.SUCCESS('Default data population complete.'))