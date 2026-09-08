"""
================================================================================
TEST SUITE: GENESIS EBOOK TO APP & CROSS-BOOK SYNTHESIS PLATFORM
Tests core/genesis_ebook_cross_synthesis_app_platform.py
================================================================================
"""

import os
import sys
import unittest

sys.path.insert(0, r"g:\マイドライブ\GENESIS_ROOT")
from core.genesis_ebook_cross_synthesis_app_platform import ebook_cross_platform

class TestGenesisEbookCrossSynthesis(unittest.TestCase):

    def test_01_ingested_books_library_with_qr_and_errata(self):
        books = ebook_cross_platform.list_ingested_books()
        self.assertTrue(len(books) >= 6)
        # Verify QR codes and Errata flags
        for b in books:
            self.assertTrue(b["qr_code_detected"].startswith("http"))
            self.assertTrue(b["errata_overridden"])
            self.assertTrue(b["audio_files_count"] > 0)
        print(f"📚 Verified Ingested Books with QR Audio & Errata: {len(books)} titles")

    def test_02_generate_custom_learning_app_combined_mode(self):
        res = ebook_cross_platform.generate_custom_learning_app(
            mode="BOTH",
            learner_weakness="単語力はあるが会話表現力と発音がとぼしい"
        )
        self.assertEqual(res["status"], "EBOOK_APP_SYNTHESIZED_SUCCESS")
        self.assertEqual(res["mode"], "BOTH")
        self.assertTrue(res["total_qr_audio_tracks"] >= 300)
        self.assertTrue(os.path.exists(res["app_package_path"]))
        print(f"📱 Custom App Synthesized: {res['app_id']} | QR Audio Tracks: {res['total_qr_audio_tracks']} | Latency: {res['latency_ms']}ms")

    def test_03_zero_hallucination_quiz_from_book(self):
        res = ebook_cross_platform.generate_zero_hallucination_quiz("book_jh_grammar", "現在完了の継続用法")
        self.assertEqual(res["status"], "ZERO_HALLUCINATION_QUIZ_READY")
        self.assertIn("quiz", res)
        self.assertIn("source_page_quote", res["quiz"])
        print(f"🔒 Zero-Hallucination Quiz from '{res['book_title']}':\n{res['quiz']['question']}\nCitation: {res['quiz']['source_page_quote']}")

    def test_04_dual_ai_alt_interaction(self):
        res = ebook_cross_platform.simulate_dual_ai_alt_interaction("I'd like to order a coffee, but I forgot how to ask for soy milk.")
        self.assertEqual(res["status"], "DUAL_AI_ALT_SUCCESS")
        self.assertIsNotNone(res["native_response"])
        self.assertIsNotNone(res["support_alt_whisper"])
        print(f"🗣️ Native ALT: {res['native_response']}\n💡 Support ALT Whisper: {res['support_alt_whisper']}")

if __name__ == "__main__":
    unittest.main()
