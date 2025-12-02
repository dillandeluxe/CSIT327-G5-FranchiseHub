"""
Management command to clear all franchise data from the database.
Usage: python manage.py clear_franchises
"""

from django.core.management.base import BaseCommand
from accounts.models import Franchise, FranchiseApplication


class Command(BaseCommand):
    help = 'Deletes all franchises and applications from the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm deletion without prompting',
        )

    def handle(self, *args, **options):
        confirm = options.get('confirm')
        
        # Count records
        franchise_count = Franchise.objects.count()
        application_count = FranchiseApplication.objects.count()
        
        if franchise_count == 0 and application_count == 0:
            self.stdout.write(self.style.SUCCESS('✅ Database is already clean - no franchises or applications found.'))
            return
        
        self.stdout.write(self.style.WARNING(f'Found {franchise_count} franchises and {application_count} applications.'))
        
        if not confirm:
            response = input('Are you sure you want to delete ALL franchises and applications? [y/N]: ')
            if response.lower() != 'y':
                self.stdout.write(self.style.ERROR('❌ Operation cancelled.'))
                return
        
        # Delete all applications first (due to foreign key)
        FranchiseApplication.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'✅ Deleted {application_count} applications'))
        
        # Delete all franchises
        Franchise.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'✅ Deleted {franchise_count} franchises'))
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Database cleaned successfully!'))
