# Generated by Django 3.1.4 on 2021-11-02 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='labels',
            fields=[
                ('label_id', models.AutoField(primary_key=True, serialize=False)),
                ('label_tile', models.CharField(blank=True, max_length=128, null=True)),
                ('label_sub_title', models.CharField(blank=True, max_length=128, null=True)),
                ('label_content', models.CharField(blank=True, max_length=256, null=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'labels',
            },
        ),
    ]