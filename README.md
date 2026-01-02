# Wedding Planning Agent

**What happens when you treat wedding planning like a data platform problem?**

## The Story

I got engaged and immediately drowned in vendor PDFs. Sixty-eight of them. Each restaurant had different formats, pricing structures, and dietary accommodation language. I found myself with 15 browser tabs open, three spreadsheets going, and absolutely no confidence in my decisions.

Sound familiar? That's when the product designer in me kicked in.

I realized wedding planning has the same challenges I see in analytics platforms: **fragmented data sources, unclear dependencies, and users who need to make high-stakes decisions without transparent information**. So I designed a system to fix it.

This is a case study in **systems-level design thinking**—treating a personal problem as a platform challenge, then building something others can actually use.

## The Problem (The Real One)

Wedding planning isn't just stressful—it's a **terrible user experience**:

- **Information is scattered everywhere**: PDFs, emails, screenshots, scribbled notes. Zero semantic structure.
- **Context switching is brutal**: You're constantly jumping between discovery ("what venues exist?"), analysis ("which fits my budget?"), and execution ("how do I email them?")
- **Dependencies are invisible**: Choosing a menu affects your beverage budget, which affects guest count, which affects... you get it. But nothing shows you this.
- **You can't trust the data**: Is $12,500 for catering reasonable? No idea. The vendor says it's competitive. Your budget says it's too high. Who's right?
- **Every decision feels risky**: Because you lack observability into how your choices compound.

I was planning a small 20-guest wedding in Boston with a $6,700 budget. It shouldn't be this hard.

## What I Built

I designed a **unified planning and analytics system** that treats wedding data like... well, data.

**Three core principles guided the design:**

### 1. Minimize Context Switching

People shouldn't need to jump between tools to make one decision. I created workflows that keep you in one mental model:
- **Discover** vendors → **Analyze** fit → **Execute** communication—all in one place
- Templates live next to examples (see it, use it, adapt it)
- Documentation shows up exactly when you need it, not buried in a separate wiki

### 2. Make Dependencies Visible

Bad things happen when you can't see how your decisions connect:
- I built **real-time budget tracking** that updates as you make choices
- **Dependency mapping** shows you: pick this menu → need X beverages → costs Y → leaves Z remaining
- **Data lineage**: You can trace any recommendation back to the source vendor PDF

### 3. Build Trust Through Transparency

Black-box AI recommendations are useless when you're spending thousands of dollars:
- Every vendor gets a **fit score with reasoning**: "Within budget ($8,500 ≤ $10,000); Matches dietary needs: vegetarian, gluten-free"
- Market analysis shows you **where prices stand** compared to competitors
- The system shows its work—no magic, just logic you can interrogate

## Design Approach

### The Mental Model

I organized everything around how people actually think about planning:
- Audit trail of all planning decisions and their impacts

### 2. System Architecture

The platform is organized around clear practitioner mental models:

```
examples/          # "See how someone else did this"
  ├── planning/    # Real wedding organized by category (venue, photos, music)
  ├── analysis/    # Budget scenarios ($5K vs $6.7K—because plans change!)
  ├── data/        # All the messy vendor PDFs, now organized
  └── outputs/     # Generated recommendations

templates/         # "Now you try"
  ├── venue_and_catering/
  ├── photography/
  ├── music/
  └── budget/

docs/              # "Here's what to know"
```

**The pattern**: See it. Try it. Learn it. No context switching required.

### The Key Decisions (And Why They Matter)

#### Decision 1: Semantic Modeling Over File Chaos

I built a data layer that treats vendor information as structured entities:
- **Venue** has **Price**, **Capacity**, **Dietary Options**, **Location**
- **Menu Item** connects to **Dietary Accommodations** and **Guest Needs**
- **Budget Allocation** links to **Actual Spend** and **Remaining Budget**

Why this matters: You can now ask questions like "show me venues under $8K that accommodate gluten-free guests" without manually re-reading 68 PDFs. The system knows the relationships.

#### Decision 2: Explainable Recommendations, Not AI Magic

Every vendor gets a fit score (0-100) with clear reasoning:
```
Score: 87.3/100
Why: Within budget ($8,500 ≤ $10,000)
     Matches dietary needs: vegetarian, gluten-free  
     Sufficient capacity (180 ≥ 150 guests)
```

No black box. No "trust the algorithm." You see exactly why the system recommends something—and you can disagree intelligently.

#### Decision 3: Show Dependencies, Not Just Options

When I chose the menu tier, the system immediately showed:
- New beverage budget needed
- Updated cost per person
- Remaining budget after this choice
- Whether we're still hitting venue minimums

This isn't a feature. **This is how platforms should work**—show people the impact of their decisions in real-time.

## What I Shipped

### The Analysis Engine

