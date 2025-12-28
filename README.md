# Wedding Planning Agent 🎉

An AI-powered wedding planning assistant that scans vendor documents, organizes options, provides personalized recommendations, and helps you plan your perfect celebration.

## 📊 Project Status - December 2025

### 🎯 Current Event Planning
**Venue:** The Banks Seafood and Steak - Fireplace Room  
**Guest Count:** 20 people  
**Budget:** $6,700  
**Date:** TBD  
**Status:** Finalizing menu selections and vendor communications

### ✅ Completed Milestones

#### Phase 1: Vendor Research & Analysis
- ✅ Scanned **68+ vendor PDFs** from 11 Boston restaurants
- ✅ Extracted pricing, menu options, and capacity details
- ✅ Analyzed options for $5,000 budget (18 venues fit)
- ✅ Analyzed options for $6,700 budget (20 venues fit - all options!)
- ✅ Created comprehensive comparison documents

#### Phase 2: Venue Selection
- ✅ Selected **The Banks Seafood and Steak** - Fireplace Room
- ✅ Reviewed private dining packet and beverage options
- ✅ Calculated detailed costs for Tier 2 dinner menu
- ✅ Finalized menu selections:
  - 3 appetizer choices
  - 4 entrée options
  - 2 family-style sides
  - 3 dessert selections
  - 5 types of hors d'oeuvres for cocktail hour

#### Phase 3: Menu Planning & Budgeting
- ✅ Created detailed cost breakdown: **$5,406.90 total**
  - Dinner: $2,600 (Tier 2 + sides)
  - Hors d'oeuvres: $575 (increased per family feedback)
  - Beverages: $860 (6 wine bottles + ~20 cocktails)
  - Fees included: 20% gratuity, 7% admin, 7% tax
- ✅ Accommodated dietary restrictions:
  - 2 guests with celiac disease (gluten-free)
  - 1 guest with tree nut allergy
  - ~10 non-drinking guests (religious/health/preference/age)
- ✅ Optimized beverage quantities for guest mix

#### Phase 4: Communication Materials
- ✅ Created vendor inquiry email with 21 detailed questions
- ✅ Prepared guest invitation details (plain & formatted versions)
- ✅ Documented all menu selections with full descriptions
- ✅ Set event timeline: 5-8 PM (1 hour cocktails, 2 hours dinner)

### 📁 Project Organization

```
analysis/                    # Original $5K budget analysis
analysis_6500/              # Expanded $6.7K budget analysis
analysis_thebanks/          # Detailed venue-specific planning
├── detailed_cost_analysis.md
├── email_to_thebanks.txt
├── email_to_thebanks_formatted.txt
├── guest_invitation_details.txt
└── guest_invitation_details_formatted.txt
data/raw/                   # 68 vendor PDFs organized by restaurant
```

### 🎯 Next Steps
1. ⏳ Send inquiry email to The Banks
2. ⏳ Schedule tasting and site visit
3. ⏳ Confirm final date and finalize guest count
4. ⏳ Send guest invitations with menu details
5. ⏳ Book photographer, florist, and other services

### 💰 Budget Summary
- **Original Budget:** $5,000 → Over by $407
- **Adjusted Budget:** $6,700 → **$1,293 remaining** ✅
- **Cost per Person:** $270.35
- **Venue Minimum Met:** $4,035 > $2,500 ✅

---

## ✨ Features

### Core Functionality
- **Document Scanning**: Extract text from PDFs and images (PNGs, JPGs) using OCR
- **Smart Metadata Extraction**: Automatically detects venue names, prices, capacity, dietary options, and categories
- **File Organization**: Renames and organizes files with clear conventions: `{category}_{venue}_{price}_{original_name}`
- **Intelligent Recommendations**: Ranks options by fit score considering budget, dietary needs, and capacity
- **Detailed Reports**: Generate comprehensive reports with top recommendations per category

### 🆕 Negotiation Agent
- **Quote Analysis**: Analyzes vendor quotes against market rates and your budget
- **Counter-Offer Suggestions**: Calculates strategic counter-offers (15-20% reductions)
- **Email Draft Generation**: Creates professional negotiation emails in 3 tones:
  - **Professional**: Formal business tone
  - **Friendly**: Warm and personable
  - **Firm**: Direct and assertive
