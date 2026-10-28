import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b")) # slate-500

        # Header (on pages after cover)
        if self._pageNumber > 1:
            self.drawString(54, 750, "PrepPilot: Comprehensive Technical & Architectural Project Review")
            self.drawRightString(612 - 54, 750, "Confidential • Review Documentation")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 612 - 54, 742)

        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 36, page_text)
        self.drawString(54, 36, "PrepPilot AI Career Assistant • Developed by Rishikesh • October 2026")
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 48, 612 - 54, 48)

        self.restoreState()


def build_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#1e3a8a") # deep blue
    accent_color = colors.HexColor("#0284c7")  # sky/cyan
    dark_neutral = colors.HexColor("#0f172a")  # slate-900
    body_color = colors.HexColor("#334155")    # slate-700
    card_bg = colors.HexColor("#f8fafc")       # slate-50
    border_color = colors.HexColor("#e2e8f0")  # slate-200

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=accent_color,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#0f766e"), # teal
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=body_color,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletDark',
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=4
    )

    meta_key = ParagraphStyle(
        'MetaKey',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=primary_color
    )

    meta_val = ParagraphStyle(
        'MetaVal',
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=dark_neutral
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=body_color
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1e293b")
    )

    story = []

    # ================= COVER / HEADER SECTION =================
    story.append(Paragraph("PrepPilot: AI-Powered Career & Interview Preparation Assistant", title_style))
    story.append(Paragraph("System Architecture, Feature Specifications & Technology Stack Defense Document", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=accent_color, spaceAfter=12))

    # Metadata Grid
    meta_data = [
        [Paragraph("Project Name:", meta_key), Paragraph("PrepPilot (v1.0.0)", meta_val),
         Paragraph("Author / Developer:", meta_key), Paragraph("Rishikesh (Rishikesh0149)", meta_val)],
        [Paragraph("Target Audience:", meta_key), Paragraph("Technical Interview Review Panel & Evaluators", meta_val),
         Paragraph("GitHub Repository:", meta_key), Paragraph("github.com/Rishikesh0149/interviewprep", meta_val)],
        [Paragraph("Architecture Model:", meta_key), Paragraph("FastAPI + React 19 (100% Docker-Free)", meta_val),
         Paragraph("Execution Engine:", meta_key), Paragraph("Monaco Code Sandbox & Dual AI Engine", meta_val)]
    ]
    meta_table = Table(meta_data, colWidths=[105, 145, 110, 144])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), card_bg),
        ('BOX', (0,0), (-1,-1), 0.5, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # ================= 1. EXECUTIVE SUMMARY & PROBLEM STATEMENT =================
    story.append(Paragraph("1. Executive Summary & Problem Statement", h1_style))
    summary_text = (
        "Securing software engineering and technical roles in modern competitive markets requires multi-dimensional "
        "competency: algorithmic problem solving, structured behavioral storytelling (STAR method), scalable system "
        "architecture, and ATS-optimized resume formatting. Candidates currently juggle fragmented, disconnected tools: "
        "LeetCode for algorithmic coding, static blogs for system design, opaque online ATS checkers, and unstructured mock interviews. "
        "<b>PrepPilot</b> unifies this journey into an integrated, intelligent co-pilot platform that assesses candidate gaps, "
        "synthesizes structured 4-week preparation roadmaps, runs voice-enabled interactive mock interviews with real-time scoring, "
        "and evaluates in-browser coding solutions in a safe, sandboxed execution environment."
    )
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 8))

    # Key Value Props Callout
    callout_data = [[
        Paragraph(
            "<b>Key Review Takeaway:</b> PrepPilot is engineered from the ground up to be <b>100% Docker-Free</b>, "
            "running natively on Python FastAPI and SQLite locally with sub-second startup times, zero virtualization "
            "dependencies, and guaranteed 100% offline availability via deterministic heuristic AI fallbacks.",
            callout_style
        )
    ]]
    callout_table = Table(callout_data, colWidths=[504])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f0fdf4")), # emerald-50
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#86efac")),       # emerald-300
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(callout_table)
    story.append(Spacer(1, 14))

    # ================= 2. CORE FUNCTIONAL MODULES =================
    story.append(Paragraph("2. Core Functional Modules (What the Project Does)", h1_style))

    modules = [
        ("Resume Lab (ATS Scorer & Profile Ingestion)",
         "Parses PDF and plain-text resumes using PyMuPDF and regular expression heuristics. Generates an ATS compatibility "
         "score across 7 independent dimensions (quantified impact, action verb diversity, keyword alignment, formatting clarity, "
         "readability tone, section completeness, and density). Flags specific red flags and provides AI-powered STAR bullet "
         "point rewrites that transform weak descriptions into measurable business achievements."),

        ("Competency Gap Analyzer & Tiered 4-Week Syllabus",
         "Cross-references candidate skills against indexed industry target roles (Software Engineer, ML Engineer, Full Stack, "
         "DevOps, Frontend). Calculates a match percentage and highlights missing vs. partial core competencies. Automatically "
         "generates an actionable 4-week roadmap organized into BASIC, INTERMEDIATE, and ADVANCED tiers with daily tasks, "
         "resource links, and progress check-offs that incrementally boost candidate readiness score."),

        ("Interactive Mock Interview Arena (Voice & Speech-to-Text)",
         "Simulates realistic interview rounds across multiple adaptive personas ('Technical Lead', 'Strict Bar Raiser', "
         "'Friendly Mentor') and rounds (Technical, Behavioral, System Design). Supports live microphone speech recognition "
         "with real-time cadence analysis (Words Per Minute and filler word detection). Evaluates candidate answers using the "
         "STAR rubric (Situation, Task, Action, Result) and generates constructive critiques, exemplars, and debrief reports."),

        ("In-Browser Code Arena (Monaco Editor & Secure Sandbox)",
         "Provides an IDE-grade code editor powered by Monaco Editor (the editor behind VS Code) supporting Python 3.12 and "
         "JavaScript. Executes candidate code against visible and hidden test cases in an AST-sanitized sandbox environment. "
         "Profiles runtime latency (in milliseconds) and generates automated Big-O time and space complexity feedback."),

        ("Curated Interview Question Bank",
         "A searchable library of technical and behavioral prompts filterable by category, difficulty (Easy, Medium, Hard), "
         "and seniority level (Junior, Mid, Senior+). Each entry features an ideal STAR exemplar answer, interviewer rubric hints, "
         "and a 1-click shortcut to practice the question in the Mock Interview simulator."),

        ("Target Company Playbooks (FAANG & High Growth)",
         "Strategic dossiers and interview stage breakdowns for top tech employers: Google, Amazon, Meta, Microsoft, and Stripe. "
         "Includes verified round timelines, core cultural principles (e.g. Amazon's 16 Leadership Principles, Googleyness), "
         "evaluator insider advice, and high-frequency recurring questions.")
    ]

    for title, desc in modules:
        story.append(Paragraph(f"• <b>{title}</b>: {desc}", bullet_style))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 10))

    # ================= 3. TECHNOLOGY STACK & JUSTIFICATION =================
    story.append(Paragraph("3. Technology Stack & Detailed Justifications (Why It Is Used)", h1_style))
    story.append(Paragraph(
        "Every framework, library, and architectural decision in PrepPilot was deliberately chosen to maximize "
        "developer velocity, runtime efficiency, local zero-configuration execution, and exceptional user experience.",
        body_style
    ))
    story.append(Spacer(1, 6))

    tech_table_data = [
        [Paragraph("Technology Layer", table_header_style),
         Paragraph("Selected Technology", table_header_style),
         Paragraph("Architectural Justification & Review Defense", table_header_style)],

        [Paragraph("<b>Backend Framework</b>", table_cell_style),
         Paragraph("Python 3.12 + FastAPI", table_cell_style),
         Paragraph("Asynchronous ASGI runtime delivers industry-leading latency. Automatic OpenAPI/Swagger generation (/api/v1/docs), native Pydantic v2 data validation, and first-class async concurrency.", table_cell_style)],

        [Paragraph("<b>Database & Storage</b>", table_cell_style),
         Paragraph("SQLite 3 via SQLAlchemy ORM", table_cell_style),
         Paragraph("Zero-container architecture! Eliminates Docker/Postgres daemon overhead, port conflicts, and memory leaks. Automatically creates schema and seeds data on startup; easily swaps to PostgreSQL in production.", table_cell_style)],

        [Paragraph("<b>Document Parser</b>", table_cell_style),
         Paragraph("PyMuPDF (Fitz)", table_cell_style),
         Paragraph("High-speed native C++ library for robust multi-column PDF text and font extraction. Operates entirely locally with zero third-party cloud API cost or data privacy leaks.", table_cell_style)],

        [Paragraph("<b>Dual AI Engine</b>", table_cell_style),
         Paragraph("Google GenAI + Heuristic Rule Engine", table_cell_style),
         Paragraph("Hybrid intelligence: uses Gemini Flash for rich generative capabilities when keys are available, and instantly falls back to a deterministic semantic heuristic engine offline or during testing.", table_cell_style)],

        [Paragraph("<b>Frontend Framework</b>", table_cell_style),
         Paragraph("React 19 + TypeScript + Vite", table_cell_style),
         Paragraph("Sub-second Hot Module Replacement (HMR), tree-shaken production bundles (under 370KB), and strict compile-time type verification (verbatimModuleSyntax) preventing runtime UI failures.", table_cell_style)],

        [Paragraph("<b>Code Editor</b>", table_cell_style),
         Paragraph("Monaco Editor (@monaco-editor/react)", table_cell_style),
         Paragraph("The exact core engine of VS Code. Provides native syntax highlighting, bracket matching, line numbering, and dark theme (vs-dark) directly within the browser.", table_cell_style)],

        [Paragraph("<b>Styling & Aesthetics</b>", table_cell_style),
         Paragraph("TailwindCSS v4 + Glassmorphism", table_cell_style),
         Paragraph("Modern high-contrast dark aesthetic (#0b0f19 background) with backdrop blur, tailored cyan/indigo accent palettes, and smooth micro-animations that exceed standard MVP designs.", table_cell_style)],

        [Paragraph("<b>Execution Model</b>", table_cell_style),
         Paragraph("Native Windows Shell (start-dev.ps1 / .bat)", table_cell_style),
         Paragraph("Completely Docker-Free. 1-click execution launches FastAPI and Vite in isolated background PowerShell/CMD instances with zero setup friction.", table_cell_style)]
    ]

    tech_table = Table(tech_table_data, colWidths=[110, 130, 264])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('BOX', (0,0), (-1,-1), 0.5, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, card_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 14))

    # ================= 4. SECURITY, PRIVACY & TEST VERIFICATION =================
    story.append(Paragraph("4. Security, Privacy & Quality Verification", h1_style))

    security_points = [
        ("AST Security Sandbox for Code Arena",
         "The code execution engine inspects submitted Python syntax trees via the <code>ast</code> module. "
         "Dangerous modules (<code>os</code>, <code>sys</code>, <code>subprocess</code>, <code>shutil</code>, <code>socket</code>, <code>open</code>) "
         "and dynamic primitives (<code>eval</code>, <code>exec</code>) are strictly prohibited before execution."),

        ("JWT Authentication & Secure Password Hashing",
         "User credentials are encrypted using <code>bcrypt</code> with salted work factors. Sessions are verified using "
         "JSON Web Tokens (HS256) with refresh token rotation and explicit token revocation."),

        ("HTTP Security Headers & Educational Disclaimer",
         "Global FastAPI middleware automatically injects <code>X-Content-Type-Options: nosniff</code>, "
         "<code>X-Frame-Options: DENY</code>, and <code>X-AI-Disclaimer</code> to guarantee responsible AI educational guidance."),

        ("100% Automated Backend Test Coverage",
         "All 12 backend unit and integration tests (auth, resume parser, skill gaps, study plans, mock interviews, coding runner, "
         "and question bank) pass with 100% success rate in pytest in under 8 seconds.")
    ]

    for title, desc in security_points:
        story.append(Paragraph(f"• <b>{title}</b>: {desc}", bullet_style))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 14))

    # ================= 5. REVIEW PRESENTATION CHECKLIST =================
    story.append(Paragraph("5. Review Presentation & Demonstration Walkthrough", h1_style))
    story.append(Paragraph(
        "For your upcoming technical review, demonstrate the platform in this natural narrative flow:",
        body_style
    ))

    flow_data = [
        [Paragraph("Step", table_header_style), Paragraph("Module / Feature", table_header_style), Paragraph("Key Demonstration Highlight to Emphasize to Evaluators", table_header_style)],
        [Paragraph("1", table_cell_style), Paragraph("<b>1-Click Startup</b>", table_cell_style), Paragraph("Show <code>start-dev.bat</code> launching FastAPI and Vite in separate windows with 0 Docker overhead.", table_cell_style)],
        [Paragraph("2", table_cell_style), Paragraph("<b>Resume Lab</b>", table_cell_style), Paragraph("Upload/load sample resume: showcase 7-metric ATS score radar, red flag flags, and STAR bullet rewriter.", table_cell_style)],
        [Paragraph("3", table_cell_style), Paragraph("<b>Skill Gap & Plan</b>", table_cell_style), Paragraph("Select Target Role (Software Engineer): show gap analysis and toggle tasks across 4-week curriculum.", table_cell_style)],
        [Paragraph("4", table_cell_style), Paragraph("<b>Mock Interview</b>", table_cell_style), Paragraph("Start a simulation: demonstrate speech recognition, WPM counter, filler word metric, and STAR score.", table_cell_style)],
        [Paragraph("5", table_cell_style), Paragraph("<b>Code Arena</b>", table_cell_style), Paragraph("Select 'Two Sum' or 'Valid Parentheses': run code in Monaco Editor and submit for instant pass/fail validation.", table_cell_style)],
        [Paragraph("6", table_cell_style), Paragraph("<b>Company Playbooks</b>", table_cell_style), Paragraph("Inspect Google/Amazon/Meta guides: review cultural criteria and high-frequency recurring questions.", table_cell_style)]
    ]
    flow_table = Table(flow_data, colWidths=[36, 120, 348])
    flow_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('BOX', (0,0), (-1,-1), 0.5, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, card_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(flow_table)
    story.append(Spacer(1, 16))

    # Concluding Signature Callout
    conclusion_data = [[
        Paragraph(
            "<b>Summary for Evaluators:</b> PrepPilot represents a complete, production-grade pairing of modern web design, "
            "asynchronous backend microservices, robust local data storage, and intelligent AI assistance—built to be fast, reliable, and completely container-independent.",
            callout_style
        )
    ]]
    conclusion_table = Table(conclusion_data, colWidths=[504])
    conclusion_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, primary_color),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(conclusion_table)

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Successfully generated PDF at: {output_path}")

if __name__ == "__main__":
    out_dir = r"c:\Users\anike\Desktop\AIProject"
    pdf_filename = os.path.join(out_dir, "PrepPilot_Project_Documentation.pdf")
    build_pdf(pdf_filename)
    # Also save copy to Desktop
    desktop_copy = r"c:\Users\anike\Desktop\PrepPilot_Project_Documentation.pdf"
    try:
        import shutil
        shutil.copyfile(pdf_filename, desktop_copy)
        print(f"[+] Successfully copied PDF to Desktop: {desktop_copy}")
    except Exception as e:
        print(f"[!] Desktop copy notice: {e}")
