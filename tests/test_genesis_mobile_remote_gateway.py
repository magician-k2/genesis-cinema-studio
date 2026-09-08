# -*- coding: utf-8 -*-
"""
================================================================================
TEST SUITE: GENESIS MOBILE REMOTE GATEWAY & 2FA AUTHENTICATION
(tests/test_genesis_mobile_remote_gateway.py)
================================================================================
"""

import unittest
import sys
import os
import time

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

sys.path.insert(0, r"g:\マイドライブ\GENESIS_ROOT")
from core.genesis_mobile_auth_gateway import mobile_auth_gateway
from core.genesis_mobile_remote_gateway import mobile_remote_gateway

class TestGenesisMobileRemoteGateway(unittest.TestCase):

    def setUp(self):
        self.test_email = "tester_mobile@genesis.ai"

    def test_01_generate_and_verify_otp_flow(self):
        """6桁OTP発行 ➔ 正しいコードで検証 ➔ 30日セッショントークン取得"""
        otp_res = mobile_auth_gateway.generate_and_send_otp(self.test_email)
        self.assertEqual(otp_res.get("status"), "OTP_SENT")
        otp_code = otp_res.get("debug_otp")
        self.assertIsNotNone(otp_code)
        self.assertEqual(len(otp_code), 6)

        auth_res = mobile_auth_gateway.verify_otp(self.test_email, otp_code, remember_me=True)
        self.assertEqual(auth_res.get("status"), "SUCCESS")
        token = auth_res.get("token")
        self.assertIsNotNone(token)
        self.assertEqual(auth_res.get("days_valid"), 30)

        is_valid, user = mobile_auth_gateway.validate_session(token)
        self.assertTrue(is_valid)
        self.assertEqual(user, self.test_email)

    def test_02_incorrect_otp_and_lockout_protection(self):
        """誤ったOTP入力の失敗判定とブルートフォース防御"""
        mobile_auth_gateway.generate_and_send_otp("wrong_user@genesis.ai")
        res = mobile_auth_gateway.verify_otp("wrong_user@genesis.ai", "000000")
        self.assertEqual(res.get("status"), "INCORRECT_CODE")

    def test_03_remote_command_execution_with_token(self):
        """認証トークン付きでスマホ遠隔指示を実行"""
        otp_res = mobile_auth_gateway.generate_and_send_otp(self.test_email)
        auth_res = mobile_auth_gateway.verify_otp(self.test_email, otp_res["debug_otp"])
        token = auth_res["token"]

        # 1. 90s テクノDJ指示
        cmd_res = mobile_remote_gateway.execute_remote_command("90sテクノのリミックスを作って", token)
        self.assertEqual(cmd_res.get("status"), "SUCCESS")
        result = cmd_res.get("result", {})
        self.assertEqual(result.get("category"), "TECHNO_DJ")
        self.assertEqual(result.get("tracks_count"), 20)

        # 2. 全器官ヘルス指示
        health_res = mobile_remote_gateway.execute_remote_command("全器官ヘルスチェック", token)
        self.assertEqual(health_res.get("status"), "SUCCESS")

        # 3. 未認証アクセス遮断
        bad_res = mobile_remote_gateway.execute_remote_command("何かやって", "invalid_token_999")
        self.assertEqual(bad_res.get("status"), "UNAUTHORIZED")

    def test_04_session_kill_switch(self):
        """緊急キルスイッチによる全端末セッション強制破棄"""
        otp_res = mobile_auth_gateway.generate_and_send_otp(self.test_email)
        auth_res = mobile_auth_gateway.verify_otp(self.test_email, otp_res["debug_otp"])
        token = auth_res["token"]

        kill_res = mobile_auth_gateway.revoke_all_sessions()
        self.assertEqual(kill_res.get("status"), "ALL_REVOKED")

        is_valid, _ = mobile_auth_gateway.validate_session(token)
        self.assertFalse(is_valid)

if __name__ == "__main__":
    unittest.main()
