import ast
import os

# ---------------------------
# Configuration
# ---------------------------

CONFIG = {
    "rules": {
        "max_function_length": 15,
        "max_parameters": 3,
        "max_nested_depth": 2,
    },
    "exclude_paths": [".venv", "build", "__pycache__", ".ipynb_checkpoints"],
    "severity_threshold": None
}

# ---------------------------
# Issue Class
# ---------------------------

class Issue:
    def __init__(self, file, line, rule, message, severity):
        self.file = file
        self.line = line
        self.rule = rule
        self.message = message
        self.severity = severity

    def to_dict(self):
        return {
            "file": self.file,
            "line": self.line,
            "rule": self.rule,
            "message": self.message,
            "severity": self.severity,
        }

# ---------------------------
# Analyzer Class
# ---------------------------

class CodeQualityAnalyzer:
    def __init__(self, rules, exclude_paths, severity_threshold):
        self.rules = rules
        self.exclude_paths = exclude_paths
        self.severity_threshold = severity_threshold
        self.issues = []

    def analyze_path(self, path):
        if os.path.isfile(path) and path.endswith(".py"):
            self._analyze_file(path)
        else:
            for root, dirs, files in os.walk(path):
                if any(ex in root for ex in self.exclude_paths):
                    continue
                for file in files:
                    if file.endswith(".py"):
                        self._analyze_file(os.path.join(root, file))

    def _analyze_file(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                source = f.read()

            tree = ast.parse(source)
            self._check_functions(tree, filepath)

        except Exception as e:
            print(f"Error analyzing {filepath}: {e}")

    def _check_functions(self, tree, filepath):
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self._check_function_length(node, filepath)
                self._check_parameters(node, filepath)
                self._check_nesting(node, filepath)

    def _add_issue(self, issue):
        severity_scores = {"Low": 1, "Medium": 3, "High": 5}

        if self.severity_threshold:
            if severity_scores[issue.severity] < severity_scores[self.severity_threshold]:
                return

        self.issues.append(issue)

    def _check_function_length(self, node, filepath):
        max_len = self.rules.get("max_function_length")
        if max_len and len(node.body) > max_len:
            self._add_issue(Issue(
                filepath,
                node.lineno,
                "Function Length",
                f"Function '{node.name}' is too long ({len(node.body)} lines)",
                "Medium",
            ))

    def _check_parameters(self, node, filepath):
        max_params = self.rules.get("max_parameters")
        if max_params and len(node.args.args) > max_params:
            self._add_issue(Issue(
                filepath,
                node.lineno,
                "Too Many Parameters",
                f"Function '{node.name}' has too many parameters ({len(node.args.args)})",
                "Low",
            ))

    def _check_nesting(self, node, filepath):
        max_depth = self.rules.get("max_nested_depth")
        depth = self._get_depth(node)

        if max_depth and depth > max_depth:
            self._add_issue(Issue(
                filepath,
                node.lineno,
                "Deep Nesting",
                f"Function '{node.name}' has deep nesting ({depth} levels)",
                "High",
            ))

    def _get_depth(self, node, current=0):
        if not hasattr(node, "body"):
            return current

        depths = [current]
        for child in node.body:
            depths.append(self._get_depth(child, current + 1))

        return max(depths)

# ---------------------------
# Create Sample File (Demo)
# ---------------------------

sample_code = """
def add(a, b, c, d, e):
    return a + b + c + d + e

def long_function():
    total = 0
    for i in range(10):
        total += i
        for j in range(5):
            total += j
            for k in range(3):
                total += k

    for x in range(5):
        total += x
    for y in range(5):
        total += y
    for z in range(5):
        total += z

    return total

def nested_function():
    if True:
        if True:
            if True:
                if True:
                    print("Deep nesting")
"""

with open("sample.py", "w", encoding="utf-8") as f:
    f.write(sample_code)

# ---------------------------
# Run Analyzer
# ---------------------------

analyzer = CodeQualityAnalyzer(
    rules=CONFIG["rules"],
    exclude_paths=CONFIG["exclude_paths"],
    severity_threshold=CONFIG["severity_threshold"]
)

analyzer.analyze_path("sample.py")

# ---------------------------
# Print Results
# ---------------------------

print("\nCode Quality Analysis Report")
print("=" * 35)

if not analyzer.issues:
    print("No issues found! 🎉")
else:
    for issue in analyzer.issues:
        print(f"\nFile: {issue.file}")
        print(f"Line: {issue.line}")
        print(f"Rule: {issue.rule}")
        print(f"Message: {issue.message}")
        print(f"Severity: {issue.severity}")

    print("\nTotal Issues Found:", len(analyzer.issues))