- **Market Comparison**: Compares quotes to industry averages
- **Negotiation Strategies**: Provides tactical approaches and talking points
- **Batch Analysis**: Analyze multiple quotes and generate comprehensive reports

### 🆕 Extensible Skills System
Plugin architecture for adding custom capabilities. Includes built-in skills:

- **Contract Analyzer**: Extracts payment terms, cancellation policies, and red flags from vendor contracts
- **Timeline Generator**: Creates customized wedding planning timelines (12-month, 6-month, or rushed)
- **Budget Tracker**: Tracks expenses, provides forecasts, and compares to industry standards

**Easily add your own skills** by inheriting from `BaseSkill` class!

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: For image OCR, you also need Tesseract:
- **macOS**: `brew install tesseract`
- **Ubuntu**: `sudo apt-get install tesseract-ocr`
- **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

### 2. Initialize Project

```bash
python main.py init
```

This creates the directory structure:
```
data/
  raw/           # Put your PDFs and PNGs here
  organized/     # Organized files appear here
    venue/
    catering/
    floral/
    photography/
    entertainment/
    other/
outputs/
  recommendations/  # Reports saved here
```

### 3. Configure Your Preferences

Edit `config.yaml` with your budget and preferences:

```yaml
budget:
  max_total: 50000
  venue: 15000
  catering: 10000
  floral: 3000
  photography: 5000

preferences:
  dietary_restrictions:
    - vegetarian
    - gluten-free
  guest_count: 150
  preferred_season: "fall"
  location_preference: "outdoor"
```

### 4. Add Your Files

Place wedding vendor PDFs and PNGs in `data/raw/`

### 5. Get Recommendations

```bash
python main.py recommend
```

This will:
1. Scan all files in `data/raw/`
2. Extract key information (price, capacity, dietary options)
3. Organize files into categories
4. Rank options by fit score
5. Generate a detailed report saved to `outputs/recommendations/`

## Commands

### Initialize project
```bash
python main.py init
```

### Scan a single file
```bash
python main.py scan data/raw/venue_proposal.pdf
```

### Scan a directory
```bash
python main.py scan data/raw/
```

### Organize files (without recommendations)
```bash
python main.py organize
```

### Generate recommendations
```bash
python main.py recommend
```

### 🆕 Negotiate with a vendor
Analyze a single vendor quote:
```bash
# Just analyze the quote
python main.py negotiate data/raw/catering_quote.pdf

# Analyze and draft negotiation email (professional tone)
python main.py negotiate data/raw/catering_quote.pdf --draft

# Draft with different tone
python main.py negotiate data/raw/venue_quote.pdf --draft --tone friendly
python main.py negotiate data/raw/photography_quote.pdf --draft --tone firm
```

### 🆕 Batch negotiation analysis
Analyze all quotes in a directory:
```bash
python main.py negotiate-batch data/raw/
```
Generates a comprehensive report with:
- Overall savings potential
- Vendor-by-vendor analysis
- Market comparisons
- Strategic recommendations

### 🆕 Skills Management
List all available skills:
```bash
python main.py skills list
```

Get help on a specific skill:
```bash
python main.py skills help --name contract_analyzer
```

Run a skill:
```bash
# Generate wedding timeline
python main.py skills run --name timeline_generator --args '{"wedding_date": "2026-06-15", "style": "comprehensive"}'

# Analyze a contract
python main.py skills run --name contract_analyzer --args '{"contract_file": "data/raw/venue_contract.pdf"}'

# Get budget summary
python main.py skills run --name budget_tracker --args '{"action": "summary"}'

# Get budget recommendations
python main.py skills run --name budget_tracker --args '{"action": "recommendations"}'
```

## File Naming Convention

Organized files follow this pattern:
```
{category}_{venue_name}_{price}_{original_name}.{ext}

Examples:
- venue_Grand_Hall_$15000_proposal.pdf
- catering_Bistro_Catering_$8500_menu.pdf
- floral_Bloom_Studio_$2800_arrangements.png
```

## How It Works

### 1. Document Scanner (`src/scanner.py`)
- Extracts text from PDFs using PyPDF2
- Extracts text from images using Tesseract OCR
- Parses metadata: price, capacity, dietary options, category, venue name

