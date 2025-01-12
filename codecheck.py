#!/usr/bin/env python3
import os
import re
import ast
import json
import subprocess
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
import logging

@dataclass
class ConventionViolation:
    file_path: str
    line_number: int
    rule: str
    message: str

class TypeScriptConventionChecker:
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.violations: List[ConventionViolation] = []
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def check_project_structure(self) -> None:
        """Check if project follows standard Node.js/TypeScript structure."""
        required_files = ['package.json', 'tsconfig.json', 'README.md']
        required_dirs = ['src', 'test', 'dist']
        
        for file in required_files:
            if not os.path.exists(os.path.join(self.project_path, file)):
                self.violations.append(
                    ConventionViolation(
                        file_path=self.project_path,
                        line_number=0,
                        rule="project_structure",
                        message=f"Missing required file: {file}"
                    )
                )
        
        for directory in required_dirs:
            if not os.path.exists(os.path.join(self.project_path, directory)):
                self.violations.append(
                    ConventionViolation(
                        file_path=self.project_path,
                        line_number=0,
                        rule="project_structure",
                        message=f"Missing required directory: {directory}"
                    )
                )

    def check_file_naming(self, file_path: str) -> None:
        """Check if file follows naming conventions."""
        filename = os.path.basename(file_path)
        
        # Check for proper file extensions
        if not filename.endswith(('.ts', '.tsx', '.test.ts', '.spec.ts')):
            self.violations.append(
                ConventionViolation(
                    file_path=file_path,
                    line_number=0,
                    rule="file_naming",
                    message=f"Invalid file extension: {filename}"
                )
            )
        
        # Check for camelCase or kebab-case
        name_without_ext = filename.split('.')[0]
        if not (re.match(r'^[a-z][a-zA-Z0-9]*$', name_without_ext) or 
                re.match(r'^[a-z][a-z0-9-]*[a-z0-9]$', name_without_ext)):
            self.violations.append(
                ConventionViolation(
                    file_path=file_path,
                    line_number=0,
                    rule="file_naming",
                    message=f"File name should be camelCase or kebab-case: {filename}"
                )
            )

    def check_line_length(self, file_path: str, max_length: int = 100) -> None:
        """Check if any lines exceed maximum length."""
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                if len(line.rstrip()) > max_length:
                    self.violations.append(
                        ConventionViolation(
                            file_path=file_path,
                            line_number=line_num,
                            rule="line_length",
                            message=f"Line exceeds {max_length} characters"
                        )
                    )

    def check_naming_conventions(self, file_path: str) -> None:
        """Check TypeScript naming conventions in the file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
            # Check class names (PascalCase)
            class_pattern = r'class\s+(?!^[A-Z][a-zA-Z0-9]*$)(\w+)'
            for match in re.finditer(class_pattern, content):
                self.violations.append(
                    ConventionViolation(
                        file_path=file_path,
                        line_number=content[:match.start()].count('\n') + 1,
                        rule="naming_convention",
                        message=f"Class name should be PascalCase: {match.group(1)}"
                    )
                )
            
            # Check interface names (PascalCase with I prefix)
            interface_pattern = r'interface\s+(?!^I[A-Z][a-zA-Z0-9]*$)(\w+)'
            for match in re.finditer(interface_pattern, content):
                self.violations.append(
                    ConventionViolation(
                        file_path=file_path,
                        line_number=content[:match.start()].count('\n') + 1,
                        rule="naming_convention",
                        message=f"Interface name should be PascalCase with I prefix: {match.group(1)}"
                    )
                )

    def check_imports(self, file_path: str) -> None:
        """Check import statements organization and conventions."""
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()
            
            import_lines = []
            current_section = None
            
            for line_num, line in enumerate(content, 1):
                if line.strip().startswith('import'):
                    import_lines.append((line_num, line.strip()))
                    
                    # Check relative imports
                    if '..' in line:
                        self.violations.append(
                            ConventionViolation(
                                file_path=file_path,
                                line_number=line_num,
                                rule="imports",
                                message="Avoid using parent directory imports (..)"
                            )
                        )

    def check_comments_documentation(self, file_path: str) -> None:
        """Check for proper comments and documentation."""
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()
            
            for line_num, line in enumerate(content, 1):
                # Check for TODO comments without assignee
                if 'TODO' in line and not re.search(r'TODO\s*\(@\w+\)', line):
                    self.violations.append(
                        ConventionViolation(
                            file_path=file_path,
                            line_number=line_num,
                            rule="documentation",
                            message="TODO comment should have an assignee (@username)"
                        )
                    )
                
                # Check for function documentation
                if re.match(r'\s*function', line) or re.match(r'\s*const\s+\w+\s*=\s*function', line):
                    if line_num > 1 and not any('/**' in l for l in content[max(0, line_num-4):line_num-1]):
                        self.violations.append(
                            ConventionViolation(
                                file_path=file_path,
                                line_number=line_num,
                                rule="documentation",
                                message="Missing JSDoc comment for function"
                            )
                        )

    def run_eslint_check(self) -> None:
        """Run ESLint checks on the project."""
        try:
            result = subprocess.run(
                ['npx', 'eslint', '.', '--format', 'json'],
                capture_output=True,
                text=True,
                cwd=self.project_path
            )
            
            if result.returncode != 0:
                eslint_results = json.loads(result.stdout)
                for file_result in eslint_results:
                    for message in file_result['messages']:
                        self.violations.append(
                            ConventionViolation(
                                file_path=file_result['filePath'],
                                line_number=message.get('line', 0),
                                rule="eslint",
                                message=message['message']
                            )
                        )
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error running ESLint: {str(e)}")
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing ESLint output: {str(e)}")

    def check_all(self) -> List[ConventionViolation]:
        """Run all convention checks."""
        self.logger.info("Starting convention checks...")
        
        # Check project structure
        self.check_project_structure()
        
        # Iterate through all TypeScript files
        for root, _, files in os.walk(self.project_path):
            for file in files:
                if file.endswith(('.ts', '.tsx')):
                    file_path = os.path.join(root, file)
                    self.logger.info(f"Checking file: {file_path}")
                    
                    self.check_file_naming(file_path)
                    self.check_line_length(file_path)
                    self.check_naming_conventions(file_path)
                    self.check_imports(file_path)
                    self.check_comments_documentation(file_path)
        
        # Run ESLint checks
        self.run_eslint_check()
        
        self.logger.info("Convention checks completed.")
        return self.violations

    def generate_report(self) -> str:
        """Generate a markdown report of all violations."""
        if not self.violations:
            return "# Convention Check Report\n\nNo violations found! 🎉"
        
        report = ["# Convention Check Report\n"]
        report.append(f"Total violations found: {len(self.violations)}\n")
        
        # Group violations by file
        violations_by_file: Dict[str, List[ConventionViolation]] = {}
        for violation in self.violations:
            if violation.file_path not in violations_by_file:
                violations_by_file[violation.file_path] = []
            violations_by_file[violation.file_path].append(violation)
        
        # Generate report sections
        for file_path, file_violations in violations_by_file.items():
            report.append(f"\n## {os.path.relpath(file_path, self.project_path)}\n")
            for violation in file_violations:
                report.append(f"- Line {violation.line_number}: [{violation.rule}] {violation.message}")
        
        return "\n".join(report)

def main():
    # Example usage
    project_path = "."  # Current directory
    checker = TypeScriptConventionChecker(project_path)
    violations = checker.check_all()
    
    # Generate and save report
    report = checker.generate_report()
    with open("convention_report.md", "w") as f:
        f.write(report)
    
    print(f"Found {len(violations)} violations. See convention_report.md for details.")

if __name__ == "__main__":
    main()
