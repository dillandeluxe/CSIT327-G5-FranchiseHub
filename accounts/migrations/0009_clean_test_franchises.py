from django.db import migrations


def remove_test_franchises(apps, schema_editor):
    try:
        Franchise = apps.get_model('accounts', 'Franchise')
        FranchiseApplication = apps.get_model('accounts', 'FranchiseApplication')
        UserFavorites = apps.get_model('accounts', 'UserFavorites')

        # Target sample and test franchises created during development
        test_qs = (
            Franchise.objects.filter(name__icontains='sample')
            | Franchise.objects.filter(description__icontains='asdasd')
            | Franchise.objects.filter(name__icontains='test')
            | Franchise.objects.filter(investment__lte=5000)
        )

        for franchise in test_qs:
            try:
                FranchiseApplication.objects.filter(franchise=franchise).delete()
            except Exception:
                pass
            try:
                UserFavorites.objects.filter(franchise=franchise).delete()
            except Exception:
                pass
            franchise.delete()
    except Exception:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_franchiseapplication_business_proposal_and_more'),
    ]

    operations = [
        migrations.RunPython(remove_test_franchises, reverse_code=migrations.RunPython.noop),
    ]