### 2. File Organizer (`src/organizer.py`)
- Renames files based on extracted metadata
- Sorts into category directories
- Maintains original files in `data/raw/`

### 3. Recommendation Engine (`src/recommender.py`)
- Calculates fit scores (0-100) for each option
- Considers budget limits per category
- Matches dietary restrictions
- Checks venue capacity vs guest count
- Ranks options and explains reasoning

## Example Output

```
=============================================================
WEDDING PLANNING RECOMMENDATIONS
=============================================================

Budget Summary:
  Max Total: $50,000
  Venue: $15,000
  Catering: $10,000
  Floral: $3,000
  Photography: $5,000

Preferences:
  Guest Count: 150
  Dietary Restrictions: vegetarian, gluten-free

=============================================================
RECOMMENDATIONS BY CATEGORY
=============================================================

### VENUE ###

1. venue_Grand_Hall_$14500_proposal.pdf
   Score: 87.3/100
   Price: $14,500
   Capacity: 180 guests
   Why: Within budget ($14,500 <= $15,000); Sufficient capacity (180 >= 150 guests)

2. venue_Garden_Estate_$18000_brochure.pdf
   Score: 52.1/100
   Price: $18,000
   Capacity: 200 guests
   Why: Over budget ($18,000 > $15,000); Sufficient capacity (200 >= 150 guests)

### CATERING ###

1. catering_Bistro_Catering_$8500_menu.pdf
   Score: 92.5/100
   Price: $8,500
   Dietary Options: vegetarian, gluten-free, vegan
   Why: Within budget ($8,500 <= $10,000); Matches dietary needs: vegetarian, gluten-free
```

## Troubleshooting

### OCR not working
- Ensure Tesseract is installed: `tesseract --version`
- On macOS, add to PATH: `export PATH="/usr/local/bin:$PATH"`

### No metadata extracted
- Check that PDFs contain text (not just images)
- For image-based PDFs, ensure they're high quality
- Verify file isn't password-protected

### Files not organizing
- Confirm files are in `data/raw/`
- Check file extensions (`.pdf`, `.png`, `.jpg` supported)
- Run `python main.py scan data/raw/` to debug extraction

## Project Structure

```
wedding-planning-agent/
├── main.py                    # CLI interface
├── config.yaml                # User preferences and budget
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── src/
│   ├── __init__.py
│   ├── scanner.py             # PDF/PNG text extraction
│   ├── organizer.py           # File renaming and organization
│   ├── recommender.py         # Recommendation engine
│   ├── negotiator.py          # 🆕 Negotiation agent
│   └── skills/                # 🆕 Extensible skills system
│       ├── __init__.py
│       ├── base_skill.py      # Base class for all skills
│       ├── contract_analyzer.py
│       ├── timeline_generator.py
│       └── budget_tracker.py
├── data/
│   ├── raw/                   # Input files (your PDFs/PNGs)
│   └── organized/             # Organized output by category
├── outputs/
│   ├── recommendations/       # Generated recommendation reports
│   └── negotiation/           # 🆕 Negotiation emails and reports
└── tests/
    └── test_agent.py
```

## 🔧 Creating Custom Skills

Extend the agent by creating your own skills! Here's how:

### 1. Create a new file in `src/skills/`

```python
# src/skills/my_custom_skill.py
from typing import Dict, Any
from .base_skill import BaseSkill

class MyCustomSkill(BaseSkill):
    @property
    def name(self) -> str:
        return "my_custom_skill"
    
    @property
    def description(self) -> str:
        return "Does something awesome for wedding planning"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def category(self) -> str:
        return "planning"  # or "analysis", "communication", "financial", etc.
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        # Your skill logic here
        return {
            'status': 'success',
            'result': {
                'message': 'Skill executed successfully!'
            }
        }
```

### 2. The skill is automatically discovered!

Just save the file and run:
```bash
python main.py skills list
```

Your skill will appear in the list and can be executed immediately.

### 3. Skill Ideas

- **Guest List Manager**: Track RSVPs, dietary restrictions, plus-ones
- **Seating Chart Generator**: Optimize table arrangements
- **Task Reminder**: Send notifications for upcoming deadlines
- **Vendor Contact Tracker**: Manage vendor communications
- **Theme Matcher**: Suggest color palettes and decorations
- **Weather Forecast**: Check weather for outdoor events
- **Music Playlist Generator**: Create ceremony/reception playlists

