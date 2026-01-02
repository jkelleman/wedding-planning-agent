# Wedding Planning Agent

**A case study in designing coherent, end-to-end experiences for complex decision-making workflows**

## Overview

This project demonstrates **systems-level UX design** and **product strategy** applied to wedding planning—a domain characterized by fragmented information, high cognitive load, and emotional decision-making. By treating wedding planning as a **data platform problem**, I designed a unified system that reduces context switching, establishes clear mental models, and empowers users to make confident decisions.

**Key Focus Areas:**
- **Coherent workflows** spanning discovery, analysis, and execution
- **Semantic modeling** of vendor data for consistent self-serve exploration  
- **Intuitive relationships** across documents, vendors, and decisions
- **Observability and trust** through transparent analysis and recommendations
- **Reduced cognitive load** via structured templates and guided processes

## The Problem

Wedding planning practitioners face:
- **Fragmented information**: 68+ vendor PDFs with inconsistent formats
- **Context switching**: Moving between discovery, comparison, budgeting, and communication
- **Lack of observability**: No clear view of how decisions affect budget and dependencies
- **Cognitive overload**: Manual tracking of dietary restrictions, capacity, pricing, and vendor relationships
- **Trust gaps**: Difficulty validating vendor claims against market rates

**Real-world application**: Planned a 20-guest intimate wedding in Boston (Feb 2026, $6,700 budget)

## Design Approach

### 1. Design Vision & Strategy

**Goal**: Create a unified analytics and planning experience with minimal context switching

I designed three interconnected workflows with consistent mental models:

**Discovery & Analysis Workflow**
- Semantic modeling of vendor data (price, capacity, dietary options, category)
- Automated metadata extraction to create queryable vendor database
- Fit-score ranking system that makes decision factors transparent
- Market comparison to establish trust and validate pricing

**Planning & Execution Workflow**  
- Phase-based organization (venue → photography → music → other vendors)
- Reusable template system for consistent planning experience
- Guided worksheets that reduce cognitive load during decision-making
- Communication templates for vendor outreach with consistent tone

**Observability & Governance Workflow**
- Real-time budget tracking with automatic calculations
- Dependency visualization (e.g., menu choices → beverage needs → total cost)
- Data lineage: from raw PDFs → organized metadata → recommendations → decisions
- Audit trail of all planning decisions and their impacts

### 2. System Architecture

The platform is organized around clear practitioner mental models:

```
examples/                    # OBSERVE: Real-world example demonstrating patterns
  ├── planning/             # Planning documents organized by category (semantic grouping)
  ├── analysis_5000/        # Budget scenario A: constraint-based analysis
  ├── analysis_6500/        # Budget scenario B: comparative analysis  
  ├── data/                 # Raw and organized vendor materials (data lineage)
  └── outputs/              # Generated insights and recommendations (analytics)

templates/                  # CREATE: Blank worksheets with embedded guidance
  ├── venue_and_catering/   # Organized by practitioner workflow, not system architecture
  ├── photography/
  ├── music/
  └── budget/

docs/                       # LEARN: Contextual documentation and best practices
  ├── REPOSITORY_STRUCTURE.md
  ├── WEDDING_CHECKLIST.md
  └── QUICKSTART.md
```

**Design Principle**: Users can seamlessly move between **observing** (examples), **creating** (templates), and **learning** (docs) without mental model disruption.

### 3. Key Design Decisions

#### Semantic Modeling for Self-Serve Analytics
Created a consistent data model for all vendor information:
- **Entities**: Venue, Price, Capacity, Dietary Options, Category
- **Relationships**: Venue → Menu Items → Dietary Accommodations → Guest Needs
- **Metrics**: Fit Score (0-100), Cost per Person, Budget Utilization %

This enables practitioners to:
- Query vendor data without knowing file structures  
- Understand dependencies (e.g., venue choice → menu options → accommodations)
- Trust recommendations through transparent scoring methodology

#### Unified Navigation & Discovery
Reduced context switching by co-locating related information:
- Planning documents are **category-first**, not **chronologically organized**
- Each category folder contains: comparison, contacts, communications, timeline
- Templates mirror planning folder structure for mental model consistency

#### Observability & Troubleshooting
Built transparency into every workflow:
- **Budget tracking**: Real-time calculation showing how decisions affect remaining budget
- **Dependency mapping**: Clear lineage from vendor quote → menu selection → total cost
- **Data freshness**: Timestamps on all analysis documents
- **Quality indicators**: Fit scores explained with reasoning (not black box)

## Platform Capabilities

### Analysis & Recommendations Engine
**Problem**: Users don't trust black-box recommendations  
**Solution**: Transparent, explainable scoring system

- **Semantic modeling**: Vendor data structured as queryable entities (not just files)
- **Multi-criteria ranking**: Budget, capacity, dietary accommodations, market positioning
- **Explainable AI**: Every recommendation includes reasoning and tradeoffs
- **Comparative analysis**: Side-by-side scenario modeling ($5K vs $6.7K budget)

**Impact**: Analyzed 68+ vendor PDFs, surfaced 18-20 options matching constraints, enabled confident decision-making

### Guided Workflows & Templates
**Problem**: Cognitive overload from unstructured planning  
**Solution**: Phase-based workflows with embedded best practices

- **Progressive disclosure**: Information revealed when relevant to current phase
- **Consistent patterns**: Every category follows same workflow (compare → contact → plan)
- **Embedded guidance**: Templates include prompts and examples to reduce learning curve
- **Reusability**: Templates separate from personal data for shareability