Fed 68 vendor PDFs into the system. It extracted pricing, capacity, dietary options, and market positioning—then ranked everything by fit score. Result: narrowed 68 options to 18 realistic choices in one afternoon (would've taken me a week manually).

### The Planning Workflow

Built phase-based templates for venue selection, photography, music, and budgeting. Each template has:
- Embedded examples from my actual planning
- Guided prompts to reduce decision paralysis  
- Communication templates for vendor outreach
- Budget calculators that update in real-time

Other couples are now using these templates. That's the "platform thinking" part—design once, reuse everywhere.

### The Budget Intelligence

Created market analysis tools that compare vendor quotes against averages:
- "This catering quote is 47% above market rate"
- "Suggested counter-offer: $10,000 (20% reduction)"
- "Negotiation strategy: Emphasize budget constraints, reference competitors"

I may not have used it to actually negotiate (too much social anxiety for that), but knowing I *could* changed how confident I felt making decisions.

## The Results (In Actual Numbers)

Here's what happened when I used this system to plan my real wedding:

**Discovery Phase**
- Started with: 68 vendor PDFs from 11 Boston restaurants
- System surfaced: 18-20 realistic options (filtered by budget + dietary needs)
- Time saved: ~15 hours of manual spreadsheet work

**Decision Phase**  
- Selected: The Banks Seafood & Steak
- Menu planning: 3 appetizers, 4 entrees, 2 sides, 3 desserts, 5 cocktail hour items
- Accommodated: 4 distinct dietary restrictions (2 celiac, 1 tree nut allergy, 10 non-drinkers)
- Final cost: $5,406.90 vs $6,700 budget = **$1,293 remaining**
- Cost per person: $270.35 (transparent breakdown at every step)

**Platform Thinking**
- Templates created: 9 reusable worksheets
- Other couples using them: At least 3 that I know of
- GitHub stars: (None yet, but this is a portfolio piece, not a product launch 😄)

**Confidence Level**
- Before system: "I have no idea if this is a good price"
- After system: "I know exactly where this sits in the market, what I'm optimizing for, and what tradeoffs I'm making"

That last one? That's the real metric.

## How This Relates to Product Design

Here's what I learned building this (and what translates to any data/analytics platform):

### 1. Users Need to See Relationships, Not Just Data

Wedding planning isn't about individual vendors—it's about how venue choice affects menu options affects beverage needs affects budget. 

Similarly, in analytics platforms, users don't just need to see tables and metrics. They need to understand **lineage**: how this metric derives from that model, which pulls from these tables. Make the dependencies visible.

### 2. Explainability Beats Sophistication

I could've built a machine learning model to predict "best venue." Instead, I built a transparent scoring system: "87.3/100 because it's within budget, has capacity, and matches dietary needs."

Users trusted the simple, explainable system way more than they would've trusted "the AI says this one."

**Takeaway**: In analytics tools, show your work. Users need to interrogate recommendations, not just accept them.

### 3. Reduce Friction Between Exploration and Action

The worst workflow: Analyze in one tool → Switch to spreadsheet → Draft email in another app → Store decision in a fourth place.

My system: See recommendation → Use template → Generate communication → Document decision—all in one mental model.

**Takeaway**: Seamless transitions between discovery, analysis, and execution. That's the whole game.

### 4. Make Examples Do Heavy Lifting

I didn't write a 50-page guide. I just showed my actual wedding planning (the `examples/` folder) and let people pattern-match.

**Takeaway**: Good documentation is executable examples, not walls of text. Let users learn by observing, then adapting.

## Design Patterns & Scalability

### Extensible Architecture
The platform uses a **plugin-based skills system** that mirrors design system patterns:

**Base Skill Interface** (like a design component)
```python
class BaseSkill:
    - name: str
    - description: str  
    - version: str
    - category: str
    - execute(**kwargs) -> Result
```

**Built-in Skills** (like foundational components):
- **Contract Analyzer**: Extracts payment terms, cancellation policies, red flags
- **Timeline Generator**: Creates customized planning timelines (12-month, 6-month, rushed)
- **Budget Tracker**: Tracks expenses, provides forecasts, compares to industry standards

**Design Principle**: New skills inherit consistent patterns, ensuring predictable mental models as platform grows.

### Cross-Surface Consistency
The system maintains mental model coherence across interfaces:

**UI (Templates & Documents)**
- Category-first navigation
- Embedded guidance and examples
- Progressive disclosure of complexity

**CLI (Python Scripts)**
- Semantic commands matching user workflows (`scan`, `organize`, `recommend`, `negotiate`)
- Consistent output formats
- Composable operations for power users

**Configuration (YAML)**
- Declarative preferences matching UI concepts
- Budget categories align with folder structure
- Dietary restrictions map to semantic vendor data model

**API (Skills System)**
- RESTful plugin architecture
- Consistent input/output contracts
- Self-documenting capabilities (`skills list`, `skills help`)

## File Naming Convention

Organized files follow this pattern:
```
{category}_{venue_name}_{price}_{original_name}.{ext}

Examples:
- venue_Grand_Hall_$15000_proposal.pdf
- catering_Bistro_Catering_$8500_menu.pdf
- floral_Bloom_Studio_$2800_arrangements.png
```

## Technical Implementation

### Data Pipeline & Semantic Layer
**Challenge**: Transform unstructured vendor PDFs into queryable, semantically meaningful data

**Solution**:
1. **Extraction Layer**: OCR and text parsing from 68+ PDFs (PyPDF2, Tesseract)
2. **Semantic Modeling**: Standardize extracted data into consistent entities (Venue, Price, Capacity, Dietary Options)
3. **Metadata Enrichment**: Auto-categorize and tag vendor information
4. **Storage Layer**: Organized file system with clear naming conventions (`{category}_{venue}_{price}_{file}`)

**Design Decision**: Chose file-based storage over database to maintain portability and enable easy sharing with non-technical users.

### Recommendation Algorithm
**Transparent fit-score calculation** (not black-box AI):

```
Fit Score = weighted_average([
    budget_match (40%),
    capacity_match (30%),
    dietary_match (20%),
    market_positioning (10%)
])
```

Each factor includes human-readable explanation:
- "Within budget ($8,500 <= $10,000)"
- "Matches dietary needs: vegetarian, gluten-free"
- "Sufficient capacity (180 >= 150 guests)"

**Why this matters**: Users can understand *why* a recommendation was made, enabling them to adjust preferences and re-run analysis.

## Repository Structure

```
wedding-planning-agent/
 
 examples/                  # Real-world application (Boston wedding, Feb 2026)
    planning/              # Category-organized planning documents
      01_venue_and_catering/
      02_photography/
      03_music/
      04_other_vendors/
    analysis_5000/         # Budget scenario A ($5K constraint analysis)
    analysis_6500/         # Budget scenario B ($6.7K comparative analysis)
    data/                  # Raw vendor PDFs and organized metadata
    outputs/               # Generated recommendations and insights
 
 templates/                 # Reusable blank worksheets
    venue_and_catering/   # Structured by practitioner workflow
    photography/
    music/
    budget/
 
 docs/                      # User guides and documentation
    REPOSITORY_STRUCTURE.md
    WEDDING_CHECKLIST.md
    QUICKSTART.md
 
 src/                       # Technical implementation
    scanner.py             # PDF/image text extraction & OCR
    organizer.py           # Semantic file organization
    recommender.py         # Fit-score recommendation engine
    negotiator.py          # Market analysis & negotiation support
    skills/                # Extensible plugin system
 
 config.yaml                # Declarative preferences & budget
 main.py                    # CLI interface
```

---

## The Technical Stuff (For Those Who Care)

### How It Actually Works

**Data Pipeline**:
1. OCR extracts text from vendor PDFs (PyPDF2 + Tesseract)
2. Semantic layer standardizes it into entities: Venue, Price, Capacity, Dietary Options
3. Files get renamed with metadata: `venue_TheBank_$5400_menu.pdf`
4. Recommendation engine scores each option against your constraints

**Why file-based storage?** Because I wanted friends to fork this repo and use it without installing PostgreSQL. Portability > perfection.

**The Scoring Algorithm**:
```
Fit Score = weighted_average([
    budget_match (40%),
    capacity_match (30%),
    dietary_match (20%),
    market_positioning (10%)
])
```

Nothing fancy. Just transparent logic you can interrogate and adjust.

### The Plugin System

Built an extensible skills architecture (think design system, but for analysis tools):
- **Contract Analyzer**: Extracts payment terms and red flags from vendor contracts  
- **Timeline Generator**: Creates planning timelines (12-month, 6-month, or rushed)
- **Budget Tracker**: Tracks spend against forecasts

Each skill has a consistent interface, so adding new capabilities doesn't break the mental model.

---

## What This Shows About How I Work

### I Start With Real Problems

I didn't build this to showcase skills. I built it because I was drowning in vendor PDFs and needed help. The product thinking came from experiencing the pain firsthand.

**Takeaway**: Best designs come from actually using the thing, not from conference room whiteboarding.

### I Think in Systems, Not Features

This isn't "a budget tracker" or "a vendor comparison tool." It's an interconnected system where every piece reinforces the mental model: **structured data → transparent analysis → confident decisions**.

**Takeaway**: Features are easy. Coherent experiences are hard.

### I Ship, Then Iterate

V1 was messy Python scripts. V2 added templates. V3 reorganized for shareability. This README? V4. I didn't wait for perfection—I shipped and learned.

**Takeaway**: Done is better than perfect, but iteration is better than done.

### I Design for Reusability

The `examples/` folder is my personal wedding. The `templates/` folder is for anyone. Separating these was intentional—it forces you to think about patterns, not just one-off solutions.

**Takeaway**: If you can't explain it to someone else, you don't understand it well enough yourself.

---

## Want to Talk About This?

I'm happy to walk through:
- How I approached the semantic modeling
- Why I chose certain UX patterns over others
- What I'd do differently if I started over
- How this applies to analytics platforms / data tools / [your product here]

This was a fun side project that accidentally became a good portfolio piece. If you're hiring for product design, systems thinking, or data platform roles, let's chat.

**GitHub**: You're already here  
**LinkedIn**: [Your LinkedIn]  
**Portfolio**: [Your portfolio site]

---

## License

MIT License - Wedding planning system available for community use.