## 🎯 Negotiation Examples

### Example: Analyze a catering quote

**Input**: `data/raw/bistro_catering_quote.pdf`
```
Bistro Catering Services
Wedding Package: $12,500
Includes: Dinner for 150 guests, open bar, appetizers
```

**Output**:
```
NEGOTIATION ANALYSIS: Bistro Catering Services
=====================================
Quoted Price: $12,500.00
Budget Allocation: $10,000.00
Over Budget: Yes
Negotiation Potential: HIGH - Significantly above market rate

Suggested Counter-Offer: $10,000.00
  Reduction: $2,500.00 (20.0%)
  Rationale: aligns with our $10,000 budget allocation, brings price closer to market average ($8,500)

Market Comparison:
  Market Average: $8,500.00
  This Quote: above average
  Difference: +$4,000.00 (+47.1%)

Top Negotiation Strategies:
  1. Emphasize budget constraints ($10,000 allocated for catering)
  2. Reference market rates (average: $8,500)
  3. Consider reducing guest count or simplifying menu options
  4. Offer to book multiple services together for a discount
  5. Ask about off-season or weekday discounts
```

### Example: Draft negotiation email

```bash
python main.py negotiate data/raw/bistro_catering_quote.pdf --draft --tone professional
```

**Generated Email**:
```
Subject: Re: Catering Quote - Following Up

Dear Bistro Catering Services Team,

Thank you for providing your detailed quote for our wedding catering. We were impressed with your offerings and the quality of service you provide.

After carefully reviewing our overall wedding budget and comparing various options, we would like to discuss the pricing. Your quoted amount of $12,500.00 is slightly above our allocated budget for this category.

We would like to propose a revised price of $10,000.00, which represents a 20.0% adjustment. This aligns with our $10,000 budget allocation, brings price closer to market average ($8,500).

We are very interested in working with you and believe this pricing would allow us to move forward confidently. We are flexible on certain details and would be happy to discuss how we can make this work for both parties.

Would you be available for a brief call this week to discuss this further? We are hoping to finalize our vendor selections soon and would love to include you in our plans.

Thank you for your consideration, and we look forward to hearing from you.

Best regards,
[Your Name]
```

## Contributing

### Ways to Extend the Agent

1. **Add new metadata extraction patterns**
   - Edit `src/scanner.py` → `_extract_metadata()`
   - Add regex patterns for new data types (dates, contact info, etc.)

2. **Improve recommendation algorithm**
   - Edit `src/recommender.py` → `_calculate_fit_score()`
   - Add new ranking criteria (location, reviews, availability)

3. **Add negotiation strategies**
   - Edit `src/negotiator.py` → `_generate_strategies()`
   - Include industry-specific tactics

4. **Create custom skills**
   - Add new Python files to `src/skills/`
   - Inherit from `BaseSkill` class
   - Implement `execute()` method

5. **Add new categories**
   - Update `config.yaml` → `file_organization.categories`
   - Add new budget categories

### Future Enhancement Ideas

- [ ] Integration with Google Calendar for deadline tracking
- [ ] Email automation for vendor outreach
- [ ] Web scraping for market rate research
- [ ] Machine learning for better recommendations
- [ ] LLM integration for natural language queries
- [ ] Mobile app interface
- [ ] Vendor review aggregation
- [ ] Contract template generation
- [ ] Budget optimization algorithms
- [ ] Guest RSVP management system

## 📝 Configuration Options

Update `config.yaml` to customize:

```yaml
# Budget allocation
budget:
  max_total: 50000
  venue: 15000
  catering: 10000
  # ... add more categories

# Your preferences
preferences:
  dietary_restrictions: [vegetarian, gluten-free]
  guest_count: 150
  wedding_date: "2026-06-15"

# Negotiation settings
negotiation:
  default_tone: professional  # or friendly, firm
  counter_offer_strategy: moderate  # or aggressive, conservative
  auto_save_drafts: true

# Skills
skills:
  enabled: true
  auto_discover: true
```

## 🤝 Support

For questions or issues:
- Check existing documentation in this README
- Review code comments in source files
- Experiment with the CLI commands
- Create custom skills for your specific needs

## License

MIT License - feel free to use for your wedding planning needs!
