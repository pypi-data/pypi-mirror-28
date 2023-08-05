from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('paypal', '0005_auto_20180110_0330'),
    ]

    operations = [
        migrations.RenameModel('paypaltransaction', 'paypalpayment')
    ]
