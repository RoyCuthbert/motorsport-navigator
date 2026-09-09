import django.db.models.deletion
from django.db import migrations, models


def link_codrivers_to_drivers(apps, schema_editor):
    CoDriverProfile = apps.get_model(
        "codrivers",
        "CoDriverProfile",
    )

    DriverProfile = apps.get_model(
        "accounts",
        "DriverProfile",
    )

    for codriver in CoDriverProfile.objects.all():
        try:
            driver = DriverProfile.objects.get(
                user_id=codriver.user_id,
            )
        except DriverProfile.DoesNotExist:
            raise RuntimeError(
                f"No DriverProfile exists for user ID "
                f"{codriver.user_id}. "
                f"Create the DriverProfile before running this migration."
            )

        codriver.driver_id = driver.id
        codriver.save(
            update_fields=["driver"],
        )


class Migration(migrations.Migration):

    dependencies = [
        (
            "accounts",
            "0002_alter_driverprofile_options_and_more",
        ),
        (
            "codrivers",
            "0003_codriveremergencycontact",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="codriverprofile",
            name="driver",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="codrivers",
                to="accounts.driverprofile",
            ),
        ),

        migrations.RunPython(
            link_codrivers_to_drivers,
            migrations.RunPython.noop,
        ),

        migrations.RemoveField(
            model_name="codriverprofile",
            name="user",
        ),

        migrations.AlterField(
            model_name="codriverprofile",
            name="driver",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="codrivers",
                to="accounts.driverprofile",
            ),
        ),
    ]