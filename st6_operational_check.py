#!/usr/bin/env python3
"""
SEAL TEAM Six Operational Readiness Check
==========================================

Mission: Verify all systems are combat-ready for OpenAI Cookbook operations.

This script performs comprehensive pre-flight checks to ensure:
- Environment configuration is mission-ready
- Dependencies are properly installed
- API connectivity is operational
- Security protocols are in place

Usage:
    python st6_operational_check.py

Author: JAMES BRANCHFORD ECHOLS, II (branch@softengineware.ai)
Created: 2025-01-28
License: MIT - Enhanced with ST6 Excellence Standards
"""

import os
import sys
import subprocess
import importlib
import time
from typing import Dict, List, Tuple, Optional
from datetime import datetime

# SEAL TEAM Six Colors for terminal output
class ST6Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class OperationalCheck:
    """SEAL TEAM Six Operational Readiness Assessment"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.checks_passed = 0
        self.checks_failed = 0
        self.warnings = 0
        self.results: List[Tuple[str, bool, str]] = []
    
    def print_header(self):
        """Print mission briefing header"""
        print(f"{ST6Colors.HEADER}{ST6Colors.BOLD}")
        print("🔱" + "="*60 + "🔱")
        print("          SEAL TEAM Six - Operational Readiness Check")
        print("🔱" + "="*60 + "🔱")
        print(f"{ST6Colors.ENDC}")
        print(f"{ST6Colors.OKBLUE}Mission Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"The Only Easy Day Was Yesterday{ST6Colors.ENDC}")
        print()
    
    def check_result(self, check_name: str, passed: bool, details: str = ""):
        """Record and display check result"""
        if passed:
            self.checks_passed += 1
            status = f"{ST6Colors.OKGREEN}✅ PASS{ST6Colors.ENDC}"
        else:
            self.checks_failed += 1
            status = f"{ST6Colors.FAIL}❌ FAIL{ST6Colors.ENDC}"
        
        self.results.append((check_name, passed, details))
        print(f"{status} {check_name}")
        if details:
            print(f"    {details}")
    
    def warning_result(self, check_name: str, details: str = ""):
        """Record and display warning"""
        self.warnings += 1
        status = f"{ST6Colors.WARNING}⚠️  WARN{ST6Colors.ENDC}"
        print(f"{status} {check_name}")
        if details:
            print(f"    {details}")
    
    def check_python_version(self):
        """Verify Python version meets mission requirements"""
        version = sys.version_info
        min_version = (3, 8)
        
        passed = version >= min_version
        details = f"Python {version.major}.{version.minor}.{version.micro}"
        if not passed:
            details += f" (Minimum required: {min_version[0]}.{min_version[1]})"
        
        self.check_result("Python Version", passed, details)
    
    def check_openai_api_key(self):
        """Verify OpenAI API key is configured"""
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            self.check_result("OpenAI API Key", False, "OPENAI_API_KEY environment variable not set")
            return
        
        if api_key.startswith('sk-'):
            if len(api_key) > 20:  # Basic length check
                self.check_result("OpenAI API Key", True, "Key format appears valid")
            else:
                self.check_result("OpenAI API Key", False, "Key appears too short")
        else:
            self.check_result("OpenAI API Key", False, "Key format invalid (should start with 'sk-')")
    
    def check_required_packages(self):
        """Verify critical packages are installed"""
        required_packages = [
            'openai',
            'requests',
            'numpy',
            'pandas',
            'matplotlib',
            'jupyter',
            'tiktoken'
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                importlib.import_module(package)
            except ImportError:
                missing_packages.append(package)
        
        if not missing_packages:
            self.check_result("Required Packages", True, "All critical packages installed")
        else:
            self.check_result("Required Packages", False, 
                            f"Missing packages: {', '.join(missing_packages)}")
    
    def check_openai_connectivity(self):
        """Test OpenAI API connectivity"""
        try:
            import openai
            client = openai.OpenAI()
            
            # Simple test request
            response = client.models.list()
            self.check_result("OpenAI API Connectivity", True, "API accessible and responding")
            
        except ImportError:
            self.check_result("OpenAI API Connectivity", False, "OpenAI package not installed")
        except Exception as e:
            self.check_result("OpenAI API Connectivity", False, f"Connection failed: {str(e)}")
    
    def check_security_protocols(self):
        """Verify security best practices"""
        issues = []
        
        # Check for .env file
        if os.path.exists('.env'):
            self.warning_result("Security Check", ".env file present - ensure it's in .gitignore")
        
        # Check if API key is hardcoded (basic check)
        try:
            for root, dirs, files in os.walk('.'):
                if '.git' in dirs:
                    dirs.remove('.git')
                for file in files:
                    if file.endswith('.py'):
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, 'r', encoding='utf-8') as f:
                                content = f.read()
                                if 'sk-' in content and 'OPENAI_API_KEY' not in content:
                                    issues.append(f"Potential hardcoded key in {filepath}")
                        except:
                            continue
        except Exception:
            pass
        
        if not issues:
            self.check_result("Security Protocols", True, "No obvious security issues detected")
        else:
            for issue in issues:
                self.check_result("Security Protocols", False, issue)
    
    def check_git_status(self):
        """Check git repository status"""
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, cwd='.')
            
            if result.returncode == 0:
                if result.stdout.strip():
                    self.warning_result("Git Status", "Uncommitted changes detected")
                else:
                    self.check_result("Git Status", True, "Working directory clean")
            else:
                self.check_result("Git Status", False, "Not a git repository or git error")
        except FileNotFoundError:
            self.check_result("Git Status", False, "Git not installed")
    
    def print_summary(self):
        """Print mission summary report"""
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        print("\n" + "="*60)
        print(f"{ST6Colors.HEADER}{ST6Colors.BOLD}MISSION SUMMARY REPORT{ST6Colors.ENDC}")
        print("="*60)
        
        total_checks = self.checks_passed + self.checks_failed
        success_rate = (self.checks_passed / total_checks * 100) if total_checks > 0 else 0
        
        print(f"✅ Checks Passed:   {self.checks_passed}")
        print(f"❌ Checks Failed:   {self.checks_failed}")
        print(f"⚠️  Warnings:       {self.warnings}")
        print(f"📊 Success Rate:    {success_rate:.1f}%")
        print(f"⏱️  Duration:       {duration.total_seconds():.2f} seconds")
        
        if self.checks_failed == 0:
            print(f"\n{ST6Colors.OKGREEN}{ST6Colors.BOLD}🔱 MISSION STATUS: READY FOR OPERATIONS 🔱{ST6Colors.ENDC}")
            print(f"{ST6Colors.OKGREEN}All systems operational. Proceed with confidence.{ST6Colors.ENDC}")
        else:
            print(f"\n{ST6Colors.FAIL}{ST6Colors.BOLD}⚠️  MISSION STATUS: NOT READY - RESOLVE ISSUES ⚠️{ST6Colors.ENDC}")
            print(f"{ST6Colors.FAIL}Address failed checks before proceeding.{ST6Colors.ENDC}")
        
        print(f"\n{ST6Colors.OKBLUE}The Only Easy Day Was Yesterday{ST6Colors.ENDC}")
        print("🔱" + "="*58 + "🔱")

def main():
    """Execute operational readiness check"""
    checker = OperationalCheck()
    
    # Mission briefing
    checker.print_header()
    
    # Execute all checks
    print(f"{ST6Colors.OKCYAN}Executing operational readiness checks...{ST6Colors.ENDC}\n")
    
    checker.check_python_version()
    checker.check_openai_api_key()
    checker.check_required_packages()
    checker.check_openai_connectivity()
    checker.check_security_protocols()
    checker.check_git_status()
    
    # Mission summary
    checker.print_summary()
    
    # Exit with appropriate code
    return 0 if checker.checks_failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())