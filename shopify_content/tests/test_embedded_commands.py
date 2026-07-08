"""Tests for embedded management command registry, dispatch, and Celery task."""

from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

from shopify_content.embedded_commands.dispatch import enqueue_embedded_command
from shopify_content.embedded_commands.registry import (
    ALL_MANAGEMENT_COMMAND_NAMES,
    EMBEDDED_COMMANDS,
    IMPORT_COMMAND_NAMES,
    get_command_by_id,
)
from shopify_content.models.command_run import EmbeddedCommandRun
from shopify_content.tasks import run_embedded_command_task


class EmbeddedCommandRegistryTests(TestCase):
    def test_registry_covers_all_management_commands(self):
        registry_command_names = {spec.command for spec in EMBEDDED_COMMANDS}
        self.assertEqual(
            registry_command_names | IMPORT_COMMAND_NAMES,
            ALL_MANAGEMENT_COMMAND_NAMES,
        )
        self.assertEqual(len(ALL_MANAGEMENT_COMMAND_NAMES), 22)

    def test_registry_has_bootstrap_apply_variant(self):
        default = get_command_by_id('bootstrap_index_pages')
        apply_variant = get_command_by_id('bootstrap_index_pages_apply')
        self.assertIsNotNone(default)
        self.assertIsNotNone(apply_variant)
        self.assertEqual(default.command, apply_variant.command)
        self.assertEqual(apply_variant.kwargs, {'apply_export_config': True})

    def test_unknown_command_id_returns_none(self):
        self.assertIsNone(get_command_by_id('does-not-exist'))


class EmbeddedCommandDispatchTests(TestCase):
    @patch('shopify_content.tasks.run_embedded_command_task')
    def test_enqueue_creates_run_and_dispatches_celery(self, mock_task):
        mock_task.delay.return_value.id = 'celery-abc'

        run = enqueue_embedded_command('setup_locales')

        self.assertEqual(run.command_id, 'setup_locales')
        self.assertEqual(run.command_name, 'setup_locales')
        self.assertEqual(run.celery_task_id, 'celery-abc')
        self.assertEqual(run.status, EmbeddedCommandRun.STATUS_PENDING)
        mock_task.delay.assert_called_once_with(run.pk)

    def test_enqueue_rejects_unknown_command(self):
        with self.assertRaises(ValueError):
            enqueue_embedded_command('invalid-command')


class RunEmbeddedCommandTaskTests(TestCase):
    def test_task_marks_success_and_persists_stdout(self):
        run = EmbeddedCommandRun.objects.create(
            command_id='setup_locales',
            command_name='setup_locales',
            kwargs={},
            message='queued',
        )

        run_embedded_command_task(run.pk)

        run.refresh_from_db()
        self.assertEqual(run.status, EmbeddedCommandRun.STATUS_SUCCESS)
        self.assertIn('Locale setup complete', run.stdout)
        self.assertTrue(run.message)

    @patch('django.core.management.call_command')
    def test_task_marks_failed_on_exception(self, mock_call_command):
        mock_call_command.side_effect = RuntimeError('boom')
        run = EmbeddedCommandRun.objects.create(
            command_id='setup_locales',
            command_name='setup_locales',
            kwargs={},
            message='queued',
        )

        with self.assertRaises(RuntimeError):
            run_embedded_command_task(run.pk)

        run.refresh_from_db()
        self.assertEqual(run.status, EmbeddedCommandRun.STATUS_FAILED)
        self.assertIn('boom', run.message)
        self.assertIn('RuntimeError', run.error_detail)

    def test_setup_locales_command_runs_via_call_command(self):
        out = StringIO()
        call_command('setup_locales', stdout=out)
        self.assertIn('Locale setup complete', out.getvalue())
