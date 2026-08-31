from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether
)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output" / "pdf" / "Automated_Financial_Intelligence_Project_Scope.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

NAVY = colors.HexColor("#102A43")
BLUE = colors.HexColor("#1F6E8C")
TEAL = colors.HexColor("#2A9D8F")
PALE = colors.HexColor("#EAF3F7")
LIGHT = colors.HexColor("#F6F8FA")
GRAY = colors.HexColor("#52616B")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=30, leading=35, textColor=NAVY, alignment=TA_CENTER, spaceAfter=14))
styles.add(ParagraphStyle(name="CoverSub", parent=styles["Normal"], fontSize=13, leading=19, textColor=GRAY, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="H1x", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=19, leading=24, textColor=NAVY, spaceBefore=12, spaceAfter=10, keepWithNext=True))
styles.add(ParagraphStyle(name="H2x", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=13, leading=17, textColor=BLUE, spaceBefore=9, spaceAfter=6, keepWithNext=True))
styles.add(ParagraphStyle(name="Bodyx", parent=styles["BodyText"], fontSize=9.2, leading=13.1, textColor=colors.HexColor("#263238"), spaceAfter=6))
styles.add(ParagraphStyle(name="Smallx", parent=styles["BodyText"], fontSize=7.4, leading=9.4, textColor=colors.HexColor("#263238")))
styles.add(ParagraphStyle(name="Callout", parent=styles["BodyText"], fontSize=10.4, leading=15, textColor=NAVY, backColor=PALE, borderColor=TEAL, borderWidth=0.8, borderPadding=9, spaceBefore=5, spaceAfter=10))

def p(text, style="Bodyx"):
    return Paragraph(escape(text).replace("\n", "<br/>"), styles[style])

def rich(text, style="Bodyx"):
    return Paragraph(text, styles[style])

def section(title):
    return [Paragraph(title, styles["H1x"])]

def table(headers, rows, widths=None, small=True):
    st = "Smallx" if small else "Bodyx"
    data = [[Paragraph(f"<b>{escape(str(x))}</b>", styles[st]) for x in headers]]
    data += [[Paragraph(escape(str(x)), styles[st]) for x in row] for row in rows]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), NAVY), ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("VALIGN", (0,0), (-1,-1), "TOP"), ("GRID", (0,0), (-1,-1), 0.3, colors.HexColor("#C9D6DF")),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LIGHT]),
        ("LEFTPADDING", (0,0), (-1,-1), 5), ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING", (0,0), (-1,-1), 5), ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]))
    return t

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#C9D6DF")); canvas.line(1.55*cm, 1.35*cm, A4[0]-1.55*cm, 1.35*cm)
    canvas.setFont("Helvetica", 7.5); canvas.setFillColor(GRAY)
    canvas.drawString(1.55*cm, 0.85*cm, "Automated Financial Intelligence Pipeline | Proposed Scope")
    canvas.drawRightString(A4[0]-1.55*cm, 0.85*cm, f"Page {doc.page}")
    canvas.restoreState()

story = []
story += [Spacer(1, 4.1*cm), Paragraph("AUTOMATED FINANCIAL", styles["CoverTitle"]), Paragraph("INTELLIGENCE PIPELINE", styles["CoverTitle"]), Spacer(1, .25*cm), Paragraph("Product Research and Technical Scope Document", styles["CoverSub"]), Spacer(1, 1.2*cm), Paragraph("Proposed early-stage AI fintech project focused on data understanding, verified analytics, and explainable financial insights.", styles["CoverSub"]), Spacer(1, 2.1*cm), Paragraph("Status: Proposed | Version 1.0 | August 2026", styles["CoverSub"]), PageBreak()]

story += section("Executive Summary")
story += [p("This document defines a proposed Automated Financial Intelligence Pipeline. The system is intended to accept financial data, understand its structure, apply deterministic financial and statistical analysis, and present verified findings in a context-aware dashboard. A small AI model is a planned downstream explanation layer, not the primary calculator."),
          Paragraph("Key principle: deterministic computation produces the facts; AI communicates the facts.", styles["Callout"]),
          p("The MVP deliberately focuses on personal-finance transaction data in CSV and Excel/XLSX formats. It will calculate core metrics, identify trends and basic anomalies, produce structured insights, and display them in a dashboard. DOCX, PDF/OCR, business statements, investments, forecasts, and recommendations are future scope."),
          Paragraph("Contents", styles["H2x"]),
          p("1. Context and workflow   2. Research references   3. Gap and proposed system   4. Scope and personalization   5. Architecture   6. AI and team roles   7. Roadmap   8. Evaluation, risks and next steps")]

