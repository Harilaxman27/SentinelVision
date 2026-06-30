"""
Module: security.plugin_validator

Purpose:
Validate third-party plugins before they are loaded.

Responsibilities:
- Inspect plugin source code for forbidden imports (e.g. `os`, `subprocess`).
- Validate manifest structure.

Dependencies:
- ast, backend.plugins.base

Owner:
SentinelVision
"""

import ast
from pathlib import Path


class PluginSecurityValidator:
    """Static analysis validator for plugin code."""
    
    # Modules that plugins are generally not allowed to import directly
    # to prevent arbitrary command execution or filesystem access outside their scope.
    FORBIDDEN_MODULES = {
        "os", "sys", "subprocess", "pty", "socket", 
        "urllib", "requests", "http", "ftplib"
    }

    @classmethod
    def validate_file(cls, path: Path) -> list[str]:
        """Perform static analysis on a plugin file.
        
        Args:
            path: Path to the python source file.
            
        Returns:
            A list of security violation messages. Empty list means valid.
        """
        violations = []
        try:
            with open(path, "r", encoding="utf-8") as f:
                source = f.read()
            tree = ast.parse(source, filename=str(path))
        except Exception as e:
            return [f"Failed to parse AST for {path.name}: {e}"]

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root_module = alias.name.split('.')[0]
                    if root_module in cls.FORBIDDEN_MODULES:
                        violations.append(
                            f"Forbidden import '{alias.name}' at line {node.lineno}"
                        )
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    root_module = node.module.split('.')[0]
                    if root_module in cls.FORBIDDEN_MODULES:
                        violations.append(
                            f"Forbidden from-import '{node.module}' at line {node.lineno}"
                        )
                        
        return violations
