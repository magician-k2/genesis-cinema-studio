"""
Unit tests for Copyright Compliance & Proof-of-Purchase Verification Engine (12 Tests)
"""

import unittest
from core.copyright_compliance_proof_engine import (
    CopyrightComplianceProofEngine,
    OfficialAppPurchaseVerification,
    DeviceBoundEncryption
)

class TestCopyrightComplianceProofEngine(unittest.TestCase):
    def setUp(self):
        self.engine = CopyrightComplianceProofEngine()
        self.verifier = OfficialAppPurchaseVerification()
        self.binder = DeviceBoundEncryption()

    def test_01_validate_and_secure_ebook_app_generation(self):
        res = self.engine.validate_and_secure_ebook_app_generation("中学英語ひとつひとつ", "app_123")
        self.assertEqual(res["status"], "COPYRIGHT_COMPLIANCE_VERIFIED_OPTIMAL")
        self.assertTrue(res["private_use_compliant"])

    def test_02_official_app_purchase_verification(self):
        res = self.verifier.verify_purchase_proof("test_book")
        self.assertEqual(res["status"], "PURCHASE_VERIFICATION_SUCCESS")
        self.assertTrue(res["verified_legitimate_owner"])

    def test_03_device_hwid_key_generation(self):
        hwid = self.binder.generate_device_hwid_key()
        self.assertEqual(len(hwid), 32)

    def test_04_device_bound_app_encryption(self):
        res = self.binder.bind_app_to_device("app_test_456")
        self.assertEqual(res["status"], "DEVICE_BOUND_ENCRYPTION_SUCCESS")
        self.assertTrue(res["redistribution_blocked"])

    def test_05_purchase_token_presence(self):
        res = self.verifier.verify_purchase_proof("kindle_book_789")
        self.assertTrue(res["purchase_license_token"].startswith("LIC_"))

    def test_06_compliance_audit_logging(self):
        self.engine.validate_and_secure_ebook_app_generation("Book A", "app_A")
        self.assertEqual(len(self.engine.compliance_audit_log), 1)

    def test_07_article_30_compliance_status(self):
        self.engine.validate_and_secure_ebook_app_generation("Book B", "app_B")
        audit = self.engine.compliance_audit_log[0]
        self.assertEqual(audit["compliance_status"], "COPYRIGHT_LAW_ARTICLE_30_PRIVATE_USE_COMPLIANT")

    def test_08_redistribution_prevented_flag(self):
        res = self.engine.validate_and_secure_ebook_app_generation("Book C", "app_C")
        self.assertTrue(res["redistribution_prevented"])

    def test_09_purchase_verified_flag(self):
        res = self.engine.validate_and_secure_ebook_app_generation("Book D", "app_D")
        self.assertTrue(res["purchase_verified"])

    def test_10_device_bound_encrypted_flag(self):
        res = self.engine.validate_and_secure_ebook_app_generation("Book E", "app_E")
        self.assertTrue(res["device_bound_encrypted"])

    def test_11_audit_id_format(self):
        self.engine.validate_and_secure_ebook_app_generation("Book F", "app_F")
        audit = self.engine.compliance_audit_log[0]
        self.assertTrue(audit["audit_id"].startswith("audit_"))

    def test_12_payload_signature_generation(self):
        res = self.binder.bind_app_to_device("app_sig_test")
        self.assertEqual(len(res["payload_signature"]), 24)

if __name__ == "__main__":
    unittest.main()
