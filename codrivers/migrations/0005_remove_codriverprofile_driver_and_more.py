from django.db import migrations, models


def copy_driver_to_many_to_many(apps, schema_editor):
    CoDriverProfile = apps.get_model(
        "codrivers",
        "CoDriverProfile",
    )

    through_model = CoDriverProfile.drivers.through

    for codriver in CoDriverProfile.objects.all():
        if codriver.driver_id:
            through_model.objects.create(
                codriverprofile_id=codriver.id,
                driverprofile_id=codriver.driver_id,
            )


class Migration(migrations.Migration):

    dependencies = [
        (
            "accounts",
            "0002_alter_driverprofile_options_and_more",
        ),
        (
            "codrivers",
            "0004_remove_codriverprofile_user_codriverprofile_driver",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="codriverprofile",
            name="drivers",
            field=models.ManyToManyField(
                related_name="codrivers",
                to="accounts.driverprofile",
            ),
        ),

        migrations.RunPython(
            copy_driver_to_many_to_many,
            migrations.RunPython.noop,
        ),

        migrations.RemoveField(
            model_name="codriverprofile",
            name="driver",
        ),
    ]