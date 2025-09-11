from datetime import date, datetime, timedelta
from django.db import migrations, models
import django.db.models.deletion


def migrate_orderables(apps, schema_editor):
    Event = apps.get_model("ddmlanskroun", "Event")
    Orderable = apps.get_model("ddmlanskroun", "Orderable")
    events = Event.objects.filter(activity_ptr__activity_type__model="orderable")
    d = date(2025, 1, 1)
    Orderable.objects.bulk_create(
        Orderable(
            activity_ptr_id=event.activity_ptr_id,
            duration=(
                datetime.combine(d, event.end_time)
                - datetime.combine(d, event.start_time)
                if event.start_time
                and event.end_time
                and event.start_time < event.end_time
                else timedelta(hours=2)
            ),
            preparation_time=timedelta(0),
            recovery_time=timedelta(0),
            due_from_days=14,
            due_date_days=14,
            min_due_date_days=event.min_due_date_days,
        )
        for event in events
    )
    events.delete()

    EventRegistration = apps.get_model("ddmlanskroun", "EventRegistration")
    OrderableRegistration = apps.get_model("ddmlanskroun", "OrderableRegistration")
    event_registrations = EventRegistration.objects.filter(
        registration_ptr__activity__activity_type__model="orderable"
    )
    OrderableRegistration.objects.bulk_create(
        OrderableRegistration(registration_ptr_id=registration.registration_ptr_id)
        for registration in event_registrations
    )
    event_registrations.delete()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("leprikon", "0092_calendar_event_effective_times"),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "activity_ptr",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="+",
                        serialize=False,
                        to="leprikon.activity",
                    ),
                ),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("start_time", models.TimeField(blank=True, null=True)),
                ("end_time", models.TimeField(blank=True, null=True)),
                ("due_from", models.DateField()),
                ("due_date", models.DateField()),
                ("min_due_date_days", models.PositiveIntegerField()),
            ],
            options={"db_table": "leprikon_event", "managed": False},
        ),
        migrations.CreateModel(
            name="Orderable",
            fields=[
                (
                    "activity_ptr",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="+",
                        serialize=False,
                        to="leprikon.activity",
                    ),
                ),
                ("duration", models.DurationField()),
                ("preparation_time", models.DurationField()),
                ("recovery_time", models.DurationField()),
                ("due_from_days", models.IntegerField(blank=True, null=True)),
                ("due_date_days", models.IntegerField()),
                ("min_due_date_days", models.PositiveIntegerField()),
            ],
            options={"db_table": "leprikon_orderable", "managed": False},
        ),
        migrations.CreateModel(
            name="EventRegistration",
            fields=[
                (
                    "registration_ptr",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="+",
                        serialize=False,
                        to="leprikon.registration",
                    ),
                ),
            ],
            options={"db_table": "leprikon_eventregistration", "managed": False},
        ),
        migrations.CreateModel(
            name="OrderableRegistration",
            fields=[
                (
                    "registration_ptr",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="+",
                        serialize=False,
                        to="leprikon.registration",
                    ),
                ),
            ],
            options={"db_table": "leprikon_orderableregistration", "managed": False},
        ),
        migrations.RunPython(migrate_orderables),
        migrations.DeleteModel(name="Event"),
        migrations.DeleteModel(name="EventRegistration"),
        migrations.DeleteModel(name="Orderable"),
        migrations.DeleteModel(name="OrderableRegistration"),
    ]
