"""
Unit tests for Zero-Hallucination Comprehension Exam & Memory Wall-Bounce Engine (12 Tests)
"""

import os
import unittest
from core.zero_hallucination_comprehension_engine import ZeroHallucinationComprehensionEngine

class TestZeroHallucinationComprehensionEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ZeroHallucinationComprehensionEngine()

    def test_01_generate_zero_hallucination_exam(self):
        res = self.engine.generate_zero_hallucination_exam("機械翻訳実践（情報/法学）")
        self.assertEqual(res["status"], "ZERO_HALLUCINATION_EXAM_OPTIMAL")
        self.assertEqual(res["hallucination_rate"], "0.00000%")

    def test_02_question_types_generated(self):
        res = self.engine.generate_zero_hallucination_exam("テスト書籍")
        self.assertEqual(res["total_questions"], 3)

    def test_03_exam_sessions_history_logging(self):
        self.engine.generate_zero_hallucination_exam("Book A")
        self.assertEqual(len(self.engine.exam_sessions_history), 1)

    def test_04_grade_essay_answer_zero_hallucination(self):
        res = self.engine.grade_essay_answer_zero_hallucination("q3_essay", "この講義の結論について法的な観点から詳細に要約します。", "法学論文要旨")
        self.assertEqual(res["status"], "ESSAY_GRADING_SUCCESS")
        self.assertTrue(res["hallucination_free_verification"])

    def test_05_essay_scoring_threshold(self):
        res_short = self.engine.grade_essay_answer_zero_hallucination("q3_essay", "短すぎる回答", "法学論文要旨")
        self.assertEqual(res_short["score"], 70.0)

    def test_06_execute_genesis_memory_wall_bounce_training(self):
        res = self.engine.execute_genesis_memory_wall_bounce_training()
        self.assertEqual(res["status"], "GENESIS_WALL_BOUNCE_TRAINING_OPTIMAL")
        self.assertTrue(res["hallucination_elimination_verified"])

    def test_07_cortex_nodes_tested_count(self):
        res = self.engine.execute_genesis_memory_wall_bounce_training()
        self.assertEqual(res["cortex_nodes_tested"], 10787)

    def test_08_wall_bounce_precision_growth(self):
        score_before = self.engine.genesis_memory_accuracy_score
        self.engine.execute_genesis_memory_wall_bounce_training()
        self.assertGreater(self.engine.genesis_memory_accuracy_score, score_before)

    def test_09_exam_id_format(self):
        res = self.engine.generate_zero_hallucination_exam("Sample Book")
        self.assertTrue(res["exam_id"].startswith("exam_"))

    def test_10_zero_hallucination_guaranteed_flag(self):
        self.engine.generate_zero_hallucination_exam("Sample Book")
        pkg = self.engine.exam_sessions_history[0]
        self.assertTrue(pkg["zero_hallucination_guaranteed"])

    def test_11_source_text_citation_presence(self):
        self.engine.generate_zero_hallucination_exam("Sample Book")
        q = self.engine.exam_sessions_history[0]["questions"][0]
        self.assertIn("source_text_citation", q)

    def test_12_critique_presence_in_essay_grading(self):
        res = self.engine.grade_essay_answer_zero_hallucination("q3_essay", "長い記述式回答文例で添削評価をテストします。", "参照本文")
        self.assertIn("critique", res)

    def test_13_save_exam_result_record(self):
        res = self.engine.save_exam_result_record(
            course_or_book_title="テスト講義",
            question_text="問題文",
            student_answer="受講者解答",
            model_answer="模範解答",
            score=90.0,
            feedback="添削フィードバック"
        )
        self.assertEqual(res["status"], "EXAM_RESULT_SAVED_SUCCESS")
        self.assertTrue(os.path.exists(res["json_path"]))
        self.assertTrue(os.path.exists(res["markdown_path"]))

if __name__ == "__main__":
    unittest.main()
