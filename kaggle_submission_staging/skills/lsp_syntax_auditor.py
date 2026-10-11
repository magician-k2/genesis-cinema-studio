# -*- coding: utf-8 -*-
"""
GENESIS LSP Syntax Auditor Skill
Verifies Python Abstract Syntax Tree (AST) validity offline.
Guarantees zero SyntaxError and correct indentation before submission.
"""

import ast
from typing import Dict, Any

def audit_code_syntax(code_string: str) -> Dict[str, Any]:
    """
    Parses code using Python standard AST.
    Returns syntax validity and precise error diagnostics if invalid.
    """
    try:
        parsed_tree = ast.parse(code_string)
        return {
            "valid": True,
            "error": None,
            "ast_node_count": len(list(ast.walk(parsed_tree)))
        }
    except SyntaxError as e:
        return {
            "valid": False,
            "error": f"SyntaxError at line {e.lineno}, col {e.offset}: {e.msg}",
            "lineno": e.lineno,
            "offset": e.offset,
            "bad_line": e.text.strip() if e.text else ""
        }
    except Exception as e:
        return {
            "valid": False,
            "error": f"Parse failure: {str(e)}"
        }
