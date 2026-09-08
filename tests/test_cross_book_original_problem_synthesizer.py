"""
Unit tests for Cross-Book Original Problem & Curriculum Synthesizer Engine (12 Tests)
"""

import unittest
from core.cross_book_original_problem_synthesizer import CrossBookOriginalProblemSynthesizer

class TestCrossBookOriginalProblemSynthesizer(unittest.TestCase):
    def setUp(self):
        self.synthesizer = CrossBookOriginalProblemSynthesizer()

    def test_01_generate_original_problem_set(self):
        res = self.synthesizer.generate_original_problem_set()
        self.assertEqual(res["status"], "CROSS_BOOK_SYNTHESIS_OPTIMAL")
        self.assertEqual(res["total_original_problems_generated"], 5)

    def test_02_ingested_books_registry(self):
        self.assertGreaterEqual(len(self.synthesizer.ingested_books_registry), 5)
        self.assertIn("100日後に英語がものになる1日10分 ネイティブ英語書き写し", self.synthesizer.ingested_books_registry)

    def test_03_original_grammar_problems_generated(self):
        self.synthesizer.generate_original_problem_set()
        pkg = self.synthesizer.generated_problems_history[0]
        self.assertEqual(len(pkg["original_grammar_problems"]), 1)
        self.assertEqual(pkg["original_grammar_problems"][0]["type"], "Grammar & Reading")

    def test_04_original_conversation_scenarios_generated(self):
        self.synthesizer.generate_original_problem_set()
        pkg = self.synthesizer.generated_problems_history[0]
        self.assertEqual(len(pkg["original_conversation_scenarios"]), 1)

    def test_05_original_vocab_flashcards_generated(self):
        self.synthesizer.generate_original_problem_set()
        pkg = self.synthesizer.generated_problems_history[0]
        self.assertEqual(len(pkg["original_vocab_flashcards"]), 1)

    def test_06_original_phonetics_drills_generated(self):
        self.synthesizer.generate_original_problem_set()
        pkg = self.synthesizer.generated_problems_history[0]
        self.assertEqual(len(pkg["original_phonetics_drills"]), 1)

    def test_07_original_handwriting_sheets_generated(self):
        self.synthesizer.generate_original_problem_set()
        pkg = self.synthesizer.generated_problems_history[0]
        self.assertEqual(len(pkg["original_handwriting_sheets"]), 1)
        self.assertEqual(pkg["original_handwriting_sheets"][0]["day_number"], 42)

    def test_08_handwriting_dictation_ready_flag(self):
        res = self.synthesizer.generate_original_problem_set()
        self.assertTrue(res["handwriting_dictation_ready"])

    def test_09_adaptive_matrix_applied_flag(self):
        self.synthesizer.generate_original_problem_set()
        pkg = self.synthesizer.generated_problems_history[0]
        self.assertTrue(pkg["adaptive_matrix_applied"])

    def test_10_problem_set_id_format(self):
        res = self.synthesizer.generate_original_problem_set()
        self.assertTrue(res["problem_set_id"].startswith("probset_"))

    def test_11_fused_books_count_match(self):
        res = self.synthesizer.generate_original_problem_set()
        self.assertEqual(res["fused_books_count"], len(self.synthesizer.ingested_books_registry))

    def test_12_history_logging(self):
        self.synthesizer.generate_original_problem_set()
        self.assertEqual(len(self.synthesizer.generated_problems_history), 1)

if __name__ == "__main__":
    unittest.main()
