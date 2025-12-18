#!/usr/bin/env python
"""
Comprehensive Diagnostic Script for Phase 1 Issues
"""
import subprocess
import sys
import os
import json
from pathlib import Path

def check_powershell_issue():
    """Check if PowerShell execution policy is blocking scripts"""
    print("🔍 CHECK 1: PowerShell Execution Policy")
    print("-" * 50)
    
    try:
        # Try to run a simple PowerShell command
        result = subprocess.run(
            ["powershell", "-Command", "Get-ExecutionPolicy -Scope CurrentUser"],
            capture_output=True,
            text=True,
            shell=True
        )
        
        execution_policy = result.stdout.strip()
        print(f"Current Execution Policy: {execution_policy}")
        
        if "Restricted" in execution_policy or "AllSigned" in execution_policy:
            print("❌ ISSUE DETECTED: Scripts are blocked!")
            print("   Solution: Run PowerShell as Admin and execute:")
            print("   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser")
            return False
        else:
            print("✅ PowerShell scripts should work correctly")
            return True
            
    except Exception as e:
        print(f"⚠️  Could not check PowerShell: {e}")
        return False

def check_virtual_environment():
    """Check if virtual environment can be activated"""
    print("\n🔍 CHECK 2: Virtual Environment Activation")
    print("-" * 50)
    
    project_root = Path.cwd()
    venv_path = project_root / "venv"
    
    if not venv_path.exists():
        print("❌ Virtual environment not found!")
        print("   Run: python -m venv venv")
        return False
    
    # Try different activation scripts
    activation_scripts = {
        "Windows": venv_path / "Scripts" / "Activate.ps1",
        "Unix": venv_path / "bin" / "activate"
    }
    
    for system, script in activation_scripts.items():
        if script.exists():
            print(f"✅ Found activation script for {system}: {script}")
            try:
                # Test if we can read the script
                with open(script, 'r') as f:
                    first_line = f.readline()
                print(f"   Script is readable")
                return True
            except Exception as e:
                print(f"❌ Cannot read script: {e}")
                return False
    
    print("❌ No activation script found!")
    return False

def check_python_syntax_errors():
    """Check for syntax errors in Python files"""
    print("\n🔍 CHECK 3: Python Syntax Errors")
    print("-" * 50)
    
    python_files = []
    
    # Find all Python files
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".py"):
                python_files.append(Path(root) / file)
    
    print(f"Found {len(python_files)} Python files")
    
    errors = []
    for py_file in python_files[:10]:  # Check first 10 files
        try:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(py_file)],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                errors.append((py_file, result.stderr))
        except Exception as e:
            errors.append((py_file, str(e)))
    
    if errors:
        print("❌ Syntax errors found:")
        for file, error in errors[:3]:  # Show first 3 errors
            print(f"   File: {file}")
            print(f"   Error: {error[:100]}...")
        return False
    else:
        print("✅ No syntax errors detected")
        return True

def check_data_pipeline():
    """Verify Phase 1 data pipeline is complete"""
    print("\n🔍 CHECK 4: Data Pipeline Status")
    print("-" * 50)
    
    checks = {
        "Raw data file exists": Path("data/raw/hotpot_dev_distractor_v1.json").exists(),
        "Processed subset exists": Path("data/processed/dev_subset_100.json").exists(),
        "src/ directory exists": Path("src").exists(),
        "requirements.txt exists": Path("requirements.txt").exists(),
    }
    
    all_ok = True
    for check_name, status in checks.items():
        if status:
            print(f"✅ {check_name}")
        else:
            print(f"❌ {check_name}")
            all_ok = False
    
    # Check file contents
    subset_path = Path("data/processed/dev_subset_100.json")
    if subset_path.exists():
        try:
            with open(subset_path, 'r') as f:
                data = json.load(f)
            examples = data.get('examples', [])
            print(f"✅ Subset contains {len(examples)} examples")
            
            # Verify structure
            if examples:
                ex = examples[0]
                required_keys = ['_id', 'question', 'answer', 'type', 'context', 'supporting_facts']
                missing = [k for k in required_keys if k not in ex]
                if missing:
                    print(f"❌ Missing keys in examples: {missing}")
                    all_ok = False
                else:
                    print(f"✅ Example structure is correct")
                    
        except json.JSONDecodeError as e:
            print(f"❌ JSON file is corrupted: {e}")
            all_ok = False
    
    return all_ok

