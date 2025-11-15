#!/usr/bin/env python3
"""
Notebook Verification Tracker
Tracks execution and verification of each cell in the polished notebook
"""

import json
import os
from datetime import datetime
from pathlib import Path

class NotebookVerificationTracker:
    """Track and verify notebook cell execution"""

    def __init__(self, notebook_path, log_path="verification_log.json"):
        self.notebook_path = notebook_path
        self.log_path = log_path
        self.log = self.load_log()

    def load_log(self):
        """Load existing verification log or create new"""
        if os.path.exists(self.log_path):
            with open(self.log_path, 'r') as f:
                return json.load(f)
        return {
            "notebook": self.notebook_path,
            "started": datetime.now().isoformat(),
            "last_updated": None,
            "cells": {},
            "phases": {
                "Phase 1": {"total": 19, "completed": 0, "verified": 0},
                "Phase 2A": {"total": 40, "completed": 0, "verified": 0},
                "Phase 2B": {"total": 14, "completed": 0, "verified": 0},
                "Phase 3": {"total": 20, "completed": 0, "verified": 0}
            },
            "issues": [],
            "statistics": {
                "total_cells": 93,
                "completed": 0,
                "verified": 0,
                "failed": 0,
                "percentage_complete": 0.0
            }
        }

    def save_log(self):
        """Save verification log to file"""
        self.log["last_updated"] = datetime.now().isoformat()
        with open(self.log_path, 'w') as f:
            json.dump(self.log, f, indent=2)
        print(f"✓ Log saved to {self.log_path}")

    def add_cell(self, cell_num, phase, cell_type, description):
        """Register a new cell for tracking"""
        cell_id = f"cell_{cell_num:03d}"
        self.log["cells"][cell_id] = {
            "number": cell_num,
            "phase": phase,
            "type": cell_type,
            "description": description,
            "status": "pending",
            "executed": False,
            "verified": False,
            "output_verified": False,
            "timestamp": None,
            "execution_time": None,
            "notes": []
        }
        print(f"Registered Cell {cell_num}: {description[:50]}")

    def mark_executed(self, cell_num, success=True, execution_time=None, output_summary=None):
        """Mark cell as executed"""
        cell_id = f"cell_{cell_num:03d}"
        if cell_id in self.log["cells"]:
            self.log["cells"][cell_id]["executed"] = True
            self.log["cells"][cell_id]["status"] = "executed" if success else "failed"
            self.log["cells"][cell_id]["timestamp"] = datetime.now().isoformat()
            if execution_time:
                self.log["cells"][cell_id]["execution_time"] = execution_time
            if output_summary:
                self.log["cells"][cell_id]["output_summary"] = output_summary

            if not success:
                self.log["statistics"]["failed"] += 1
            else:
                self.log["statistics"]["completed"] += 1

            self.update_statistics()
            print(f"✓ Cell {cell_num} marked as {'executed' if success else 'FAILED'}")
        else:
            print(f"✗ Cell {cell_num} not found in log")

    def mark_verified(self, cell_num, verified=True, checks_passed=None, notes=None):
        """Mark cell as verified"""
        cell_id = f"cell_{cell_num:03d}"
        if cell_id in self.log["cells"]:
            self.log["cells"][cell_id]["verified"] = verified
            self.log["cells"][cell_id]["output_verified"] = verified
            if checks_passed:
                self.log["cells"][cell_id]["checks_passed"] = checks_passed
            if notes:
                self.log["cells"][cell_id]["notes"].append({
                    "timestamp": datetime.now().isoformat(),
                    "note": notes
                })

            if verified:
                self.log["statistics"]["verified"] += 1
                # Update phase statistics
                phase = self.log["cells"][cell_id]["phase"]
                if phase in self.log["phases"]:
                    self.log["phases"][phase]["verified"] += 1
                    self.log["phases"][phase]["completed"] += 1

            self.update_statistics()
            print(f"✓ Cell {cell_num} verification: {'PASSED' if verified else 'FAILED'}")
        else:
            print(f"✗ Cell {cell_num} not found in log")

    def add_issue(self, cell_num, issue_type, description, severity="medium"):
        """Log an issue found during verification"""
        issue = {
            "cell": cell_num,
            "type": issue_type,
            "description": description,
            "severity": severity,
            "timestamp": datetime.now().isoformat(),
            "resolved": False
        }
        self.log["issues"].append(issue)
        print(f"⚠ Issue logged for Cell {cell_num}: {description}")

    def resolve_issue(self, issue_index):
        """Mark an issue as resolved"""
        if issue_index < len(self.log["issues"]):
            self.log["issues"][issue_index]["resolved"] = True
            self.log["issues"][issue_index]["resolved_at"] = datetime.now().isoformat()
            print(f"✓ Issue {issue_index} resolved")

    def update_statistics(self):
        """Update overall statistics"""
        total = self.log["statistics"]["total_cells"]
        completed = self.log["statistics"]["completed"]
        verified = self.log["statistics"]["verified"]

        self.log["statistics"]["percentage_complete"] = (completed / total * 100) if total > 0 else 0
        self.log["statistics"]["percentage_verified"] = (verified / total * 100) if total > 0 else 0

    def get_phase_status(self, phase):
        """Get status of a specific phase"""
        if phase in self.log["phases"]:
            stats = self.log["phases"][phase]
            print(f"\n{phase} Status:")
            print(f"  Total cells: {stats['total']}")
            print(f"  Completed: {stats['completed']}/{stats['total']}")
            print(f"  Verified: {stats['verified']}/{stats['total']}")
            pct = (stats['verified'] / stats['total'] * 100) if stats['total'] > 0 else 0
            print(f"  Progress: {pct:.1f}%")
            return stats

    def print_status(self):
        """Print current verification status"""
        stats = self.log["statistics"]
        print("\n" + "="*70)
        print("NOTEBOOK VERIFICATION STATUS")
        print("="*70)
        print(f"Notebook: {self.notebook_path}")
        print(f"Last Updated: {self.log.get('last_updated', 'Never')}")
        print(f"\nOverall Progress:")
        print(f"  Total Cells: {stats['total_cells']}")
        print(f"  Completed: {stats['completed']} ({stats['percentage_complete']:.1f}%)")
        print(f"  Verified: {stats['verified']} ({stats.get('percentage_verified', 0):.1f}%)")
        print(f"  Failed: {stats['failed']}")
        print(f"\nPhase Breakdown:")
        for phase, data in self.log["phases"].items():
            pct = (data['verified'] / data['total'] * 100) if data['total'] > 0 else 0
            print(f"  {phase:12s}: {data['verified']}/{data['total']} verified ({pct:.0f}%)")

        if self.log["issues"]:
            unresolved = [i for i in self.log["issues"] if not i.get("resolved", False)]
            print(f"\nIssues:")
            print(f"  Total: {len(self.log['issues'])}")
            print(f"  Unresolved: {len(unresolved)}")

        print("="*70)

    def print_detailed_report(self):
        """Print detailed cell-by-cell report"""
        print("\n" + "="*70)
        print("DETAILED CELL VERIFICATION REPORT")
        print("="*70)

        for cell_id in sorted(self.log["cells"].keys()):
            cell = self.log["cells"][cell_id]
            status_icon = "✓" if cell["verified"] else ("✗" if cell["status"] == "failed" else "○")
            print(f"\n{status_icon} Cell {cell['number']:03d} [{cell['type']:8s}] - {cell['phase']}")
            print(f"   Description: {cell['description'][:60]}")
            print(f"   Status: {cell['status']}")
            print(f"   Executed: {cell['executed']} | Verified: {cell['verified']}")
            if cell.get("execution_time"):
                print(f"   Execution Time: {cell['execution_time']}")
            if cell.get("notes"):
                for note in cell['notes']:
                    print(f"   Note: {note['note']}")

        print("="*70)

    def export_report(self, filename="verification_report.txt"):
        """Export verification report to text file"""
        with open(filename, 'w') as f:
            f.write("="*70 + "\n")
            f.write("NOTEBOOK VERIFICATION REPORT\n")
            f.write("="*70 + "\n\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n")
            f.write(f"Notebook: {self.notebook_path}\n\n")

            stats = self.log["statistics"]
            f.write(f"Overall Progress: {stats['percentage_complete']:.1f}%\n")
            f.write(f"Cells Completed: {stats['completed']}/{stats['total_cells']}\n")
            f.write(f"Cells Verified: {stats['verified']}/{stats['total_cells']}\n\n")

            f.write("Phase Status:\n")
            for phase, data in self.log["phases"].items():
                pct = (data['verified'] / data['total'] * 100) if data['total'] > 0 else 0
                f.write(f"  {phase}: {data['verified']}/{data['total']} ({pct:.0f}%)\n")

            if self.log["issues"]:
                f.write(f"\n\nIssues Found: {len(self.log['issues'])}\n")
                for i, issue in enumerate(self.log["issues"]):
                    status = "RESOLVED" if issue.get("resolved") else "OPEN"
                    f.write(f"\n{i+1}. [{status}] Cell {issue['cell']} - {issue['type']}\n")
                    f.write(f"   {issue['description']}\n")
                    f.write(f"   Severity: {issue['severity']}\n")

        print(f"✓ Report exported to {filename}")


def main():
    """Main function for command-line usage"""
    tracker = NotebookVerificationTracker(
        "notebooks/Ames_Housing_Price_Prediction_Complete.ipynb",
        "notebooks/verification_log.json"
    )

    # Example usage
    tracker.print_status()

    return tracker


if __name__ == "__main__":
    tracker = main()