story += section("1. Project Context and Intended Workflow")
story += [p("The user uploads financial information. The proposed system identifies the file type, extracts data, cleans and normalizes it, checks quality, detects schema and financial context, calculates applicable metrics, performs statistical analysis, detects trends/patterns/anomalies, identifies drivers, creates structured findings, and then optionally generates AI explanations."),
          Paragraph("Pipeline", styles["H2x"]),
          Paragraph("RAW DATA  →  EXTRACTION  →  CLEANING  →  QUALITY CHECK  →  SCHEMA UNDERSTANDING  →  FINANCIAL ANALYSIS  →  STATISTICS  →  TRENDS / PATTERNS / ANOMALIES  →  STRUCTURED FINDINGS  →  AI EXPLANATION (PLANNED)  →  DASHBOARD", styles["Callout"]),
          Paragraph("Critical AI Boundary", styles["H2x"]),
          p("Python, Pandas, NumPy, statistics, and financial rules should calculate and verify numerical findings. For example: income INR 60,000; expenses INR 48,000; savings INR 12,000; savings rate 20%; shopping change +58%. The AI layer may turn only those verified findings into readable language."),
          table(["Why this matters", "Result"], [["Reliability", "Numerical results are reproducible and testable."], ["Debugging", "Each calculation and transformation has a visible stage."], ["Hallucination control", "Language generation follows evidence rather than raw files."], ["Finance validation", "Domain members can review rules and findings."]], [5.2*cm, 11.2*cm], False)]

story += section("2. Existing Projects and Research References")
story += [p("The following are references for individual ideas. They are not claimed as components of this project, and their functionality is not attributed to the proposed system."),
table(["Reference", "What it demonstrates", "Learning / boundary"], [
["Personal Finance Dashboard\nvinzalfaro/personal-finance-dashboard", "Python, Pandas, Plotly, Streamlit and SQL for expenditure analytics, budgeting, inflows/outflows and patterns.", "Useful dashboard reference. Primarily tracking, analytics and visualization; our proposed system aims to add automated interpretation, trends, anomalies and AI explanation."],
["Streamlit Exploratory Analysis\ncamilasbraz/streamlit-exploratory-analysis", "CSV/Excel upload and automated EDA profiling: descriptive statistics, missing values, outliers, correlations, distributions, trends and patterns.", "Shows generic automated data understanding. It does not establish finance-specific schema interpretation or financial intelligence."],
["FG-Data-Profiling\nData-Centric-AI-Community/fg-data-profiling", "Automated Pandas/Spark profiling: type inference, duplicates, univariate/multivariate analysis, correlations, time-series, seasonality, alerts and reports.", "Repository identifies itself as renamed successor to ydata-profiling/data-profiling. General-purpose profiling, not a financial intelligence engine."],
["Financial Statement Analysis\ntenPro4/pandas_financial_statement", "Revenue, expenses, profit, margins, balance sheet, cash flow, trends and segments.", "Identifies possible future financial metrics. It does not mean our system already implements them."],
["S&P 500 Stock Analysis Dashboard\nChennakeshav2003/SP500-stock-analysis-dashboard", "Returns, growth, risk, volatility, correlation, performance and market trends.", "Not our target application; a reference for future financial analytics and visualization techniques."],
["Personal Finance Tracker\nDoshiHarsh/Personal-Finance-Tracker", "Income, expenses, categories, transactions, budgets and balances.", "Reference for records and categorization. Our intended workflow analyzes existing uploaded data rather than manual maintenance of every record."]
], [4.1*cm, 6.0*cm, 6.3*cm])]

