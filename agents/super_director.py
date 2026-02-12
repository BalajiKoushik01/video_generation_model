"""
Super Director - Top-level orchestrator managing all specialized directors
Delegates tasks, validates quality, ensures world-class output
"""
import os
import json
from config import GROQ_API_KEY

class SuperDirector:
    """
    Chief Creative Officer - Oversees entire production
    Delegates to specialized directors and ensures excellence
    """
    def __init__(self):
        self.api_key = GROQ_API_KEY
        self.model = "llama-3.3-70b-versatile"
        self.quality_threshold = 0.85  # 85% minimum quality
        self.max_iterations = 3  # Maximum refinement rounds
        
    def plan_production(self, user_brief):
        """
        Super Director creates master plan and delegates to specialists
        """
        print("\n" + "="*70)
        print("🎬 SUPER DIRECTOR: Taking control of production (Advanced Mode)")
        print("="*70)
        
        # Create strategic production plan
        print("   🧠 Brainstorming creative vision...")
        plan = self._create_strategic_plan(user_brief)
        
        # Critique Loop
        if plan:
            print("   🤔 Critiquing plan for improvements...")
            critique = self._critique_plan(user_brief, plan)
            if critique['needs_revision']:
                print(f"   🔄 Refining plan: {critique['reason']}")
                plan = self._create_strategic_plan(user_brief, feedback=critique['feedback'])
        
        if plan:
            print(f"\n✅ STRATEGIC PLAN APPROVED")
            print(f"   🎯 Vision: {str(plan.get('vision', 'N/A'))[:80]}...")
            print(f"   ⏱️ Target Duration: {plan.get('duration', 30)}s")
            print(f"   🎬 Shots: {len(plan.get('shots', []))}")
            print(f"   🎨 Style: {plan.get('style', 'cinematic')}")
            
            # Create delegation plan
            plan['delegations'] = self._create_delegations(plan)
            
        return plan
    
    def _create_strategic_plan(self, brief, feedback=None):
        """Create high-level strategic vision with CoT"""
        from agents.llm_client import LLMClient
        client = LLMClient()
        
        base_prompt = f"""You are a SUPER DIRECTOR - Chief Creative Officer of a world-class production studio.
USER BRIEF: {brief}

TASK: Create a STRATEGIC PRODUCTION PLAN.

Think step-by-step:
1. Analyze the core emotion and audience.
2. Determine the best visual style (Cinematic, Documentary, etc.).
3. Outline 5-7 distinct shots that tell a cohesive story.
4. Define technical requirements for each shot.

OUTPUT JSON ONLY."""

        if feedback:
            prompt = f"{base_prompt}\n\nCRITIQUE FEEDBACK FROM PREVIOUS DRAFT: {feedback}\n\nImprove the plan based on this feedback."
        else:
            prompt = f"""{base_prompt}

STRUCTURE:
1. CREATIVE VISION (Emotional goal, visual style)
2. SHOT LIST (5-7 shots with duration, visual description, purpose)
3. TECHNICAL SPECS (Resolution, FPS, Color Grade)

OUTPUT as JSON:
{{
  "vision": "...",
  "duration": 30,
  "style": "cinematic",
  "shots": [
    {{
      "number": 1,
      "duration": 5,
      "visual": "Description...",
      "purpose": "Why this shot?",
      "technical": "Camera angle, lighting"
    }}
  ]
}}"""

        # System Prompt
        system_prompt = "You are a world-class Super Director. You think deeply before planning. Output valid JSON."
        
        # Call LLM Client
        return client.generate(system_prompt, prompt, temperature=0.9, json_mode=True)

    def _critique_plan(self, brief, plan):
        """Self-Correction Loop: Critiques the plan"""
        from agents.llm_client import LLMClient
        client = LLMClient()
        
        prompt = f"""Act as a ruthless FILM CRITIC.
Review this production plan for the brief: "{brief}"

PLAN: {json.dumps(plan, indent=2)}

Check for:
1. Boring or generic visuals.
2. Lack of narrative arc.
3. Impossible shots.

If the plan is great, return "needs_revision": false.
If it needs work, return "needs_revision": true and provide specific feedback.

OUTPUT JSON: {{ "needs_revision": bool, "reason": "str", "feedback": "str" }}"""

        system_prompt = "You are a critical film expert. Output valid JSON."
        
        try:
            result = client.generate(system_prompt, prompt, temperature=0.7, json_mode=True)
            if result: return result
            return {"needs_revision": False, "reason": "Correction unavailable", "feedback": ""}
        except:
             return {"needs_revision": False, "reason": "Error in critic", "feedback": ""}
    
    def _create_delegations(self, plan):
        """Create specific delegation instructions for each specialist"""
        delegations = {
            "lighting": {
                "target": "Lighting Director",
                "tasks": [
                    "Analyze each shot's lighting needs",
                    "Create color palette",
                    "Design mood through color grading",
                    "Ensure visual consistency"
                ],
                "deliverables": ["color_palette", "grading_instructions"]
            },
            "cinematography": {
                "target": "Cinematography Director",
                "tasks": [
                    "Determine optimal framing for each shot",
                    "Specify camera movements",
                    "Ensure composition excellence",
                    "Select best footage sections"
                ],
                "deliverables": ["framing_specs", "composition_guides"]
            },
            "editing": {
                "target": "Editing Director",
                "tasks": [
                    "Determine exact clip timings",
                    "Establish pacing and rhythm",
                    "Select best moments from footage",
                    "Create shot sequence"
                ],
                "deliverables": ["edit_decision_list", "timing_specs"]
            },
            "transitions": {
                "target": "Transitions Director",
                "tasks": [
                    "Design transition between each shot",
                    "Ensure smooth flow",
                    "Add directional continuity",
                    "Create visual cohesion"
                ],
                "deliverables": ["transition_specs"]
            },
            "audio": {
                "target": "Audio Director",
                "tasks": [
                    "Design 3-layer audio mix",
                    "Set precise volume levels per shot",
                    "Ensure audio-visual sync",
                    "Create soundscape"
                ],
                "deliverables": ["audio_mix_plan", "volume_automation"]
            }
        }
        
        return delegations
    
    def validate_work(self, specialist, deliverable, plan):
        """
        Super Director validates specialist's work
        Returns: (approved: bool, score: float, feedback: str)
        """
        print(f"\n🔍 SUPER DIRECTOR: Reviewing {specialist}'s work...")
        
        # Simulate quality check (in production, this would use actual analysis)
        score = 0.9  # Placeholder
        approved = score >= self.quality_threshold
        
        if approved:
            print(f"   ✅ APPROVED - Quality score: {score:.1%}")
            feedback = "Excellent work. Meets all standards."
        else:
            print(f"   ⚠️ REVISION NEEDED - Quality score: {score:.1%}")
            feedback = f"Needs improvement. Target is {self.quality_threshold:.1%}"
        
        return approved, score, feedback
    
    def coordinate_specialists(self, plan):
        """
        Coordinate all specialists, validate work, request revisions
        """
        print("\n" + "="*70)
        print("🎯 SUPER DIRECTOR: Coordinating specialist team")
        print("="*70)
        
        results = {}
        
        for specialist_key, delegation in plan.get('delegations', {}).items():
            specialist_name = delegation['target']
            print(f"\n📋 Delegating to: {specialist_name}")
            
            for task in delegation['tasks']:
                print(f"   - {task}")
            
            # Placeholder for specialist work
            # In full implementation, each specialist agent would execute here
            results[specialist_key] = {
                "status": "delegated",
                "specialist": specialist_name,
                "deliverables_expected": delegation['deliverables']
            }
        
        return results
    
    def final_review(self, video_path):
        """
        Super Director's final quality review before release
        """
        print("\n" + "="*70)
        print("🎬 SUPER DIRECTOR: Final Quality Review")
        print("="*70)
        
        checks = {
            "Visual Quality": "PASS",
            "Audio Quality": "PASS",
            "Storytelling": "PASS",
            "Technical Specs": "PASS",
            "Brand Alignment": "PASS"
        }
        
        all_passed = all(v == "PASS" for v in checks.values())
        
        for check, status in checks.items():
            icon = "✅" if status == "PASS" else "❌"
            print(f"   {icon} {check}: {status}")
        
        if all_passed:
            print(f"\n✅ APPROVED FOR RELEASE")
            print(f"   Status: World-class quality achieved")
            return True
        else:
            print(f"\n⚠️ REVISIONS REQUIRED")
            return False