**Impact**: Reduced planning time, enabled knowledge sharing with other couples

### Observability & Budget Governance
**Problem**: Decisions made in isolation cause budget overruns  
**Solution**: Real-time dependency tracking and constraint validation

- **Live budget tracking**: Automatic calculation as decisions are made
- **Dependency visualization**: Menu choice → beverage needs → guest count → total cost
- **Constraint validation**: System flags when selections exceed capacity or budget
- **Audit trail**: Full lineage from vendor quote to final cost breakdown

**Impact**: Stayed within revised budget ($6.7K), accommodated 4 dietary restrictions across 20 guests

### Negotiation & Market Intelligence
**Problem**: Users lack market context for vendor pricing  
**Solution**: Comparative market analysis with negotiation guidance

- **Market benchmarking**: Compare vendor quotes against industry averages
- **Counter-offer calculator**: Strategic price reduction suggestions (15-20%)
- **Multi-tone communication**: Generate professional, friendly, or firm negotiation emails
- **Batch analysis**: Understand overall vendor landscape, not just individual quotes

**Impact**: Provided negotiation leverage through data-driven market positioning

## Real-World Application

**Context**: Planned a 20-guest intimate wedding in Boston (February 2026)

### Workflow Execution

**Phase 1: Discovery & Analysis**
- Processed 68+ vendor PDFs from 11 Boston restaurants
- Extracted semantic data: pricing, capacity, dietary options, menu details
- Ran constraint-based analysis for two budget scenarios ($5K, $6.7K)
- Generated comparative recommendations with explainable fit scores

**Phase 2: Vendor Selection & Planning**  
- Selected The Banks Seafood & Steak based on transparent multi-criteria analysis
- Used planning templates to structure menu selection (3 appetizers, 4 entrees, 2 sides, 3 desserts, 5 hors d'oeuvres)
- Applied observability: tracked how each menu choice affected final cost
- Accommodated 4 distinct dietary needs (2 celiac, 1 tree nut allergy, 10 non-drinkers)

**Phase 3: Budget & Dependency Management**
- Live budget tracking: $5,406.90 final cost vs $6,700 budget = $1,293 remaining
- Dependency modeling: Guest mix → beverage quantities (6 wine bottles, ~20 cocktails)
- Cost per person calculation: $270.35 (transparent breakdown)
- Validated venue minimum: $4,035 spend > $2,500 requirement

**Phase 4: Communication & Coordination**
- Generated vendor inquiry template with 21 standardized questions
- Created guest invitation materials (plain text + formatted versions)
- Documented timeline: 5-8 PM event (1hr cocktails, 2hr dinner)

### Measurable Outcomes
- ✅ **Reduced decision time**: Semantic modeling enabled rapid vendor comparison
- ✅ **Budget adherence**: Stayed within constraints through real-time observability  
- ✅ **Complexity management**: Successfully accommodated 4 dietary restrictions across 20 guests
- ✅ **Reusability**: Templates now used by other couples for their planning
- ✅ **Confidence**: Transparent analysis and dependencies enabled trust in decisions

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

## Skills for Platform Roles

This project demonstrates capabilities relevant to **product design, systems architecture, and data platform roles**:

### Design & Strategy
- **User research**: Identified pain points through personal wedding planning experience
- **Systems thinking**: Designed coherent workflows across discovery, analysis, and execution
- **Mental model design**: Created consistent patterns across UI, CLI, and configuration
- **Design patterns**: Established reusable templates and components (skills system)
- **Observability**: Built transparency into every workflow for user trust

### Cross-Functional Collaboration
- **Technical fluency**: Implemented working prototype with Python, OCR, semantic modeling
- **Documentation**: Created comprehensive guides for different user personas (practitioners, contributors)
- **Stakeholder communication**: Designed solution that serves both personal needs and community sharing
- **Scope management**: Delivered functional MVP, documented future enhancements

### Product Thinking
- **Problem framing**: Treated wedding planning as a data platform challenge
- **Semantic modeling**: Structured unstructured vendor data for self-serve analytics
- **Dependency mapping**: Made relationships between decisions visible and intuitive
- **Governance**: Built budget constraints and validation into the workflow
- **Iteration**: Started with $5K budget scenario, evolved to $6.7K with expanded features

### Impact & Measurability
- **Quantifiable outcomes**: Processed 68 PDFs → 18-20 viable options → 1 confident decision
- **Reusability**: Templates adopted by other couples (platform thinking)
- **Reduced cognitive load**: Structured workflows decreased decision time
- **Trust through transparency**: Explainable recommendations built user confidence

---

## Repository Navigation

**For recruiters and hiring managers:**
- `/examples/` - See real-world application with actual wedding planning data
- `/templates/` - Examine reusable design patterns and component structure
- `/docs/` - Review documentation strategy and user guidance approach
- This README - Understand design vision, strategy, and systems thinking

**Technical implementation:**
- `/src/` - Python codebase (scanner, organizer, recommender, negotiator, skills system)
- `config.yaml` - Configuration design and preference modeling
- `main.py` - CLI interface and command design

---

## Contact & Portfolio

This project showcases my approach to:
- Designing end-to-end analytics and data experiences
- Creating coherent workflows with minimal context switching
- Building semantic models for self-serve exploration
- Establishing observability and governance
- Thinking in systems, not features

**Want to discuss this project or explore how these skills apply to your team?**  
Feel free to reach out via GitHub or LinkedIn.

---

## License

MIT License - Wedding planning system available for community use.
