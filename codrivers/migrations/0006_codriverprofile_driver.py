import django.db.models.deletion
from django.db import migrations, models


def copy_driver_relationship(apps, schema_editor):
    CoDriverProfile = apps.get_model(
        "codrivers",
        "CoDriverProfile",
    )

    for codriver in CoDriverProfile.objects.all():
        drivers = list(
            codriver.drivers.all()
        )

        if len(drivers) == 1:
            codriver.driver_id = drivers[0].id
            codriver.save(
                update_fields=["driver"],
            )

        elif len(drivers) == 0:
            raise RuntimeError(
                f"Co-driver ID {codriver.id} has no linked driver."
            )

        else:
            raise RuntimeError(
                f"Co-driver ID {codriver.id} is linked to "
                f"{len(drivers)} drivers. This must be resolved "
                f"before converting to private driver-owned profiles."
            )


class Migration(migrations.Migration):

    dependencies = [
        (
            "accounts",
            "0002_alter_driverprofile_options_and_more",
        ),
        (
            "codrivers",
            "0005_remove_codriverprofile_driver_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="codriverprofile",
            name="driver",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="owned_codrivers",
                to="accounts.driverprofile",
            ),
        ),

        migrations.RunPython(
            copy_driver_relationship,
            migrations.RunPython.noop,
        ),
    ]