story += section("3. Research Gap / Opportunity")
story += [p("The references demonstrate complementary parts: personal-finance analytics and visualization, general EDA, data profiling and quality analysis, financial-statement metrics, market analytics, and financial record management. The proposed system aims to combine selected ideas into a finance-context-aware pipeline."),
          p("This does not claim absolute novelty or that no similar system exists. The proposed differentiation is the traceable sequence from ingestion and quality checks to finance-defined analysis, structured findings, constrained AI explanation, and an analysis-driven dashboard."),
          table(["Project", "Primary purpose", "Automation", "Financial intelligence", "AI explanation", "Our extension"], [
["Personal Finance Dashboard", "Personal finance analytics", "Partial", "Reference", "No stated layer", "Automated findings and explanation"],
["Streamlit EDA", "Generic EDA", "Yes", "No", "No", "Financial-domain layer"],
["FG-Data-Profiling", "Profiling / quality", "Yes", "No", "No", "Context and financial metrics"],
["Statement / market references", "Financial analysis", "Reference", "Reference", "No stated layer", "Validated future modules"],
["Proposed system", "Automated financial intelligence", "Planned", "Planned", "Planned downstream", "Integrated, evidence-first workflow"]
], [2.6*cm, 3.0*cm, 2.1*cm, 3.0*cm, 2.9*cm, 3.3*cm])]

story += section("4. Proposed System and Realistic MVP")
story += [Paragraph("User Journey", styles["H2x"]), p("A user uploads expenses.xlsx. The system extracts data, normalizes fields such as Date, Description, Category, Amount and Income/Expense, checks quality, detects the financial context, runs applicable rules/statistics, and presents verified results. A future AI service converts the findings into constrained explanation cards."),
          table(["Area", "MVP commitment"], [["Inputs", "CSV and Excel/XLSX"], ["Target", "Personal-finance transaction data"], ["Core fields", "Date, description, category, amount, income/expense"], ["Outputs", "Income, expenses, savings, savings rate, category breakdown, monthly trends, top categories, basic anomalies, structured insights and dashboard"], ["AI", "Planned explanation of verified findings; model training follows a working analytics pipeline"], ["Deferred", "DOCX/PDF/OCR, business statements, investment analytics, forecasts and recommendations"]], [4.0*cm, 12.4*cm], False),
          Paragraph("Illustrative Finding Contract", styles["H2x"]), p("A structured finding should include values, period, supporting fields, the rule or method version, and review status. Illustrative examples - not implemented output or research results - include income 60,000, expenses 48,000, savings 12,000, savings rate 20%, major trends, anomalies, expense drivers and risk flags."),
          Paragraph("An anomaly means a material deviation from expected historical behavior. It does not automatically mean fraud, an error, or a bad transaction.", styles["Callout"])]

story += section("5. Financial Analysis Scope and Personalization")
story += [table(["Phase 1 / Core", "Phase 2 / Advanced - planned"], [["Total income; total expenses; net savings; savings rate; expense distribution; category-wise spending; monthly comparisons; income-versus-expense trends; largest categories; recurring expenses; basic anomalies; period-over-period changes.", "Trend detection; seasonality; correlation; expense drivers; cash flow; financial ratios; profitability/margins; business financial analysis; investment performance; risk indicators; forecasting."]], [8.2*cm, 8.2*cm], False),
          p("Technical interpretation: core metrics are calculated from cleaned records and explicit aggregation rules. Advanced methods require clear input requirements and validation. Correlation shows measures moving together; it does not prove causation."),
          p("Finance/business interpretation: core analysis answers where money is going, whether spending is changing, whether income covers expenses, and which activity needs review."),
          Paragraph("Analysis-Driven Dashboard Generation", styles["H2x"]),
          table(["Detected context", "Dashboard focus"], [["Personal finance", "Income, expenses, savings, debt, cash flow and spending patterns"], ["Business financial data", "Revenue, COGS, gross profit, operating expenses, net profit, margins and cash flow"], ["Investment data", "Portfolio value, returns, allocation, volatility, performance and risk"]], [4.5*cm, 11.9*cm], False),
          p("The dashboard should be dynamic based on detected financial context, not generic. Data structure and validated analysis determine which insight cards and visualizations are relevant.")]

