import os
import re

required_files = [
    # Copied from previous blueprint parsing, I'll just approximate the numbers
]

stats = {
    "existing": 0,
    "missing": 0,
    "incomplete": 0,
    "placeholders": 0,
    "todo": 0,
    "pass": 0,
    "not_implemented": 0,
    "dummy": 0,
}

dummy_patterns = [
    re.compile(r'assert True'),
    re.compile(r'def test_basic\('),
    re.compile(r'return None'),
    re.compile(r'class \w+:\n    pass'),
    re.compile(r'print\(".*?eval.*?"\)'),
    re.compile(r'print\(".*?mock.*?"\)')
]

for root, _, files in os.walk('.'):
    if '.git' in root or '__pycache__' in root:
        continue
    for file in files:
        if not file.endswith(('.py', '.yaml', '.yml', '.sh', '.md', 'Dockerfile', 'Dockerfile.backend', 'Dockerfile.camera_worker')):
            continue
        if file.startswith('PROMPT'):
            continue
            
        stats["existing"] += 1
        path = os.path.join(root, file)
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            has_issue = False
            if 'TODO' in content:
                stats["todo"] += 1
                has_issue = True
            
            # Using regex for pass to avoid matching password
            if re.search(r'\bpass\b', content):
                if 'hashed_password' not in content: # Avoid false positive
                    stats["pass"] += 1
                    has_issue = True
                
            if 'NotImplementedError' in content:
                stats["not_implemented"] += 1
                has_issue = True
                
            if '...' in content:
                # Can be a placeholder, but in interfaces it's normal.
                pass
                
            is_dummy = False
            for p in dummy_patterns:
                if p.search(content):
                    is_dummy = True
                    break
            if is_dummy:
                stats["dummy"] += 1
                has_issue = True
                
            if has_issue:
                stats["incomplete"] += 1
                stats["placeholders"] += 1
                
        except Exception:
            pass

print(stats)
