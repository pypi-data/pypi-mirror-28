from django.core import checks
from django.db import models

from . import fields
from ...conf import settings

__all__ = ('HerokuConnectModel',)


class HerokuConnectModelBase(models.base.ModelBase):
    """
    Custom model base class to set ``Meta`` attributes.

    Sets :attr:`Meta.managed<django.db.models.Options.managed>` to ``False``
    and sets a default value for :attr:`Meta.db_table<django.db.models.Options.db_table>`.
    """

    def __new__(mcs, name, bases, attrs):
        super_new = super(HerokuConnectModelBase, mcs).__new__
        # We need t create a temporary fake model class to access
        # the original Meta class since ModelBase will remove it.
        fake_class = type.__new__(mcs, name, bases, attrs)
        org_meta_attr = getattr(fake_class, 'Meta', None)
        new_class = super_new(mcs, name, bases, attrs)
        if org_meta_attr is None or not hasattr(org_meta_attr, 'db_table'):
            new_class._meta.db_table = '{schema}"."{table}'.format(
                schema=settings.HEROKU_CONNECT_SCHEMA,
                table=new_class.sf_object_name.lower(),
            )

        # User object in Heroku Connect has no is_deleted field.
        if new_class.sf_object_name == 'User':
            is_deleted = [x for x in new_class._meta.local_fields if x.name == 'is_deleted'][0]
            new_class._meta.local_fields.remove(is_deleted)

        new_class._meta.managed = False
        return new_class


class HerokuConnectModel(models.Model, metaclass=HerokuConnectModelBase):
    """
    Base model for Heroku Connect enabled ORM models in Django.

    Example::

        from heroku_connect.db import models as hc_models


        class MyCustomObject(hc_models.HerokuConnectModel):
            sf_object_name = 'My_Custom_Object__c'

            custom_date = hc_models.DateTime(sf_field_name='Custom_Date__c')

    Note:

        Subclasses have :attr:`Meta.managed<django.db.models.Options.managed>` set to ``False``.

        A default value for :attr:`Meta.db_table<django.db.models.Options.db_table>` is set based
        on :attr:`settings.HEROKU_CONNECT_SCHEMA<.HerokuConnectAppConf.HEROKU_CONNECT_SCHEMA>`
        and :attr:`.sf_object_name`.

    Warning:

        The Salesforce object `User`_ object has no ``IsDeleted`` field. Therefore
        if :attr:`.sf_object_name` is set to ``User`` the Django ORM representation
        does not have this field either. You can add the ``IsActive`` field to your
        user object, but it is not required by Heroku Connect.

    .. _User:
        https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_user.htm

    """

    sf_object_name = ''
    """Salesforce object API name."""

    sf_access = 'read_only'
    """
    Heroku Connect Object access level.

    Access to Heroku Connect tables can be either read or write.
    Read will only sync from Salesforce to PostgreSQL where
    write will sync both ways.

    Default value is ``read_only``.

    Accepted values:
        * ``read_only``
            Synchronize only from Salesforce to PostgreSQL.
        * ``read_write``
            Synchronize both ways between Salesforce and PostgreSQL.

    """

    sf_notify_enabled = True
    sf_polling_seconds = 120
    sf_max_daily_api_calls = 30000

    sf_id = fields.ID(sf_field_name='ID', db_column='sfid')
    system_mod_stamp = fields.DateTime(sf_field_name='SystemModstamp', db_index=True)
    is_deleted = fields.Checkbox(sf_field_name='IsDeleted')
    _hc_lastop = models.CharField(
        max_length=32, editable=False,
        help_text='Indicates the last sync operation Heroku Connect performed on the record',
    )
    _hc_err = models.TextField(
        max_length=1024, editable=False,
        help_text='If the last sync operation by Heroku Connect resulted in an error then this'
                  ' column will contain a JSON object containing more'
                  ' information about the error',
    )

    class Meta:
        abstract = True

    @classmethod
    def get_heroku_connect_fields(cls):
        return [
            field for field in cls._meta.fields
            if isinstance(field, fields.HerokuConnectFieldMixin)
        ]

    @classmethod
    def get_heroku_connect_field_mapping(cls):
        sf_fields = list(cls.get_heroku_connect_fields())

        sf_field_names = {
            field.sf_field_name: {}  # dict for possible future options
            for field in sf_fields
        }

        indexes = {
            field.sf_field_name: {
                'unique': field.unique,
            }
            for field in sf_fields
            if field.db_index
        }

        upsert_field = None

        for field in sf_fields:
            if field.upsert:
                upsert_field = field.sf_field_name

        return sf_field_names, indexes, upsert_field

    @classmethod
    def get_heroku_connect_mapping(cls):
        fields, indexes, upsert_field = cls.get_heroku_connect_field_mapping()
        config = {
            "access": cls.sf_access,
            "sf_notify_enabled": cls.sf_notify_enabled,
            "sf_polling_seconds": cls.sf_polling_seconds,
            "sf_max_daily_api_calls": cls.sf_max_daily_api_calls,
            "fields": fields,
            "indexes": indexes,
        }

        if upsert_field is not None:
            config["upsert_field"] = upsert_field
        return {
            "object_name": cls.sf_object_name,
            "config": config
        }

    @classmethod
    def _check_sf_object_name(cls):
        if not cls.sf_object_name:
            return [checks.Error(
                "%s.%s must define a \"sf_object_name\"." % (
                    cls._meta.app_label, cls.__name__
                ),
                id='heroku_connect.E001',
            )]
        return []

    @classmethod
    def _check_sf_access(cls):
        allowed_access_types = ['read_only', 'read_write']
        if cls.sf_access not in allowed_access_types:
            return [checks.Error(
                "%s.%s.sf_access must be one of %s" % (
                    cls._meta.app_label, cls.__name__, allowed_access_types
                ),
                hint=cls.sf_access,
                id='heroku_connect.E002',
            )]
        return []

    @classmethod
    def _check_unique_sf_field_names(cls):
        sf_field_names = [field.sf_field_name for field in cls.get_heroku_connect_fields()]
        duplicates = [x for n, x in enumerate(sf_field_names) if x in sf_field_names[:n]]
        if duplicates:
            return [checks.Error(
                "%s.%s has duplicate Salesforce field names." % (
                    cls._meta.app_label, cls.__name__
                ),
                hint=duplicates,
                id='heroku_connect.E003',
            )]
        return []

    @classmethod
    def _check_upsert_field(cls):
        upsert_fields = [field for field in cls.get_heroku_connect_fields() if field.upsert]
        if len(upsert_fields) > 1:
            return [checks.Error(
                "%s.%s can only have a single upsert field." % (
                    cls._meta.app_label, cls.__name__
                ),
                hint=upsert_fields,
                id='heroku_connect.E004',
            )]
        return []

    @classmethod
    def check(cls, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(cls._check_sf_object_name())
        errors.extend(cls._check_sf_access())
        errors.extend(cls._check_unique_sf_field_names())
        errors.extend(cls._check_upsert_field())
        return errors
