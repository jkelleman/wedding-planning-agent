# Wedding Planning Agent - Quick Start Guide 🎉

## What's New? ✨

Your wedding planning agent now has **3 major new capabilities**:

### 1. 🤝 Negotiation Agent
- Analyzes vendor quotes vs. your budget and market rates
- Suggests strategic counter-offers (typically 15-20% reductions)
- Drafts professional negotiation emails in 3 tones
- Provides tactical talking points and strategies

### 2. 🧩 Extensible Skills System
- Plugin architecture - easily add new capabilities
- Auto-discovery - just drop a file in `src/skills/` and it's ready
- Built-in skills included:
  - **Contract Analyzer**: Find red flags, extract terms
  - **Timeline Generator**: Custom planning timelines
  - **Budget Tracker**: Track spending, get recommendations
  - **Vendor Comparison**: Side-by-side analysis

### 3. 📄 Enhanced Document Processing
- Better PDF/PNG scanning
- Improved metadata extraction
- Organized output structure

## Getting Started in 5 Minutes

### 1. Install Dependencies
```bash
pip install -r requirements.txt

# Install Tesseract for OCR
brew install tesseract  # macOS
```

### 2. Initialize Project
```bash
python main.py init
```

### 3. Configure Your Budget
Edit `config.yaml`:
```yaml
budget:
  max_total: 50000
  venue: 15000
  catering: 10000
  
preferences:
  guest_count: 150
  dietary_restrictions: [vegetarian, gluten-free]
  wedding_date: "2026-06-15"
```

### 4. Add Your Files
Put vendor quotes (PDFs/PNGs) in: `data/raw/`

### 5. Get Started!
```bash
# Get recommendations
python main.py recommend

# Negotiate a quote
python main.py negotiate data/raw/venue_quote.pdf --draft

# Check skills
python main.py skills list
```

## Common Use Cases

### 📊 Scenario 1: You received a venue quote
```bash
# Analyze if it's a good deal
python main.py negotiate data/raw/venue_grand_hall.pdf

# Draft a negotiation email
python main.py negotiate data/raw/venue_grand_hall.pdf --draft --tone professional
```

### 📋 Scenario 2: You have multiple catering options
```bash
# Organize and compare them
python main.py recommend

# Or use the vendor comparison skill
python main.py skills run --name vendor_comparison --args '{
  "category": "catering",
  "vendors": [
    {"name": "Bistro A", "price": 8500, "rating": 4.5, "pros": ["Great food", "Flexible"], "cons": ["Limited menu"]},
    {"name": "Bistro B", "price": 12000, "rating": 4.8, "pros": ["Amazing reviews", "Full service"], "cons": ["Expensive"]}
  ]
}'
```

### 📅 Scenario 3: Create your planning timeline
```bash
python main.py skills run --name timeline_generator --args '{
  "wedding_date": "2026-06-15",
  "style": "comprehensive"
}'
```

### 📑 Scenario 4: Review a vendor contract
```bash
python main.py skills run --name contract_analyzer --args '{
  "contract_file": "data/raw/venue_contract.pdf"
}'
```

### 💰 Scenario 5: Track your budget
```bash
# Get budget summary
python main.py skills run --name budget_tracker --args '{"action": "summary"}'

# Get recommendations based on industry standards
python main.py skills run --name budget_tracker --args '{"action": "recommendations"}'
```

## File Organization

After running commands, your files will be organized like this:

```
data/
├── raw/                              # Your original files
│   ├── venue_quote.pdf
│   ├── catering_menu.png
│   └── photographer_proposal.pdf
└── organized/                        # Auto-organized files
    ├── venue/
    │   └── venue_Grand_Hall_$15000_quote.pdf
    ├── catering/
    │   └── catering_Bistro_$8500_menu.png
    └── photography/
        └── photography_ProShots_$4000_proposal.pdf

outputs/
├── recommendations/                   # Recommendation reports
│   └── recommendations_20251227_143022.txt
└── negotiation/                       # Negotiation drafts & reports
    ├── catering_Bistro_20251227_143045.txt
    └── negotiation_report_20251227_143100.txt
```

## Pro Tips 💡

1. **Start with the recommend command** - It gives you an overview of all your options ranked by fit

2. **Use batch negotiation** - Analyze all quotes at once:
   ```bash
   python main.py negotiate-batch data/raw/
   ```

3. **Create custom skills** - The system auto-discovers them! Just create a file in `src/skills/`

4. **Adjust negotiation tone** - Use `--tone firm` for expensive quotes, `--tone friendly` for preferred vendors

5. **Check the contract analyzer** - Before signing anything, run it through the analyzer to find red flags

## Building Your Own Skill

Create `src/skills/my_skill.py`:

```python
from typing import Dict, Any
from .base_skill import BaseSkill

class MySkill(BaseSkill):
    @property
    def name(self) -> str:
        return "my_skill"
    
    @property
    def description(self) -> str:
        return "What my skill does"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def category(self) -> str:
        return "planning"
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        # Your logic here
        return {
            'status': 'success',
            'result': {'message': 'It works!'}
        }
```

That's it! Run `python main.py skills list` and it's there!

## Next Steps

- [ ] Add all your vendor quotes to `data/raw/`
- [ ] Run `python main.py recommend` to see ranked options
- [ ] Use `negotiate` command on quotes over budget
- [ ] Check contracts with `contract_analyzer`
- [ ] Generate your planning timeline
- [ ] Track expenses with `budget_tracker`
- [ ] Create custom skills for your specific needs

## Need Help?

All commands support `--help`:
```bash
python main.py --help
python main.py negotiate --help
python main.py skills --help
```

Check `README.md` for full documentation.

Happy planning! 🎊