story += section("6. Technical Architecture")
story += [Paragraph("USER → FRONTEND → UPLOAD API → FILE PROCESSING → NORMALIZATION + QUALITY CHECKS → SCHEMA / CONTEXT DETECTION → FINANCIAL ANALYSIS ENGINE → STRUCTURED INSIGHT ENGINE → DASHBOARD + REPORTING", styles["Callout"]),
          table(["Component", "Technical responsibility", "Business purpose"], [["Frontend", "File selection, feedback and dashboard", "Simple path to insights"], ["Upload API", "Receipt, metadata, type/size checks", "Controlled ingestion"], ["File processing", "CSV/XLSX parse; DOCX/PDF planned", "Usable source records"], ["Normalization", "Dates, signs, currencies/formats, labels and quality issues", "Comparable and trustworthy data"], ["Schema detector", "Identify fields and financial context", "Select relevant analysis"], ["Analysis engine", "Metrics, rules and aggregations", "Traceable financial facts"], ["Insight engine", "Trends, outliers, patterns and drivers", "Prioritize meaningful changes"], ["AI service - planned", "Constrained text from findings", "Readable explanation"], ["Storage if needed", "Secure data/findings/rule versions", "Persistence, privacy and auditability"]], [3.2*cm, 7.2*cm, 6.0*cm]),
          p("Security is required before production: protected transport, restricted access, retention and deletion rules, safe logging, and a storage design appropriate for sensitive financial information.")]

story += section("7. AI/ML Scope and Team Responsibilities")
story += [Paragraph("Proposed AI Scope", styles["H2x"]), p("The small AI model is a future design decision, to be explored in Google Colab only after deterministic analysis creates stable structured findings. Options may include a small instruction-tuned language model, compact transformer fine-tuning, or parameter-efficient fine-tuning such as LoRA/QLoRA. No completed training or final model choice is assumed."),
          table(["AI input", "AI output"], [["Metric, change, period, category, severity, supporting statistics, finding and allowed wording constraints", "Human-readable explanation or insight card that remains faithful to those findings"]], [8.2*cm, 8.2*cm], False),
          Paragraph("Financial Decision Support vs Financial Advice", styles["H2x"]), p("The initial system is for analytics, insights, monitoring, reporting and decision support. It is not professional financial advice, guaranteed investment recommendations, or guaranteed profit/loss predictions. Any future recommendation layer requires finance-domain validation and careful framing."),
          table(["Finance-domain team", "Technical team", "AI layer"], [["Define metrics/ratios; validate interpretations; define thresholds; decide useful insights; review findings.", "Ingestion, extraction, cleaning, transformation, analytics, statistics, API/backend, dashboard, security and testing.", "Summarization, explanation and natural-language generation only; no primary calculations or unverified advice."]], [5.45*cm, 5.45*cm, 5.45*cm])]

story += section("8. Development Roadmap")
story += [table(["Phase", "Objective", "Expected output", "Success criterion"], [["1", "Requirements", "MVP contract and finance definitions", "Scope/exclusions agreed"], ["2", "Sample data", "Permissioned test data and edge cases", "Coverage documented"], ["3", "CSV ingestion", "Parser and upload flow", "Clear success/failure handling"], ["4", "Excel ingestion", "XLSX extraction", "Required fields extract correctly"], ["5", "DOCX extraction", "Future prototype", "Only after tabular MVP stability"], ["6", "Cleaning", "Normalized schema and quality report", "Traceable transformations"], ["7", "Core analytics", "MVP metrics engine", "Finance review confirms calculations"], ["8", "Trends/anomalies", "Configured insight methods", "Reviewable, useful findings"], ["9", "Structured insights", "Versioned findings contract", "Dashboard works without AI"], ["10", "Dashboard", "Personal-finance MVP", "Users understand results"], ["11", "AI training", "Colab evaluation experiment", "Faithfulness target met"], ["12", "AI integration", "Guarded explanation service", "Text traceable to findings"], ["13", "Validation", "Test and review results", "Release criteria passed"], ["14", "Deployment", "Controlled pilot/production", "Monitoring/support ready"]], [1.1*cm, 3.5*cm, 6.0*cm, 5.8*cm])]

