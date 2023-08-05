# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-30 17:47
from __future__ import unicode_literals

import django.core.validators
import django.db.migrations.operations.special
import django.db.models.deletion
import django_countries.fields
import i18nfield.fields
from django.conf import settings
from django.core.cache import cache
from django.db import migrations, models

import pretix.base.models.base
import pretix.base.models.event
import pretix.base.models.invoices
import pretix.base.models.orders
import pretix.base.models.organizer
import pretix.base.validators


def create_teams(apps, schema_editor):
    Organizer = apps.get_model('pretixbase', 'Organizer')
    Team = apps.get_model('pretixbase', 'Team')

    for o in Organizer.objects.prefetch_related('events'):
        for e in o.events.all():
            teams = {}

            for p in e.user_perms.all():
                pkey = (p.can_change_settings, p.can_change_items, p.can_view_orders,
                        p.can_change_permissions, p.can_change_orders, p.can_view_vouchers,
                        p.can_change_vouchers)
                if pkey not in teams:
                    team = Team()
                    team.can_change_event_settings = p.can_change_settings
                    team.can_change_items = p.can_change_items
                    team.can_view_orders = p.can_view_orders
                    team.can_change_orders = p.can_change_orders
                    team.can_view_vouchers = p.can_view_vouchers
                    team.can_change_vouchers = p.can_change_vouchers
                    team.organizer = o
                    team.name = '{} Team {}'.format(
                        str(e.name), len(teams) + 1
                    )
                    team.save()
                    team.limit_events.add(e)

                    teams[pkey] = team

                if p.user:
                    teams[pkey].members.add(p.user)
                else:
                    teams[pkey].invites.create(email=p.invite_email, token=p.invite_token)

        teams = {}
        for p in o.user_perms.all():
            pkey = (p.can_create_events, p.can_change_permissions)
            if pkey not in teams:
                team = Team()
                team.can_change_organizer_settings = True
                team.can_create_events = p.can_create_events
                team.can_change_teams = p.can_change_permissions
                team.organizer = o
                team.name = '{} Team {}'.format(
                    str(o.name), len(teams) + 1
                )
                team.save()
                teams[pkey] = team

            if p.user:
                teams[pkey].members.add(p.user)
            else:
                teams[pkey].invites.create(email=p.invite_email, token=p.invite_token)


def rename_placeholder(app, schema_editor):
    EventSettingsStore = app.get_model('pretixbase', 'Event_SettingsStore')

    for setting in EventSettingsStore.objects.all():
        if setting.key == 'mail_text_order_placed':
            new_value = setting.value.replace('{paymentinfo}', '{payment_info}')
            setting.value = new_value
            cache.delete('hierarkey_{}_{}'.format('event', setting.object_id))
            setting.save()


def fwd69(app, schema_editor):
    Event = app.get_model('pretixbase', 'Event')
    for e in Event.objects.select_related('organizer').all():
        e.invoices.all().update(prefix=e.slug.upper() + '-', organizer=e.organizer)


def fwd70(app, schema_editor):
    InvoiceAddress = app.get_model('pretixbase', 'InvoiceAddress')
    for ia in InvoiceAddress.objects.all():
        if ia.company or ia.vat_id:
            ia.is_business = True
            ia.save()


