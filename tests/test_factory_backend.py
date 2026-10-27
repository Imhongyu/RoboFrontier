"""The legacy replay tools retain verification but cannot emit Classic factory video."""
import unittest

from scripts.replay_motion_in_factory import replay
from scripts.replay_dial_motion import replay as replay_dial
from scripts.export_relay_edited import render_all, render_case


class FactoryBackendTests(unittest.TestCase):
    def test_legacy_factory_video_requests_are_rejected_before_reading_inputs(self):
        with self.assertRaisesRegex(ValueError, 'Cycles'):
            replay('missing', 'missing', 'missing', render=True)
        with self.assertRaisesRegex(ValueError, 'Cycles'):
            replay_dial('missing', 'missing', 'missing', render=True)
        with self.assertRaisesRegex(ValueError, 'Cycles'):
            render_all('missing', 'missing', 'missing', 'classic')
        with self.assertRaisesRegex(ValueError, 'Cycles'):
            render_case('missing', 'missing', factory_renderer=object())