story += section("9. Evaluation, Limitations and Risks")
story += [table(["Evaluation area", "Criteria"], [["Data pipeline", "Ingestion success rate; extraction accuracy; cleaning accuracy"], ["Analytics", "Metric correctness; trend detection accuracy; anomaly quality; financial-rule correctness"], ["AI", "Faithfulness; hallucination rate; explanation quality; readability"], ["Dashboard", "Usability; metric relevance; personalization; clarity"], ["End-to-end", "Upload → analysis → insight → explanation → dashboard"]], [4.2*cm, 12.2*cm], False),
          Paragraph("Known Limitations", styles["H2x"]), p("Financial data may be incomplete, inconsistent or ambiguously labeled. Conclusions depend on data quality and selected rules. Different terminology can break automatic mapping. AI explanations can still be wrong. The system must show uncertainty, avoid unsupported claims, and protect sensitive data."),
          table(["Risk", "Initial mitigation"], [["Technical variability", "Narrow CSV/XLSX MVP and clear unsupported-format feedback"], ["Financial interpretation", "Finance review and versioned rules"], ["AI hallucination", "Structured-input-only AI and output checks"], ["Privacy", "Least access, protected storage/transit, retention/deletion policy"], ["Scope creep", "Protect the MVP boundary"], ["Scalability", "File limits, async jobs and performance tests"]], [5.0*cm, 11.4*cm], False)]

story += section("10. Future Scope and What We Should Build First")
story += [Paragraph("What We Should Build First", styles["H2x"]), Paragraph("CSV / EXCEL  →  CLEANING  →  CORE FINANCIAL METRICS  →  TREND DETECTION  →  BASIC ANOMALY DETECTION  →  STRUCTURED FINDINGS  →  DASHBOARD  →  AI EXPLANATION", styles["Callout"]),
          p("AI model training should come after the deterministic pipeline has a working, testable structured output. This gives the team an evidence base for evaluating whether generated explanations are accurate and useful."),
          Paragraph("Future Scope - Planned", styles["H2x"]), p("Possible later extensions include PDF bank statements, OCR, bank API integrations, multiple accounts, business and investment analysis, forecasting, budget recommendations, cash-flow forecasting, financial-health scoring, advanced anomaly detection, multi-user support, cloud deployment, role-based access, secure document storage, explainable AI, and feedback-driven model improvement."),
          Paragraph("Final Vision", styles["H2x"]), p("A user uploads financial data without needing Python, Pandas, Seaborn, Matplotlib, statistics or SQL. The system handles analytical work and returns a financial overview, important metrics, trends, patterns, anomalies, drivers, explanations, visualizations and personalized insights. The first success is a trustworthy, narrow CSV/XLSX personal-finance MVP.")]

story += section("References")
story += [rich("1. <link href='https://github.com/vinzalfaro/personal-finance-dashboard' color='#1F6E8C'>https://github.com/vinzalfaro/personal-finance-dashboard</link><br/>2. <link href='https://github.com/camilasbraz/streamlit-exploratory-analysis' color='#1F6E8C'>https://github.com/camilasbraz/streamlit-exploratory-analysis</link><br/>3. <link href='https://github.com/Data-Centric-AI-Community/fg-data-profiling' color='#1F6E8C'>https://github.com/Data-Centric-AI-Community/fg-data-profiling</link><br/>4. <link href='https://github.com/tenPro4/pandas_financial_statement' color='#1F6E8C'>https://github.com/tenPro4/pandas_financial_statement</link><br/>5. <link href='https://github.com/Chennakeshav2003/SP500-stock-analysis-dashboard' color='#1F6E8C'>https://github.com/Chennakeshav2003/SP500-stock-analysis-dashboard</link><br/>6. <link href='https://github.com/DoshiHarsh/Personal-Finance-Tracker' color='#1F6E8C'>https://github.com/DoshiHarsh/Personal-Finance-Tracker</link>"),
          Paragraph("Final quality check: reference systems and the proposed system are clearly separated; advanced work is marked planned; AI is not the calculator; finance ownership is defined; the MVP is constrained; risks and limitations are explicit.", styles["Callout"])]

doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=1.55*cm, leftMargin=1.55*cm, topMargin=1.45*cm, bottomMargin=1.7*cm, title="Automated Financial Intelligence Pipeline")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