class Migration(migrations.Migration):
    replaces = [('pretixbase', '0052_team_teaminvite'), ('pretixbase', '0058_auto_20170429_1020'),
                ('pretixbase', '0059_checkin_nonce'), ('pretixbase', '0060_auto_20170510_1027'),
                ('pretixbase', '0061_auto_20170521_0942'), ('pretixbase', '0062_auto_20170602_0948'),
                ('pretixbase', '0063_auto_20170702_1711'), ('pretixbase', '0064_auto_20170703_0912'),
                ('pretixbase', '0065_auto_20170707_0920'), ('pretixbase', '0066_auto_20170708_2102'),
                ('pretixbase', '0067_auto_20170712_1610'), ('pretixbase', '0068_subevent_frontpage_text'),
                ('pretixbase', '0069_invoice_prefix'), ('pretixbase', '0070_auto_20170719_0910')]

    dependencies = [
        ('pretixbase', '0051_auto_20170206_2027_squashed_0057_auto_20170501_2116'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=190, verbose_name='Team name')),
                ('all_events',
                 models.BooleanField(default=False, verbose_name='All events (including newly created ones)')),
                ('can_create_events', models.BooleanField(default=False, verbose_name='Can create events')),
                ('can_change_teams', models.BooleanField(default=False, verbose_name='Can change permissions')),
                ('can_change_organizer_settings',
                 models.BooleanField(default=False, verbose_name='Can change organizer settings')),
                ('can_change_event_settings',
                 models.BooleanField(default=False, verbose_name='Can change event settings')),
                ('can_change_items', models.BooleanField(default=False, verbose_name='Can change product settings')),
                ('can_view_orders', models.BooleanField(default=False, verbose_name='Can view orders')),
                ('can_change_orders', models.BooleanField(default=False, verbose_name='Can change orders')),
                ('can_view_vouchers', models.BooleanField(default=False, verbose_name='Can view vouchers')),
                ('can_change_vouchers', models.BooleanField(default=False, verbose_name='Can change vouchers')),
                ('limit_events', models.ManyToManyField(to='pretixbase.Event', verbose_name='Limit to events')),
                ('members', models.ManyToManyField(related_name='teams', to=settings.AUTH_USER_MODEL,
                                                   verbose_name='Team members')),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams',
                                                to='pretixbase.Organizer')),
            ],
            options={
                'verbose_name_plural': 'Teams',
                'verbose_name': 'Team',
            },
        ),
        migrations.CreateModel(
            name='TeamInvite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('token',
                 models.CharField(blank=True, default=pretix.base.models.organizer.generate_invite_token, max_length=64,
                                  null=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invites',
                                           to='pretixbase.Team')),
            ],
        ),
        migrations.RunPython(
            code=create_teams,
            reverse_code=django.db.migrations.operations.special.RunPython.noop,
        ),
        migrations.RemoveField(
            model_name='eventpermission',
            name='event',
        ),
        migrations.RemoveField(
            model_name='eventpermission',
            name='user',
        ),
        migrations.RemoveField(
            model_name='organizerpermission',
            name='organizer',
        ),
        migrations.RemoveField(
            model_name='organizerpermission',
            name='user',
        ),
        migrations.RemoveField(
            model_name='event',
            name='permitted',
        ),
        migrations.RemoveField(
            model_name='organizer',
            name='permitted',
        ),
        migrations.AlterField(
            model_name='team',
            name='can_change_teams',
            field=models.BooleanField(default=False, verbose_name='Can change teams and permissions'),
        ),
        migrations.AlterField(
            model_name='team',
            name='limit_events',
            field=models.ManyToManyField(blank=True, to='pretixbase.Event', verbose_name='Limit to events'),
        ),
        migrations.DeleteModel(
            name='EventPermission',
        ),
        migrations.DeleteModel(
            name='OrganizerPermission',
        ),
        migrations.AddField(
            model_name='checkin',
            name='nonce',
            field=models.CharField(blank=True, max_length=190, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='date_admission',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Admission time'),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=i18nfield.fields.I18nTextField(blank=True, max_length=200, null=True, verbose_name='Location'),
        ),
        migrations.RunPython(
            code=rename_placeholder,
            reverse_code=django.db.migrations.operations.special.RunPython.noop,
        ),
        migrations.CreateModel(
            name='TeamAPIToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=190)),
                ('active', models.BooleanField(default=True)),
                ('token', models.CharField(default=pretix.base.models.organizer.generate_api_token, max_length=64)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tokens',
                                           to='pretixbase.Team')),
            ],
        ),
        migrations.AlterModelOptions(
            name='voucher',
            options={'ordering': ('code',), 'verbose_name': 'Voucher', 'verbose_name_plural': 'Vouchers'},
        ),
        migrations.AddField(
            model_name='cartposition',
            name='meta_info',
            field=models.TextField(blank=True, null=True, verbose_name='Meta information'),
        ),
        migrations.AddField(
            model_name='orderposition',
            name='meta_info',
            field=models.TextField(blank=True, null=True, verbose_name='Meta information'),
        ),
        migrations.AlterField(
            model_name='event',
            name='currency',
            field=models.CharField(choices=[('AED', 'AED - UAE Dirham'), ('AFN', 'AFN - Afghani'), ('ALL', 'ALL - Lek'),
                                            ('AMD', 'AMD - Armenian Dram'),
                                            ('ANG', 'ANG - Netherlands Antillean Guilder'),
                                            ('AOA', 'AOA - Kwanza'), ('ARS', 'ARS - Argentine Peso'),
                                            ('AUD', 'AUD - Australian Dollar'), ('AWG', 'AWG - Aruban Florin'),
                                            ('AZN', 'AZN - Azerbaijanian Manat'), ('BAM', 'BAM - Convertible Mark'),
                                            ('BBD', 'BBD - Barbados Dollar'), ('BDT', 'BDT - Taka'),
                                            ('BGN', 'BGN - Bulgarian Lev'), ('BHD', 'BHD - Bahraini Dinar'),
                                            ('BIF', 'BIF - Burundi Franc'), ('BMD', 'BMD - Bermudian Dollar'),
                                            ('BND', 'BND - Brunei Dollar'), ('BOB', 'BOB - Boliviano'),
                                            ('BRL', 'BRL - Brazilian Real'), ('BSD', 'BSD - Bahamian Dollar'),
                                            ('BTN', 'BTN - Ngultrum'), ('BWP', 'BWP - Pula'),
                                            ('BYN', 'BYN - Belarusian Ruble'), ('BZD', 'BZD - Belize Dollar'),
                                            ('CAD', 'CAD - Canadian Dollar'), ('CDF', 'CDF - Congolese Franc'),
                                            ('CHF', 'CHF - Swiss Franc'), ('CLP', 'CLP - Chilean Peso'),
                                            ('CNY', 'CNY - Yuan Renminbi'), ('COP', 'COP - Colombian Peso'),
                                            ('CRC', 'CRC - Costa Rican Colon'), ('CUC', 'CUC - Peso Convertible'),
                                            ('CUP', 'CUP - Cuban Peso'), ('CVE', 'CVE - Cabo Verde Escudo'),
                                            ('CZK', 'CZK - Czech Koruna'), ('DJF', 'DJF - Djibouti Franc'),
                                            ('DKK', 'DKK - Danish Krone'), ('DOP', 'DOP - Dominican Peso'),
                                            ('DZD', 'DZD - Algerian Dinar'), ('EGP', 'EGP - Egyptian Pound'),
                                            ('ERN', 'ERN - Nakfa'), ('ETB', 'ETB - Ethiopian Birr'),
                                            ('EUR', 'EUR - Euro'),
                                            ('FJD', 'FJD - Fiji Dollar'), ('FKP', 'FKP - Falkland Islands Pound'),
                                            ('GBP', 'GBP - Pound Sterling'), ('GEL', 'GEL - Lari'),
                                            ('GHS', 'GHS - Ghana Cedi'), ('GIP', 'GIP - Gibraltar Pound'),
                                            ('GMD', 'GMD - Dalasi'), ('GNF', 'GNF - Guinea Franc'),
                                            ('GTQ', 'GTQ - Quetzal'), ('GYD', 'GYD - Guyana Dollar'),
                                            ('HKD', 'HKD - Hong Kong Dollar'), ('HNL', 'HNL - Lempira'),
                                            ('HRK', 'HRK - Kuna'), ('HTG', 'HTG - Gourde'), ('HUF', 'HUF - Forint'),
                                            ('IDR', 'IDR - Rupiah'), ('ILS', 'ILS - New Israeli Sheqel'),
                                            ('INR', 'INR - Indian Rupee'), ('IQD', 'IQD - Iraqi Dinar'),
                                            ('IRR', 'IRR - Iranian Rial'), ('ISK', 'ISK - Iceland Krona'),
                                            ('JMD', 'JMD - Jamaican Dollar'), ('JOD', 'JOD - Jordanian Dinar'),
                                            ('JPY', 'JPY - Yen'), ('KES', 'KES - Kenyan Shilling'),
                                            ('KGS', 'KGS - Som'),
                                            ('KHR', 'KHR - Riel'), ('KMF', 'KMF - Comoro Franc'),
                                            ('KPW', 'KPW - North Korean Won'), ('KRW', 'KRW - Won'),
                                            ('KWD', 'KWD - Kuwaiti Dinar'), ('KYD', 'KYD - Cayman Islands Dollar'),
                                            ('KZT', 'KZT - Tenge'), ('LAK', 'LAK - Kip'),
                                            ('LBP', 'LBP - Lebanese Pound'),
                                            ('LKR', 'LKR - Sri Lanka Rupee'), ('LRD', 'LRD - Liberian Dollar'),
                                            ('LSL', 'LSL - Loti'), ('LYD', 'LYD - Libyan Dinar'),
                                            ('MAD', 'MAD - Moroccan Dirham'), ('MDL', 'MDL - Moldovan Leu'),
                                            ('MGA', 'MGA - Malagasy Ariary'), ('MKD', 'MKD - Denar'),
                                            ('MMK', 'MMK - Kyat'),
                                            ('MNT', 'MNT - Tugrik'), ('MOP', 'MOP - Pataca'), ('MRO', 'MRO - Ouguiya'),
                                            ('MUR', 'MUR - Mauritius Rupee'), ('MVR', 'MVR - Rufiyaa'),
                                            ('MWK', 'MWK - Malawi Kwacha'), ('MXN', 'MXN - Mexican Peso'),
                                            ('MYR', 'MYR - Malaysian Ringgit'), ('MZN', 'MZN - Mozambique Metical'),
                                            ('NAD', 'NAD - Namibia Dollar'), ('NGN', 'NGN - Naira'),
                                            ('NIO', 'NIO - Cordoba Oro'), ('NOK', 'NOK - Norwegian Krone'),
                                            ('NPR', 'NPR - Nepalese Rupee'), ('NZD', 'NZD - New Zealand Dollar'),
                                            ('OMR', 'OMR - Rial Omani'), ('PAB', 'PAB - Balboa'), ('PEN', 'PEN - Sol'),
                                            ('PGK', 'PGK - Kina'), ('PHP', 'PHP - Philippine Peso'),
                                            ('PKR', 'PKR - Pakistan Rupee'), ('PLN', 'PLN - Zloty'),
                                            ('PYG', 'PYG - Guarani'), ('QAR', 'QAR - Qatari Rial'),
                                            ('RON', 'RON - Romanian Leu'), ('RSD', 'RSD - Serbian Dinar'),
                                            ('RUB', 'RUB - Russian Ruble'), ('RWF', 'RWF - Rwanda Franc'),
                                            ('SAR', 'SAR - Saudi Riyal'), ('SBD', 'SBD - Solomon Islands Dollar'),
                                            ('SCR', 'SCR - Seychelles Rupee'), ('SDG', 'SDG - Sudanese Pound'),
                                            ('SEK', 'SEK - Swedish Krona'), ('SGD', 'SGD - Singapore Dollar'),
                                            ('SHP', 'SHP - Saint Helena Pound'), ('SLL', 'SLL - Leone'),
                                            ('SOS', 'SOS - Somali Shilling'), ('SRD', 'SRD - Surinam Dollar'),
                                            ('SSP', 'SSP - South Sudanese Pound'), ('STD', 'STD - Dobra'),
                                            ('SVC', 'SVC - El Salvador Colon'), ('SYP', 'SYP - Syrian Pound'),
                                            ('SZL', 'SZL - Lilangeni'), ('THB', 'THB - Baht'), ('TJS', 'TJS - Somoni'),
                                            ('TMT', 'TMT - Turkmenistan New Manat'), ('TND', 'TND - Tunisian Dinar'),
                                            ('TOP', 'TOP - Pa’anga'), ('TRY', 'TRY - Turkish Lira'),
                                            ('TTD', 'TTD - Trinidad and Tobago Dollar'),
                                            ('TWD', 'TWD - New Taiwan Dollar'),
                                            ('TZS', 'TZS - Tanzanian Shilling'), ('UAH', 'UAH - Hryvnia'),
                                            ('UGX', 'UGX - Uganda Shilling'), ('USD', 'USD - US Dollar'),
                                            ('UYU', 'UYU - Peso Uruguayo'), ('UZS', 'UZS - Uzbekistan Sum'),
                                            ('VEF', 'VEF - Bolívar'), ('VND', 'VND - Dong'), ('VUV', 'VUV - Vatu'),
                                            ('WST', 'WST - Tala'), ('XAF', 'XAF - CFA Franc BEAC'),
                                            ('XAG', 'XAG - Silver'),
                                            ('XAU', 'XAU - Gold'),
                                            ('XBA', 'XBA - Bond Markets Unit European Composite Unit (EURCO)'),
                                            ('XBB', 'XBB - Bond Markets Unit European Monetary Unit (E.M.U.-6)'),
                                            ('XBC', 'XBC - Bond Markets Unit European Unit of Account 9 (E.U.A.-9)'),
                                            ('XBD', 'XBD - Bond Markets Unit European Unit of Account 17 (E.U.A.-17)'),
                                            ('XCD', 'XCD - East Caribbean Dollar'),
                                            ('XDR', 'XDR - SDR (Special Drawing Right)'),
                                            ('XOF', 'XOF - CFA Franc BCEAO'),
                                            ('XPD', 'XPD - Palladium'), ('XPF', 'XPF - CFP Franc'),
                                            ('XPT', 'XPT - Platinum'), ('XSU', 'XSU - Sucre'),
                                            ('XTS', 'XTS - Codes specifically reserved for testing purposes'),
                                            ('XUA', 'XUA - ADB Unit of Account'), ('XXX',
                                                                                   'XXX - The codes assigned for transactions where no currency is involved'),
                                            ('YER', 'YER - Yemeni Rial'), ('ZAR', 'ZAR - Rand'),
                                            ('ZMW', 'ZMW - Zambian Kwacha'), ('ZWL', 'ZWL - Zimbabwe Dollar')],
                                   default='EUR', max_length=10, verbose_name='Default currency'),
        ),
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.SlugField(
                help_text='Should be short, only contain lowercase letters and numbers, and must be unique among your events. We recommend some kind of abbreviation or a date with less than 10 characters that can be easily remembered, but you can also choose to use a random value. This will be used in URLs, order codes, invoice numbers, and bank transfer references.',
                validators=[django.core.validators.RegexValidator(
                    message='The slug may only contain letters, numbers, dots and dashes.', regex='^[a-zA-Z0-9.-]+$'),
                    pretix.base.validators.EventSlugBlacklistValidator()], verbose_name='Short form'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=models.DateField(default=pretix.base.models.invoices.today),
        ),
        migrations.AlterField(
            model_name='item',
            name='allow_cancel',
            field=models.BooleanField(default=True,
                                      help_text='If this is active and the general event settings allow it, orders containing this product can be canceled by the user until the order is paid for. Users cannot cancel paid orders on their own and you can cancel orders at all times, regardless of this setting',
                                      verbose_name='Allow product to be canceled'),
        ),
        migrations.AddField(
            model_name='questionanswer',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=pretix.base.models.orders.answerfile_name),
        ),
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.CharField(
                choices=[('N', 'Number'), ('S', 'Text (one line)'), ('T', 'Multiline text'), ('B', 'Yes/No'),
                         ('C', 'Choose one from a list'), ('M', 'Choose multiple from a list'), ('F', 'File upload')],
                max_length=5, verbose_name='Question type'),
        ),
        migrations.AddField(
            model_name='event',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Internal comment'),
        ),
        migrations.AlterField(
            model_name='event',
            name='presale_end',
            field=models.DateTimeField(blank=True, help_text='Optional. No products will be sold after this date.',
                                       null=True, verbose_name='End of presale'),
        ),
        migrations.AlterField(
            model_name='event',
            name='presale_start',
            field=models.DateTimeField(blank=True, help_text='Optional. No products will be sold before this date.',
                                       null=True, verbose_name='Start of presale'),
        ),
        migrations.CreateModel(
            name='SubEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False,
                                               help_text='Only with this checkbox enabled, this sub-event is visible in the frontend to users.',
                                               verbose_name='Active')),
                ('name', i18nfield.fields.I18nCharField(max_length=200, verbose_name='Name')),
                ('date_from', models.DateTimeField(verbose_name='Event start time')),
                ('date_to', models.DateTimeField(blank=True, null=True, verbose_name='Event end time')),
                ('date_admission', models.DateTimeField(blank=True, null=True, verbose_name='Admission time')),
                ('presale_end',
                 models.DateTimeField(blank=True, help_text='No products will be sold after this date.', null=True,
                                      verbose_name='End of presale')),
                ('presale_start',
                 models.DateTimeField(blank=True, help_text='No products will be sold before this date.', null=True,
                                      verbose_name='Start of presale')),
                (
                    'location',
                    i18nfield.fields.I18nTextField(blank=True, max_length=200, null=True, verbose_name='Location')),
            ],
            options={
                'verbose_name': 'Sub-Event',
                'verbose_name_plural': 'Sub-Events',
                'ordering': ('date_from', 'name'),
            },
            bases=(pretix.base.models.event.EventMixin, models.Model, pretix.base.models.base.LoggingMixin),
        ),
        migrations.CreateModel(
            name='SubEventItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pretixbase.Item')),
                ('subevent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pretixbase.SubEvent')),
            ],
        ),
        migrations.CreateModel(
            name='SubEventItemVariation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('subevent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pretixbase.SubEvent')),
                (
                    'variation',
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pretixbase.ItemVariation')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='has_subevents',
            field=models.BooleanField(default=False, verbose_name='Event series'),
        ),
        migrations.AddField(
            model_name='subevent',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subevents',
                                    to='pretixbase.Event'),
        ),
        migrations.AddField(
            model_name='subevent',
            name='items',
            field=models.ManyToManyField(through='pretixbase.SubEventItem', to='pretixbase.Item'),
        ),
        migrations.AddField(
            model_name='subevent',
            name='variations',
            field=models.ManyToManyField(through='pretixbase.SubEventItemVariation', to='pretixbase.ItemVariation'),
        ),
        migrations.AddField(
            model_name='cartposition',
            name='subevent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='pretixbase.SubEvent', verbose_name='Date'),
        ),
        migrations.AddField(
            model_name='orderposition',
            name='subevent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='pretixbase.SubEvent', verbose_name='Date'),
        ),
        migrations.AddField(
            model_name='quota',
            name='subevent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='quotas', to='pretixbase.SubEvent', verbose_name='Date'),
        ),
        migrations.AddField(
            model_name='voucher',
            name='subevent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='pretixbase.SubEvent', verbose_name='Date'),
        ),
        migrations.AddField(
            model_name='waitinglistentry',
            name='subevent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='pretixbase.SubEvent', verbose_name='Date'),
        ),
        migrations.AlterModelOptions(
            name='subevent',
            options={'ordering': ('date_from', 'name'), 'verbose_name': 'Date in event series',
                     'verbose_name_plural': 'Dates in event series'},
        ),
        migrations.AddField(
            model_name='itemaddon',
            name='price_included',
            field=models.BooleanField(default=False,
                                      help_text='If selected, adding add-ons to this ticket is free, even if the add-ons would normally cost money individually.',
                                      verbose_name='Add-Ons are included in the price'),
        ),
        migrations.AlterField(
            model_name='subevent',
            name='active',
            field=models.BooleanField(default=False,
                                      help_text='Only with this checkbox enabled, this date is visible in the frontend to users.',
                                      verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='subevent',
            name='presale_end',
            field=models.DateTimeField(blank=True, help_text='Optional. No products will be sold after this date.',
                                       null=True, verbose_name='End of presale'),
        ),
        migrations.AlterField(
            model_name='subevent',
            name='presale_start',
            field=models.DateTimeField(blank=True, help_text='Optional. No products will be sold before this date.',
                                       null=True, verbose_name='Start of presale'),
        ),
        migrations.AddField(
            model_name='subevent',
            name='frontpage_text',
            field=i18nfield.fields.I18nTextField(blank=True, null=True, verbose_name='Frontpage text'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='prefix',
            field=models.CharField(db_index=True, default='', max_length=160),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoice',
            name='organizer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='invoices',
                                    to='pretixbase.Organizer'),
            preserve_default=False,
        ),
        migrations.RunPython(
            code=fwd69, reverse_code=django.db.migrations.operations.special.RunPython.noop,
        ),
        migrations.AlterUniqueTogether(
            name='invoice',
            unique_together=set([('organizer', 'prefix', 'invoice_no')]),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='organizer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='invoices',
                                    to='pretixbase.Organizer'),
        ),
        migrations.RenameField(
            model_name='invoiceaddress',
            old_name='country',
            new_name='country_old',
        ),
        migrations.AddField(
            model_name='invoiceaddress',
            name='country',
            field=django_countries.fields.CountryField(default='', max_length=2, verbose_name='Country'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoiceaddress',
            name='is_business',
            field=models.BooleanField(default=False, verbose_name='Business customer'),
        ),
        migrations.RunPython(
            code=fwd70, reverse_code=django.db.migrations.operations.special.RunPython.noop,
        ),
    ]
