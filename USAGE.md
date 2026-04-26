# Usage Guide - Dark Fibre Framework Agreement Engine

Complete guide to using the proposal engine for generating telecom contracts and proposals.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Proposal Levels](#proposal-levels)
3. [User Interface Tour](#user-interface-tour)
4. [Creating Proposals](#creating-proposals)
5. [Advanced Features](#advanced-features)
6. [Saving & Managing Proposals](#saving--managing-proposals)
7. [Examples & Scenarios](#examples--scenarios)
8. [Tips & Best Practices](#tips--best-practices)

---

## Quick Start

### 1. Launch the Application

```bash
# Make sure you're in the project directory and venv is activated
streamlit run app.py
```

Open browser to: **http://localhost:8501**

### 2. Create New Proposal

1. Click **"Create New Proposal"** button
2. Choose proposal level:
   - **L1 Quick**: 8 quick questions, 2 minutes
   - **L2 Standard**: 15 detailed questions, 5 minutes
   - **L3 Dark Fibre**: 35+ questions across 5 phases, 15+ minutes
3. Answer questions one by one
4. Click **"Generate Proposal"** when complete

### 3. View & Download

- Proposal appears in main content area
- Click **"📥 Download as .docx"** to export
- Or copy-paste the Markdown text

---

## Proposal Levels

### Level 1 - Quick Proposal (L1)

**Use when**: You need a rapid 1-page overview for internal use or quick client outreach.

**Time**: ~2 minutes  
**Questions**: 8 fields  
**Output**: 1-2 page proposal

**Fields covered**:
- Client name
- Service description
- Prepared by
- Total cost
- Timeline
- Executive summary tone
- Subsector classification

**Best for**:
- ✓ Quick feasibility checks
- ✓ Internal pre-sales
- ✓ RFI responses

---

### Level 2 - Standard Proposal (L2)

**Use when**: You need a formal, comprehensive proposal for a real opportunity.

**Time**: ~5 minutes  
**Questions**: 15 fields  
**Output**: 3-5 page proposal

**Sections included**:
- Executive Summary
- Scope of Work
- Pricing & Commercial Terms
- Timeline & Milestones
- Assumptions & Exclusions
- Support & Contact

**Best for**:
- ✓ RFP responses
- ✓ Commercial negotiations
- ✓ Client presentations
- ✓ External proposals

---

### Level 3 - Dark Fibre Framework Agreement (L3)

**Use when**: You're negotiating a legal-grade framework agreement for dark fibre services.

**Time**: ~15-20 minutes  
**Questions**: 35+ fields across 5 phases  
**Output**: 20-clause framework agreement

**Phases**:

#### Phase 1: Entity & Administrative
- Party details (Provider/Customer)
- Contact information
- Registration numbers
- Effective date
- Governing law & dispute resolution

#### Phase 2: Wayleave & Access Rights
- Wayleave responsibility (Provider vs Customer)
- High-risk site identification
- Access notice periods
- Equipment ownership & removal terms
- NTP (Network Termination Point) arrangements

#### Phase 3: Commercials & Pricing
- Service model (e.g., "Build + Warranty")
- IRU charge (upfront capital)
- O&M charge (annual operations & maintenance)
- Contract term (months)
- Indexation model (e.g., RPI annual growth)
- Payment terms (net 30, etc.)

#### Phase 4: Liability & Termination
- General liability cap
- Order-specific liability cap
- Property damage caps
- Early termination fees
- Breach cure periods
- Force majeure provisions

#### Phase 5: Technical SLAs
- Target time to repair (TTTR)
- Service credit caps
- Chronic outage thresholds
- First-line testing requirements
- SLA exclusions
- NOC contact details

**Best for**:
- ✓ Dark fibre IRU contracts
- ✓ Framework agreement negotiations
- ✓ Commercial risk analysis
- ✓ Legal due diligence

**Risk Analysis**: L3 includes real-time cross-clause risk detection:
- 🚨 **Critical**: Long-term contract without indexation
- ⚠️ **High**: Provider-led wayleaves, aggressive SLAs
- ⚠️ **Medium**: Over-generous service credits

---

## User Interface Tour

### Main Screen Layout

```
┌─────────────────────────────────────────────────┐
│  🔌 Telecom Proposal Engine                    │
│  L1 Quick | L2 Standard | L3 Dark Fibre         │
└─────────────────────────────────────────────────┘

┌──────────────────┐  ┌──────────────────────────────┐
│                  │  │  Current Question:            │
│   Sidebar        │  │  ========================     │
│   ────────       │  │                               │
│  • New Proposal  │  │  [Question text]              │
│  • My Proposals  │  │                               │
│  • Knowledge Base│  │  📝 [User input field]        │
│  • Help          │  │                               │
│                  │  │  🤖 AI Response:              │
│                  │  │  [AI acknowledgment]          │
│                  │  │  [Optional risk warnings]     │
│                  │  │                               │
│                  │  │  Progress: ▓▓░░░░ (3/8)      │
│                  │  │                               │
│                  │  │  [Next] [Skip] [Back]        │
└──────────────────┘  └──────────────────────────────┘
```

### Key Components

#### Top Bar
- **Level Selector**: Choose L1, L2, or L3
- **Session Info**: Current session ID and client name

#### Input Area
- **Question Display**: Current field to fill
- **Text Input**: Enter your answer
- **Smart Defaults**: Type "defaults" to apply standard values

#### AI Response Area
- **Acknowledgment**: AI confirms your answer
- **Risk Warnings** (L3 only): ⚠️ or 🚨 alerts
- **Clarification** (if needed): Optional follow-up question

#### Progress Indicators
- **Progress Bar**: Visual completion status
- **Field Counter**: "Question 3 of 8"
- **Phase Progress** (L3): "Phase 2 of 5"

#### Action Buttons
- **Next/Continue**: Advance to next field
- **Skip**: Apply defaults and skip
- **Back**: Return to previous field
- **Generate**: Create final proposal (when complete)

#### Right Sidebar (My Proposals)
- **Saved Proposals List**: All generated proposals
- **Client/Date**: Quick identification
- **Actions**: View, Download, Delete

---

## Creating Proposals

### Step-by-Step: L1 Quick Proposal

#### Step 1: Select Level
Click **"L1 Quick"** at top

#### Step 2: Initial Question
**Q1: "Who is this proposal for?"**
```
Enter: Acme Corp
AI Response: "Perfect! Acme Corp it is. 👍"
Click: Next
```

#### Step 3: Service Description
**Q2: "What service are you proposing?"**
```
Enter: Dark Fibre IRU from London to Manchester
AI Response: "Got it! Long-haul dark fibre. Great choice."
Click: Next
```

#### Step 4: Continue Remaining Fields
- Prepared by: [Your name]
- Total cost: £250,000
- Timeline: 6 months from RFS
- Executive tone: Professional
- Subsector: Core Network

#### Step 5: Review
All 8 questions complete. Check answers are correct.

#### Step 6: Generate
Click **"📄 Generate Proposal"**

**Wait**: 5-10 seconds for LLM generation

**Result**: Proposal appears with:
- Header & executive summary
- Service details
- Pricing & timeline
- Contact information

#### Step 7: Save & Download
- Click **"💾 Save Proposal"** to store in history
- Click **"📥 Download as .docx"** for export

---

### Step-by-Step: L3 Dark Fibre Agreement

#### Step 1: Select Level
Click **"L3 Dark Fibre"**

Greeting: "Welcome to the Dark Fibre Framework Agreement Wizard..."

#### Step 2: Phase 1 - Entity & Admin (8 questions)

**Q1: Provider Company Name**
```
Answer: BT Wholesale Limited
```

**Q2: Provider Address**
```
Answer: 81 Newgate Street, London, EC1A 7AJ
```

Continue for:
- Provider company registration number
- Provider notice email
- Customer details (name, address, company no, email)
- Effective date (smart: "last signature" → converts automatically)
- Governing law (default: "English Law, Courts of England and Wales")

#### Step 3: Phase 2 - Wayleave & Access (7 questions)

**Q1: "Who will handle wayleave permissions?"**
```
Options implied:
a) Customer fully responsible
b) Provider assists
c) Provider fully responsible (❌ HIGH RISK FLAG)

Answer: a) Customer fully responsible

AI Response: "Good choice - customer-led wayleaves are standard."
Risk Count: No warnings for this choice
```

**Q2: "High-risk site types?"**
```
Example answer: None identified
Or: Railway crossing (triggers HIGH RISK warning)
Or: Multi-tenant building (triggers HIGH RISK warning)
```

Continue for:
- Access notice days
- Equipment ownership
- Network termination point arrangement
- Equipment removal days

#### Step 4: Phase 3 - Commercials & Pricing (8 questions)

**Q1: "Service model?"**
```
Answer: Build + 12-month Warranty
```

**Q2: "IRU (upfront capital charge)?"**
```
Answer: £150,000
```

**Q3: "O&M (annual operations & maintenance)?"**
```
Answer: £25,000/year
```

**Q4: "Contract term length (months)?"**
```
Answer: 60  [This triggers indexation alert]
```

**Q5: "Indexation model?"** 
```
Answer: RPI annual increase
⚠️ If you said "No indexation" + "60+ months":
    🚨 CRITICAL: "No indexation on long-term contract..."
```

Continue for:
- Payment terms (net 30)
- Pricing structure
- Commercial protections

#### Step 5: Phase 4 - Liability & Termination (6 questions)

**Q1: "General liability cap?"**
```
Answer: £50,000
(Default value - can customize)
```

**Q2: "Order-specific liability?"**
```
Answer: 100% of annual fees for that route
```

Continue for:
- Property damage caps
- Early termination fees
- Breach cure periods (default: 30 days)
- Force majeure termination (default: 180 days)

#### Step 6: Phase 5 - Technical SLAs (6 questions)

**Q1: "Target Time to Repair (TTTR)?"**
```
Answer: 12 hours (standard)
⚠️ If you answer 4-8 hours:
    "Aggressive repair target. Consider adding permit extension."
```

**Q2: "Service credit cap?"**
```
Answer: 50% of annual O&M (standard)
```

Continue for:
- Chronic outage threshold
- First-line testing requirement (Yes/No)
- SLA exclusions
- NOC contact details

#### Step 7: Complete & Generate

When all 35+ fields are complete:
- Session shows: "All phases complete! ✓"
- Click **"📄 Generate Agreement"**
- Wait ~15-20 seconds

**Output**: 20-clause framework agreement with:
- Cover page & signature block
- Parties' details
- Numbered clauses 1-20
- Schedules (Definitions, SLAs)

---

## Advanced Features

### Feature 1: Smart Defaults

Type **"defaults"** to instantly apply UK telecom industry standards:

```text
User: defaults
AI: "✅ Smart defaults applied!"
Defaults applied:
- Wayleave owner: Customer
- Indexation: RPI annual increase
- Payment terms: 30 days
- General liability cap: £50,000
- TTTR: 12 hours
- ... and more
```

### Feature 2: Explain This Clause

Don't understand a field?

```text
Click: 📚 Explain
AI Response: 
  "This field asks who will secure landlord permissions...
   It's critical because wayleaves are the #1 cause of project delays.
   If the Provider handles it, expect 3-9 months and external relief clauses.
   Typical answer: 'Customer responsible' or 'Provider assists'"
```

### Feature 3: Ask the Knowledge Base

Ask off-topic questions using 18 reference documents:

```text
User: "What is TTTR in telecom?"
Click: 🔍 Ask Knowledge Base

AI Response:
  "TTTR (Target Time to Repair) is the maximum time the provider
   has to physically repair a dark fibre cut or fault.
   
   Standard in UK telecom:
   - Normal faults: 12 hours for inland routes
   - Critical sites: 6 hours for metro networks
   - Remote routes: 24-48 hours due to mobilization
   
   This is PHYSICAL repair time, not software uptime SLA."
```

### Feature 4: Risk Analysis (L3 only)

Real-time warnings during wizard:

```
🚨 CRITICAL: No indexation on 60-month contract
   "Your O&M costs will double while revenue stays flat.
    Recommend RPI (annual) or CPI indexation."

⚠️ HIGH: Provider-led wayleaves
   "Highest delivery risk. External Event relief and 
    Long-Stop Date will be added automatically."

⚠️ MEDIUM: Aggressive 8-hour TTTR
   "Mobilizing dig-teams for long routes takes 12+ hours.
    Consider adding permit extension clause."
```

### Feature 5: Navigation

Go back and edit any previous answer:

```
Current: Phase 3, Question 2
Click: Back ← Back ← Back
Result: Phase 2, Question 1 (earlier)
Edit: Change answer
Click: Next →
Continue: Phase resumes
```

### Feature 6: Generate Risk Summary (L3 only)

After completion, generate executive-level risk analysis:

```
Click: 📊 Generate Risk Summary

Output: 1-2 page executive summary covering:
- Critical issues requiring immediate attention
- High-risk commercial terms
- Recommendations for negotiation
- Industry benchmarks & best practices
```

---

## Saving & Managing Proposals

### Auto-Save

Proposals are auto-saved when you click "Generate". Each saved proposal gets:

- **Session ID**: `df_20260324_114640` (unique timestamp)
- **Timestamp**: Date & time created
- **Client name**: Extracted from proposal
- **Status**: Saved to `proposals/` directory as JSON

### View Saved Proposals

1. Scroll to **"My Proposals"** section
2. See list sorted by newest first
3. Each entry shows:
   - Client name
   - Proposal type (L1/L2/L3)
   - Save date & time
   - Subsector

### Load a Saved Proposal

1. In **"My Proposals"**, click on a proposal
2. Full proposal text appears
3. You can:
   - ✓ Read the content
   - ✓ Download as .docx
   - ✓ Copy text
   - ✓ Delete if unwanted

### Download as Word Document

```
Click: 📥 Download as .docx

Result: File downloads to your Downloads folder
Filename: df_20260324_114640.docx
```

Open in Microsoft Word, Google Docs, or any word processor.

### Export/Share

**Option 1: Download .docx**
- Professional format for sharing with clients
- Fully editable in Word

**Option 2: Copy Markdown**
- Copy proposal text from browser
- Paste into Markdown editor (e.g., Notion, Obsidian)
- Paste into email

**Option 3: Print**
- Ctrl+P / Cmd+P in browser
- Save as PDF
- Print directly

### Delete Old Proposals

1. In **"My Proposals"**, click a proposal
2. Scroll to bottom
3. Click **"🗑️ Delete"**
4. Confirm deletion

---

## Examples & Scenarios

### Scenario 1: Quick Proposal to BT Openreach

**Goal**: 15-minute proposal for dark fibre IRU  
**Level**: L1 (Quick)

```
Q1: Who is this for?
A: BT Openreach

Q2: What service?
A: Dark fibre IRU, London-Manchester route (180km)

Q3: Prepared by?
A: Sales Team, Network Partners Ltd

Q4: Total cost?
A: £185,000

Q5: Timeline?
A: 6 months from RFS (Ready for Service)

Q6: Tone?
A: Professional with emphasis on cost-efficiency

Q7: Subsector?
A: Core Network Infrastructure

Q8: Any additional notes?
A: Includes 24/7 NOC support, 12-hour TTTR SLA

[Generate] → 2-page proposal ready in 60 seconds
```

---

### Scenario 2: Formal RFP Response for Vodafone

**Goal**: Comprehensive 5-page proposal matching RFP requirements  
**Level**: L2 (Standard)

```
Q1-Q15: [Answer 15 questions about commercial propositions, 
         scope, timeline, team, support, etc.]

Unique answers for RFP:
- Executive Summary: Link to RFP requirements
- Scope: Point-by-point RFP section compliance
- Commercial: 3-year deal with volume discounts
- Support: Dedicated Vodafone account team
- Timeline: Align with Vodafone go-live date

[Generate] → Professional RFP response, 5 pages
Download as .docx for formal submission
```

---

### Scenario 3: Framework Agreement Negotiation

**Goal**: Legal-grade 20-clause framework agreement  
**Level**: L3 (Dark Fibre)

```
Phase 1: Your company & customer details
- Provider: Fibre Solutions Ltd
- Customer: EE Wholesale
- Effective: 2026-04-01
- Governing Law: English Law

Phase 2: Wayleave & Access Rights
- Wayleave: Customer fully responsible
- Sites: 12 high-risk railway crossings (flags warning)
- Access Notice: 3 business days
- Equipment: Fibre Solutions retains ownership

Phase 3: Commercials (The critical part!)
- Service Model: Build + 24-month warranty
- IRU: £500,000 (upfront)
- O&M: £60,000/year
- Term: 84 months ← Long term!
- Indexation: RPI Annual ← Protects against inflation!
- Payment: Net 30 days

Phase 4: Liability
- General Cap: £75,000
- Order Cap: 100% annual fees (per route)
- Property Damage: £2M per claim / £10M aggregate
- Early Termination: 100% remaining fees
- Cure Period: 30 days
- Force Majeure: 180 days

Phase 5: Technical SLAs
- TTTR: 12 hours (realistic)
- Service Credits: 50% annual O&M (fair)
- Chronic Threshold: 3 failures in 4 weeks
- First-line Testing: Yes
- NOC: +44-208-XXXXXX (24/7)
- Exclusions: Standard (strikes, weather, landowner access)

Risks Detected:
⚠️ HIGH: 84-month term (long commitment)
    Recommendation: Lock indexation rate
⚠️ HIGH: Railway sites (delivery risk)
    Recommendation: Add Programme Relief clause
✓ No critical risks - ready to sign!

[Generate] → 20-clause framework agreement
[Re-negotiate] → Go back, adjust Phase 3 terms, regenerate
```

---

## Tips & Best Practices

### General Tips

1. **Know Your Details**
   - Have client company name, address, contact info ready
   - Know pricing (IRU, O&M, services) in advance
   - Gather any special terms/subsectors

2. **Use "Explain" When Stuck**
   - Don't guess on legal/commercial terms
   - Click 📚 to get AI explanation
   - Understand implications before answering

3. **Defaults Are Safe**
   - Type "defaults" to apply UK telecom industry standards
   - All defaults are market-standard and negotiator-friendly
   - Safe starting point for modifications

4. **Save Everything**
   - Click "Save" after generation
   - Keep history of all proposals for audit trail
   - Reference past proposals for consistency

5. **Risk Warnings Are Important (L3)**
   - 🚨 Red flags must be discussed with legal/commercial
   - ⚠️ Yellow flags should be considered
   - All warnings are backed by market experience

### For Sales Teams

- **Quick Turnaround**: Use L1 for RFI responses (2 min)
- **RFP Responses**: Use L2 for comprehensive proposals (5 min)
- **Follow-ups**: Keep saved proposals for consistency
- **Client Comparison**: Generate L1 for multiple scenarios, compare

### For Legal Teams

- **L3 Agreements**: Comprehensive starting points for negotiation
- **Risk Analysis**: Automated detection of dangerous clause combinations
- **Consistency**: Ensures all agreements follow market standards
- **Documentation**: Full audit trail of all versions generated

### For Commercial Teams

- **Pricing Review**: All financial terms visible in Phase 3
- **Risk Summary**: Understanding deal risks before signature
- **Negotiation**: Quickly regenerate with different terms
- **Benchmarking**: Compare against UK telecom standards

### For Finance Teams

- **Liability Caps**: Clear financial exposure limits
- **Payment Terms**: Net 30 default, customizable
- **Indexation**: Protects revenue in long-term deals
- **Early Term Fees**: Clear exit cost structure

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Enter` | Submit answer (same as clicking Next) |
| `Tab` | Move focus to action buttons |
| `Esc` | Return to main menu (in some screens) |
| `Ctrl+S` (Windows) / `Cmd+S` (Mac) | Save proposal (browser-level) |
| `Ctrl+P` (Windows) / `Cmd+P` (Mac) | Print/Save as PDF |

---

## Keyboard Shortcuts

---

## Common Questions

**Q: Can I edit a proposal after generating it?**  
A: Yes! Load it from "My Proposals", then manually edit the text in the browser or download as .docx to edit in Word.

**Q: How long are generated proposals?**  
A: L1 = 1-2 pages, L2 = 3-5 pages, L3 = 15-25 pages (full agreement)

**Q: Can I use custom documents instead of embedded knowledge base?**  
A: Yes! Add .pdf/.docx files to `rag_data/`, then run `python rag_ingest.py` to re-index.

**Q: What happens if I go back to edit an answer?**  
A: Session resets from that point. Previous answers after that point are cleared, but earlier answers are preserved.

**Q: Can I share proposals with colleagues?**  
A: Yes! Download as .docx or copy-paste Markdown text. Share the file normally.

**Q: Is there an API or programmatic interface?**  
A: Currently UI-only. For API access, see [README.md](README.md) development roadmap.

---

## Support & Feedback

- **Documentation**: [README.md](README.md), [INSTALLATION.md](INSTALLATION.md)
- **GitHub Issues**: [Report bugs](https://github.com/Melochi127/Proposal_Engine_L1-L2-L3-/issues)
- **Discord Community**: [Join discussion]()

---

**Last Updated**: March 2026  
**Maintained by**: Melochi127
