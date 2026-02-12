"""
Workflow Tracker - Comprehensive logging and awareness of all operations
The AI uses this to track what clips it's taking, how it's editing them, and how it's merging
"""
import json
import os
from datetime import datetime
from config import OUTPUT_DIR

class WorkflowTracker:
    """
    Tracks every decision the AI makes during production.
    Provides full transparency and awareness.
    """
    def __init__(self):
        self.decisions = []
        self.clips_manifest = []
        self.editing_log = []
        self.merge_plan = []
        
    def log_decision(self, agent, decision_type, decision, rationale):
        """Log an AI decision with rationale."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "type": decision_type,
            "decision": decision,
            "rationale": rationale
        }
        self.decisions.append(entry)
        print(f"   🧠 {agent}: {decision} - {rationale}")
    
    def register_clip(self, clip_number, source, path, metadata):
        """Register a clip with full metadata."""
        clip_info = {
            "number": clip_number,
            "source": source,
            "path": path,
            "original_duration": metadata.get('duration'),
            "original_resolution": metadata.get('resolution'),
            "description": metadata.get('description'),
            "acquired_from": metadata.get('api'),
            "timestamp": datetime.now().isoformat()
        }
        self.clips_manifest.append(clip_info)
        
        print(f"\n   📹 CLIP {clip_number} REGISTERED:")
        print(f"      Source: {source}")
        print(f"      File: {os.path.basename(path)}")
        print(f"      Duration: {metadata.get('duration', 'unknown')}s")
        print(f"      Resolution: {metadata.get('resolution', 'unknown')}")
        print(f"      API: {metadata.get('api', 'local')}")
    
    def log_edit_operation(self, clip_number, operation, params, result):
        """Log each editing operation performed on a clip."""
        edit = {
            "clip": clip_number,
            "operation": operation,
            "parameters": params,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        self.editing_log.append(edit)
        
        print(f"      ✂️ EDIT: {operation}")
        print(f"         Params: {params}")
        print(f"         Result: {result}")
    
    def create_merge_plan(self, clips, transitions, audio_layers):
        """Document the complete merge strategy."""
        self.merge_plan = {
            "total_clips": len(clips),
            "clips": [
                {
                    "position": i,
                    "file": os.path.basename(c['path']),
                    "duration": c.get('final_duration'),
                    "transition_to_next": transitions[i] if i < len(transitions) else "none"
                }
                for i, c in enumerate(clips)
            ],
            "audio_layers": audio_layers,
            "total_duration": sum(c.get('final_duration', 0) for c in clips),
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"\n   🎬 MERGE PLAN CREATED:")
        print(f"      Total clips: {len(clips)}")
        print(f"      Total duration: {self.merge_plan['total_duration']:.1f}s")
        print(f"      Audio layers: {len(audio_layers)}")
        
        for i, clip in enumerate(self.merge_plan['clips']):
            print(f"      {i+1}. {clip['file']} ({clip['duration']:.1f}s) → {clip['transition_to_next']}")
    
    def save_report(self):
        """Save complete workflow report to JSON."""
        report = {
            "decisions": self.decisions,
            "clips_manifest": self.clips_manifest,
            "editing_log": self.editing_log,
            "merge_plan": self.merge_plan,
            "generated_at": datetime.now().isoformat()
        }
        
        report_path = os.path.join(OUTPUT_DIR, "workflow_report.json")
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n   📊 Workflow report saved: {report_path}")
        return report_path
    
    def print_summary(self):
        """Print human-readable summary of entire workflow."""
        print("\n" + "="*60)
        print("   WORKFLOW SUMMARY")
        print("="*60)
        
        print(f"\n   🎬 CLIPS ACQUIRED: {len(self.clips_manifest)}")
        for clip in self.clips_manifest:
            print(f"      {clip['number']}. {os.path.basename(clip['path'])}")
            print(f"         From: {clip['acquired_from']}")
            print(f"         Duration: {clip['original_duration']}s")
        
        print(f"\n   ✂️ EDITING OPERATIONS: {len(self.editing_log)}")
        ops_summary = {}
        for edit in self.editing_log:
            op = edit['operation']
            ops_summary[op] = ops_summary.get(op, 0) + 1
        for op, count in ops_summary.items():
            print(f"      {op}: {count}x")
        
        print(f"\n   🔀 MERGE SEQUENCE:")
        if self.merge_plan:
            for i, clip in enumerate(self.merge_plan['clips']):
                print(f"      {i+1}. {clip['file']}")
                print(f"         Duration: {clip['duration']:.1f}s")
                print(f"         Transition: {clip['transition_to_next']}")
        
        print("\n" + "="*60)
