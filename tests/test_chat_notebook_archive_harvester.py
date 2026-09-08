"""
Unit tests for Chat Log & NotebookLM Past Memory Auto-Archiver (12 Tests)
"""

import os
import unittest
from core.chat_notebook_archive_harvester import ChatNotebookArchiveHarvester

class TestChatNotebookArchiveHarvester(unittest.TestCase):
    def setUp(self):
        self.harvester = ChatNotebookArchiveHarvester()

    def test_01_harvest_chat_and_notebook_archives(self):
        res = self.harvester.harvest_chat_and_notebook_archives()
        self.assertEqual(res["status"], "CHAT_NOTEBOOK_HARVESTING_OPTIMAL")
        self.assertGreater(res["total_conversations_indexed"], 0)

    def test_02_antigravity_transcripts_count(self):
        res = self.harvester.harvest_chat_and_notebook_archives()
        self.assertGreaterEqual(res["antigravity_transcripts"], 0)

    def test_03_notebooklm_exports_count(self):
        res = self.harvester.harvest_chat_and_notebook_archives()
        self.assertEqual(res["notebooklm_exports"], 8)

    def test_04_pdf_chat_logs_count(self):
        res = self.harvester.harvest_chat_and_notebook_archives()
        self.assertEqual(res["pdf_chat_logs"], 5)

    def test_05_archive_destination_folder(self):
        res = self.harvester.harvest_chat_and_notebook_archives()
        self.assertIn("chat_notebook_archives", res["destination"])

    def test_06_harvest_log_recording(self):
        self.harvester.harvest_chat_and_notebook_archives()
        self.assertEqual(len(self.harvester.harvested_archives_log), 1)

    def test_07_gemma4_lineage_tag_in_archive_log(self):
        self.harvester.harvest_chat_and_notebook_archives()
        log_entry = self.harvester.harvested_archives_log[0]
        self.assertEqual(log_entry["gemma4_lineage_tag"], "CHAT_NOTEBOOKLM_MEMORY_ARCHIVED")

    def test_08_status_chat_notebook_archived_success(self):
        self.harvester.harvest_chat_and_notebook_archives()
        log_entry = self.harvester.harvested_archives_log[0]
        self.assertEqual(log_entry["status"], "CHAT_NOTEBOOK_ARCHIVED_SUCCESS")

    def test_09_archive_id_format(self):
        self.harvester.harvest_chat_and_notebook_archives()
        log_entry = self.harvester.harvested_archives_log[0]
        self.assertTrue(log_entry["archive_id"].startswith("arch_chat_"))

    def test_10_multiple_archival_runs(self):
        self.harvester.harvest_chat_and_notebook_archives()
        self.harvester.harvest_chat_and_notebook_archives()
        self.assertEqual(len(self.harvester.harvested_archives_log), 2)

    def test_11_total_conversations_sum(self):
        res = self.harvester.harvest_chat_and_notebook_archives()
        expected = res["antigravity_transcripts"] + res["notebooklm_exports"] + res["pdf_chat_logs"]
        self.assertEqual(res["total_conversations_indexed"], expected)

    def test_12_cloud_destination_exists(self):
        res = self.harvester.harvest_chat_and_notebook_archives()
        self.assertTrue(os.path.exists(res["destination"]))

if __name__ == "__main__":
    unittest.main()
