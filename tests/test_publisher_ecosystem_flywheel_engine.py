"""
Unit tests for Publisher Ecosystem Flywheel & Antigravity Brain Augmentation Engine (12 Tests)
"""

import unittest
from core.publisher_ecosystem_flywheel_engine import PublisherEcosystemFlywheelEngine

class TestPublisherEcosystemFlywheelEngine(unittest.TestCase):
    def setUp(self):
        self.engine = PublisherEcosystemFlywheelEngine()

    def test_01_register_purchased_book_augmentation(self):
        res = self.engine.register_purchased_book_augmentation("Python Deep Dive", "John Doe")
        self.assertEqual(res["status"], "ECOSYSTEM_FLYWHEEL_OPTIMAL")
        self.assertTrue(res["win_win_publisher_model_active"])

    def test_02_antigravity_capacity_multiplier_increase(self):
        self.engine.register_purchased_book_augmentation("Book 1", "Author 1")
        self.assertGreater(self.engine.antigravity_capacity_multiplier, 1.0)

    def test_03_ingested_specialized_books_registry(self):
        self.engine.register_purchased_book_augmentation("Book A", "Author A")
        self.assertEqual(len(self.engine.ingested_specialized_books), 1)

    def test_04_author_royalty_protection_flag(self):
        self.engine.register_purchased_book_augmentation("Book B", "Author B")
        rec = self.engine.ingested_specialized_books[0]
        self.assertTrue(rec["author_royalty_protected"])

    def test_05_official_purchase_verification_flag(self):
        self.engine.register_purchased_book_augmentation("Book C", "Author C")
        rec = self.engine.ingested_specialized_books[0]
        self.assertTrue(rec["official_purchase_verified"])

    def test_06_multiple_book_capacity_stacking(self):
        self.engine.register_purchased_book_augmentation("Book 1", "A1")
        self.engine.register_purchased_book_augmentation("Book 2", "A2")
        self.assertAlmostEqual(self.engine.antigravity_capacity_multiplier, 1.30, places=2)

    def test_07_book_id_format(self):
        self.engine.register_purchased_book_augmentation("Book X", "AX")
        rec = self.engine.ingested_specialized_books[0]
        self.assertTrue(rec["book_id"].startswith("flywheel_"))

    def test_08_domain_category_support(self):
        res = self.engine.register_purchased_book_augmentation("Quantum Physics", "Physicist", "QUANTUM_PHYSICS")
        self.assertEqual(res["status"], "ECOSYSTEM_FLYWHEEL_OPTIMAL")

    def test_09_capacity_boost_display(self):
        self.engine.register_purchased_book_augmentation("Book Y", "AY")
        rec = self.engine.ingested_specialized_books[0]
        self.assertEqual(rec["antigravity_capacity_boost"], "+15%")

    def test_10_status_flywheel_augmentation_success(self):
        self.engine.register_purchased_book_augmentation("Book Z", "AZ")
        rec = self.engine.ingested_specialized_books[0]
        self.assertEqual(rec["status"], "FLYWHEEL_AUGMENTATION_SUCCESS")

    def test_11_current_capacity_multiplier_round(self):
        res = self.engine.register_purchased_book_augmentation("Book 10", "A10")
        self.assertEqual(res["current_capacity_multiplier"], 1.15)

    def test_12_registry_length_growth(self):
        self.engine.register_purchased_book_augmentation("Book 1", "A1")
        self.engine.register_purchased_book_augmentation("Book 2", "A2")
        self.assertEqual(len(self.engine.ingested_specialized_books), 2)

if __name__ == "__main__":
    unittest.main()
