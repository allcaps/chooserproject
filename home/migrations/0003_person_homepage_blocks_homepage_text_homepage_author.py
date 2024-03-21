# Generated by Django 4.2.11 on 2024-03-21 15:21

from django.db import migrations, models
import django.db.models.deletion
import home.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_create_homepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='homepage',
            name='blocks',
            field=wagtail.fields.StreamField([('person', home.blocks.PersonChooserBlock())], blank=True, null=True, use_json_field=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='text',
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.person'),
        ),
    ]