from __future__ import absolute_import, division, print_function, unicode_literals

from django import dispatch
from django.db import transaction
from django.db.models import signals as model_signals

from . import client

# Setup model notifications.
observer_client = client.QueryObserverClient()


@dispatch.receiver(model_signals.post_save)
def model_post_save(sender, instance, created=False, **kwargs):
    """
    Signal emitted after any model is saved via Django ORM.

    :param sender: Model class that was saved
    :param instance: The actual instance that was saved
    :param created: True if a new row was created
    """

    def notify():
        table = sender._meta.db_table
        if created:
            observer_client.notify_table_insert(table)
        else:
            observer_client.notify_table_update(table)

    transaction.on_commit(notify)


@dispatch.receiver(model_signals.post_delete)
def model_post_delete(sender, instance, **kwargs):
    """
    Signal emitted after any model is deleted via Django ORM.

    :param sender: Model class that was deleted
    :param instance: The actual instance that was removed
    """

    def notify():
        table = sender._meta.db_table
        observer_client.notify_table_remove(table)

    transaction.on_commit(notify)


@dispatch.receiver(model_signals.m2m_changed)
def model_m2m_changed(sender, instance, action, **kwargs):
    """
    Signal emitted after any M2M relation changes via Django ORM.

    :param sender: M2M intermediate model
    :param instance: The actual instance that was saved
    :param action: M2M action
    """

    def notify():
        table = sender._meta.db_table
        if action == 'post_add':
            observer_client.notify_table_insert(table)
        elif action in ('post_remove', 'post_clear'):
            observer_client.notify_table_remove(table)

    transaction.on_commit(notify)