def check_project_structure():
    """Verify complete project structure from your plan"""
    print("\n🔍 CHECK 5: Project Structure Completeness")
    print("-" * 50)
    
    required_dirs = [
        ".vscode",
        "data/raw",
        "data/processed", 
        "src",
        "scripts",
        "notebooks",
        "reports/data_analysis"
    ]
    
    required_files = [
        ".vscode/settings.json",
        ".vscode/launch.json",
        "src/__init__.py",
        "src/config.py",
        "src/data_loader.py",
        "src/preprocessor.py",
        "src/utils.py",
        "scripts/setup_data.py",
        "scripts/analyze_data.py",
        "requirements.txt",
        "README.md",
        ".gitignore"
    ]
    
    print("Required Directories:")
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"  ✅ {dir_path}")
        else:
            print(f"  ❌ {dir_path} (MISSING)")
    
    print("\nRequired Files:")
    all_files_exist = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} (MISSING)")
            all_files_exist = False
    
    return all_files_exist

def check_verification_script():
    """Test the exact verification script that had issues"""
    print("\n🔍 CHECK 6: Verification Script Test")
    print("-" * 50)
    
    # Create a temporary test script
    test_script = """
import json
from pathlib import Path

print('=' * 60)
print('TEST VERIFICATION SCRIPT')
print('=' * 60)

files = [
    ('Raw data', Path('data/raw/hotpot_dev_distractor_v1.json')),
    ('Subset', Path('data/processed/dev_subset_100.json'))
]

for name, path in files:
    if path.exists():
        size_mb = path.stat().st_size / (1024 * 1024)
        print(f'✓ {name}: {size_mb:.1f} MB')
    else:
        print(f'✗ {name}: MISSING')
"""
    
    try:
        # Write test script
        with open("test_verification.py", "w") as f:
            f.write(test_script)
        
        # Run it
        result = subprocess.run(
            [sys.executable, "test_verification.py"],
            capture_output=True,
            text=True
        )
        
        # Clean up
        Path("test_verification.py").unlink(missing_ok=True)
        
        if result.returncode == 0:
            print("✅ Verification script runs without errors")
            print(f"Output:\n{result.stdout}")
            return True
        else:
            print("❌ Verification script failed!")
            print(f"Error:\n{result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to test verification script: {e}")
        return False

def run_all_checks():
    """Run all diagnostic checks"""
    print("🚀 RUNNING COMPREHENSIVE DIAGNOSTIC")
    print("=" * 60)
    
    results = {
        "PowerShell": check_powershell_issue(),
        "Virtual Environment": check_virtual_environment(),
        "Python Syntax": check_python_syntax_errors(),
        "Data Pipeline": check_data_pipeline(),
        "Project Structure": check_project_structure(),
        "Verification Script": check_verification_script(),
    }
    
    print("\n" + "=" * 60)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for check, status in results.items():
        status_symbol = "✅" if status else "❌"
        print(f"{status_symbol} {check}")
    
    print(f"\n🎯 Result: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🌟 All checks passed! Your Phase 1 is ready.")
    else:
        print("\n⚠️  Issues detected. Run the fixes below:")
        
        if not results["PowerShell"]:
            print("\n1. Fix PowerShell Execution Policy:")
            print("   Run PowerShell as Administrator and execute:")
            print("   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser")
        
        if not results["Project Structure"]:
            print("\n2. Complete missing files from your structure plan")
            print("   Check the files marked as MISSING above")
        
        if not results["Data Pipeline"]:
            print("\n3. Run setup_data.py to complete data pipeline:")
            print("   python scripts/setup_data.py")

if __name__ == "__main__":
    run_all_checks()