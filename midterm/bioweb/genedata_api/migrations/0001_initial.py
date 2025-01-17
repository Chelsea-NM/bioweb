# Generated by Django 4.1.2 on 2023-07-16 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="domains",
            fields=[
                (
                    "domainID",
                    models.CharField(max_length=255, primary_key=True, serialize=False),
                ),
                ("pfamFamilyDescription", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="proteins",
            fields=[
                (
                    "proteinID",
                    models.CharField(max_length=255, primary_key=True, serialize=False),
                ),
                ("sequence", models.TextField(max_length=40000)),
            ],
        ),
        migrations.CreateModel(
            name="domainAssignment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("organismTaxaID", models.CharField(max_length=255)),
                ("organismCladeIdenitifer", models.CharField(max_length=255)),
                ("organismScientificName", models.CharField(max_length=255)),
                ("domainDescription", models.CharField(max_length=255)),
                ("domainStart", models.IntegerField()),
                ("domainEndCoordinate", models.IntegerField()),
                ("lengthProtein", models.IntegerField()),
                (
                    "domainID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="genedata_api.domains",
                    ),
                ),
                (
                    "protein",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="genedata_api.proteins",
                    ),
                ),
            ],
        ),
    ]
