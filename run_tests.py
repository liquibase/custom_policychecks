#!/usr/bin/env python3
"""
Two-stage test execution strategy for Python Policy Checks

Stage 1: Fast feedback with lightweight tests (fail-fast approach)
Stage 2: Comprehensive parallel testing with coverage (if Stage 1 passes)

Usage:
    python run_tests.py              # Run both stages
    python run_tests.py --fast-only  # Run only Stage 1
    python run_tests.py --full-only  # Run only Stage 2
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd: list[str], description: str) -> tuple[int, str]:
    """Run a command and return exit code and output."""
    print(f"\n🚀 {description}")
    print(f"Command: {' '.join(cmd)}")
    print("=" * 60)
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=900  # 15 minutes max per stage
        )
        
        # Print output in real-time style
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
            
        return result.returncode, result.stdout + result.stderr
    
    except subprocess.TimeoutExpired:
        print(f"❌ TIMEOUT: {description} exceeded 15 minutes")
        return 1, "Timeout expired"
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return 1, str(e)


def stage1_fast_tests() -> int:
    """Stage 1: Fast feedback tests - table names only (known to work quickly)."""
    cmd = [
        "uv", "run", "python", "-m", "pytest", 
        "Python/tests/test_table_names_uppercase.py",
        "-v", "--tb=short", "-x",  # fail-fast
        "--timeout=60"  # 1 minute timeout per test
    ]
    
    exit_code, output = run_command(cmd, "Stage 1: Fast Feedback Tests")
    
    if exit_code == 0:
        print("✅ Stage 1 PASSED: Fast tests completed successfully")
        return 0
    else:
        print(f"❌ Stage 1 FAILED: Exit code {exit_code}")
        print("🛑 Stopping execution due to Stage 1 failure - please review failures")
        return exit_code


def stage2_full_tests() -> int:
    """Stage 2: Comprehensive parallel testing with coverage."""
    cmd = [
        "uv", "run", "python", "-m", "pytest",
        "Python/tests/",
        "--cov", "--cov-report=html", "--cov-report=xml", "--cov-report=term-missing",
        "-n", "4",  # 4 parallel workers
        "-v", "--tb=short",
        "--timeout=300"  # 5 minutes timeout per test
    ]
    
    exit_code, output = run_command(cmd, "Stage 2: Comprehensive Parallel Tests with Coverage")
    
    if exit_code == 0:
        print("✅ Stage 2 PASSED: All tests completed successfully")
        print("📊 Coverage reports generated:")
        print("   - HTML: htmlcov/index.html") 
        print("   - XML:  coverage.xml")
        return 0
    else:
        print(f"❌ Stage 2 FAILED: Exit code {exit_code}")
        return exit_code


def main():
    parser = argparse.ArgumentParser(description="Two-stage test execution for Python Policy Checks")
    parser.add_argument("--fast-only", action="store_true", help="Run only Stage 1 (fast tests)")
    parser.add_argument("--full-only", action="store_true", help="Run only Stage 2 (full tests)")
    args = parser.parse_args()
    
    print("🧪 Python Policy Checks - Two-Stage Test Strategy")
    print("=" * 60)
    
    # Validate we're in the right directory
    if not Path("Python/tests").exists():
        print("❌ ERROR: Must run from project root (Python/tests not found)")
        return 1
    
    overall_exit_code = 0
    
    # Stage 1: Fast feedback tests
    if not args.full_only:
        stage1_result = stage1_fast_tests()
        if stage1_result != 0:
            if args.fast_only:
                return stage1_result
            else:
                print("🛑 Skipping Stage 2 due to Stage 1 failure")
                return stage1_result
        overall_exit_code = max(overall_exit_code, stage1_result)
    
    # Stage 2: Comprehensive tests (only if Stage 1 passed or --full-only)
    if not args.fast_only:
        stage2_result = stage2_full_tests()
        overall_exit_code = max(overall_exit_code, stage2_result)
    
    # Final summary
    print("\n" + "=" * 60)
    if overall_exit_code == 0:
        print("🎉 ALL TESTS PASSED - Quality gates satisfied!")
    else:
        print(f"❌ TESTS FAILED - Exit code: {overall_exit_code}")
    print("=" * 60)
    
    return overall_exit_code


if __name__ == "__main__":
    sys.exit(main())