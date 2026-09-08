# -*- coding: utf-8 -*-
"""
Tests for Gemini Code Assist Autonomous Quality Pipeline
"""

import unittest
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from core.gemini_code_assist_pipeline import GeminiCodeAssistPipeline, GCPMockFactory

class TestGeminiCodeAssistPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = GeminiCodeAssistPipeline()

    def test_gcp_mock_generation(self):
        firestore_mock = GCPMockFactory.generate_firestore_mock()
        self.assertIn("MockFirestoreClient", firestore_mock)
        pubsub_mock = GCPMockFactory.generate_pubsub_mock()
        self.assertIn("MockPubSubPublisher", pubsub_mock)
        storage_mock = GCPMockFactory.generate_storage_mock()
        self.assertIn("MockStorageClient", storage_mock)

    def test_inspect_python_code(self):
        sample_code = """
import os
from google.cloud import firestore

class VideoProcessor:
    def process_frames(self, frames):
        pass
    def render_output(self):
        pass
"""
        res = self.pipeline.inspect_python_code(sample_code)
        self.assertTrue(res["valid_syntax"])
        self.assertEqual(res["classes"], ["VideoProcessor"])
        self.assertIn("process_frames", res["functions"])
        self.assertIn("render_output", res["functions"])
        self.assertTrue(any("firestore" in dep for dep in res["gcp_dependencies"]))

    def test_generate_unit_tests(self):
        sample_code = """
class AudioMixer:
    def adjust_gain(self, volume):
        return volume * 1.5
"""
        test_code = self.pipeline.generate_unit_tests("audio_mixer", sample_code)
        self.assertIn("TestAudio_mixerGeneratedSuite", test_code)
        self.assertIn("MockFirestoreClient", test_code)
        self.assertIn("test_adjust_gain_execution_boundary", test_code)

if __name__ == "__main__":
    unittest.main()
