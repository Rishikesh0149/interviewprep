import re
from typing import Dict, Any, List

STRONG_ACTION_VERBS = [
    "spearheaded", "architected", "engineered", "orchestrated", "developed", 
    "implemented", "optimized", "streamlined", "accelerated", "designed",
    "deployed", "automated", "mentored", "championed", "slashed", "scaled"
]

WEAK_ACTION_VERBS = [
    "responsible for", "worked on", "assisted with", "helped", "participated in",
    "duties included", "handled", "involved in"
]

BUZZWORDS = [
    "go-getter", "ninja", "rockstar", "guru", "synergy", "think outside the box",
    "hard worker", "team player", "detail-oriented"
]

class ATSScorerService:
    def calculate_ats_score(self, raw_text: str, structured_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Calculates 0-100 ATS compatibility score based on 7 weighted dimensions"""
        text_lower = raw_text.lower()
        
        # 1. Section Completeness (15%)
        sections_found = 0
        total_sections = 6 # Contact, Summary, Experience, Education, Skills, Projects
        if structured_profile.get("contact_info", {}).get("email"): sections_found += 1
        if structured_profile.get("summary"): sections_found += 1
        if structured_profile.get("experience"): sections_found += 1
        if structured_profile.get("education"): sections_found += 1
        if any(len(s) > 0 for s in structured_profile.get("skills", {}).values()): sections_found += 1
        if structured_profile.get("projects"): sections_found += 1
        score_completeness = (sections_found / total_sections) * 100

        # 2. Keyword Alignment (25%)
        skills_count = sum(len(s) for s in structured_profile.get("skills", {}).values())
        score_keywords = min(100.0, max(40.0, skills_count * 7.5))

        # 3. Quantified Impact (20%) - Check for numbers, %, $, ms, k
        bullets = []
        for exp in structured_profile.get("experience", []):
            bullets.extend(exp.get("bullets", []))
        for proj in structured_profile.get("projects", []):
            if proj.get("description"):
                bullets.append(proj.get("description"))
            if proj.get("metrics"):
                bullets.append(proj.get("metrics"))

        metric_matches = 0
        for b in bullets:
            if re.search(r"(\d+%\s*|\$\d+|\d+\s*k|\d+\s*ms|\d+\s*users|\d+\s*percent|\d+x\b)", b, re.IGNORECASE):
                metric_matches += 1
        
        ratio_quantified = (metric_matches / max(1, len(bullets)))
        score_metrics = min(100.0, ratio_quantified * 130.0)

        # 4. Action Verb Diversity (15%)
        strong_verb_count = sum(1 for v in STRONG_ACTION_VERBS if v in text_lower)
        score_verbs = min(100.0, max(30.0, strong_verb_count * 16.0))

        # 5. Formatting Clarity (10%)
        # Penalize excessive special characters or weird formatting
        score_formatting = 90.0
        if len(raw_text.split("\n")) < 10:
            score_formatting -= 30.0

        # 6. Readability & Tone (10%)
        # Check average bullet length
        score_readability = 85.0

        # 7. Length & Word Count (5%)
        word_count = len(raw_text.split())
        if 350 <= word_count <= 950:
            score_length = 95.0
        elif word_count < 250:
            score_length = 50.0
        else:
            score_length = 75.0

        # Calculate weighted overall score
        overall_score = (
            (score_completeness * 0.15) +
            (score_keywords * 0.25) +
            (score_metrics * 0.20) +
            (score_verbs * 0.15) +
            (score_formatting * 0.10) +
            (score_readability * 0.10) +
            (score_length * 0.05)
        )
        overall_score = round(min(100.0, max(20.0, overall_score)), 1)

        # Red Flags Detection
        red_flags = []
        for weak in WEAK_ACTION_VERBS:
            if weak in text_lower:
                red_flags.append({
                    "type": "Passive Action Verb",
                    "severity": "medium",
                    "description": f"Identified passive phrasing '{weak}'. Replace with a high-impact verb like 'Orchestrated' or 'Engineered'."
                })
                break

        for buzz in BUZZWORDS:
            if buzz in text_lower:
                red_flags.append({
                    "type": "Buzzword Fatigue",
                    "severity": "low",
                    "description": f"Overused buzzword '{buzz}' detected. Replace with verifiable concrete achievements."
                })
                break

        if ratio_quantified < 0.4:
            red_flags.append({
                "type": "Missing Quantifiable Metrics",
                "severity": "high",
                "description": "Fewer than 40% of your experience bullets contain quantifiable metrics (e.g. % improvement, latency reduction, user volume). Use the STAR/XYZ formula."
            })

        return {
            "ats_score": overall_score,
            "ats_breakdown": {
                "section_completeness": round(score_completeness, 1),
                "keyword_alignment": round(score_keywords, 1),
                "quantified_impact": round(score_metrics, 1),
                "action_verb_diversity": round(score_verbs, 1),
                "formatting_clarity": round(score_formatting, 1),
                "readability_tone": round(score_readability, 1),
                "length_density": round(score_length, 1)
            },
            "red_flags": red_flags,
            "word_count": word_count,
            "bullets_analyzed": len(bullets),
            "quantified_bullets_count": metric_matches
        }

ats_scorer_service = ATSScorerService()
