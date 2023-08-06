django-slxauth
==============

Consult the django-project-template on how to use it.

Upgrade from 1.7 to 1.8
-----------------------

In 1.8 there is a new username column introduced which removes unique identification responsibility from the email
column. To migrate existing users and populate the DB sucessfully add the following script to your migrations.
Fix the model name as needed and update the dependency to the last previous migration.

Afterwards run makemigrations as usual to update other fields.

populate username migration::

    import django.contrib.auth.validators
    from django.db import migrations, models


    def populate_usernames(apps, schema_editor):
        User = apps.get_model('example', 'MyUser')
        for u in User.objects.all().iterator():
            if u.um_id:
                u.username = 'um_%s' % u.um_id
            else:
                u.username = 'user_%s' % u.id
            u.save()


    class Migration(migrations.Migration):

        dependencies = [
            ('example', '0008_auto_20180208_1019'),
        ]

        operations = [
            migrations.AddField(
                model_name='myuser',
                name='username',
                field=models.CharField(null=True,
                                       error_messages={'unique': 'A user with that username already exists.'},
                                       help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                                       max_length=150, unique=True,
                                       validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                                       verbose_name='username'),
            ),
            migrations.RunPython(populate_usernames),
            migrations.AlterField(
                model_name='myuser',
                name='username',
                field=models.CharField(error_messages={'unique': 'A user with that username already exists.'},
                                       help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                                       max_length=150, unique=True,
                                       validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                                       verbose_name='username'),
            )
        ]
