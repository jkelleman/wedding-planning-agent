# Next Steps Guide

## Immediate Actions

### 1. Review Your Options
- [ ] Read through budget_summary.md for overview
- [ ] Check top_recommendations.md for curated picks
- [ ] Review restaurant_details.md for full information

### 2. Narrow Down Choices
Consider these factors:
- **Time of day:** Lunch, brunch, or dinner?
- **Style preference:** Seafood, steakhouse, or French?
- **Budget allocation:** Save money or splurge within budget?
- **Venue atmosphere:** Modern, historic, or classic?

### 3. Schedule Venue Visits
**Top 3 to Visit (Based on Value & Quality):**
1. **The Banks** - Most flexible pricing
2. **CLINK** - Verified quality, unique venue  
3. **Bistro du Midi** - Established reputation, great views

---

## Contact Information

### The Banks Seafood and Steak
- **Address:** Clarendon & Stuart Streets, Boston, MA
- **Team:** Chef Robert Sisca & Chris Himmel
- **Next Step:** Request private dining packet and schedule tour
- **Ask About:** Wine Suite, Fireplace Suite availability

### CLINK
- **Location:** Liberty Hotel, Boston, MA
- **Next Step:** Inquire about Liberty Hotel private events
- **Ask About:** Historic venue features, menu customization

### Bistro du Midi
- **Address:** 223 Columbus Avenue (Public Garden), Boston, MA
- **Chef:** Robert Sisca
- **Next Step:** Request private dining consultation
- **Ask About:** Public Garden view spaces, seasonal menu options

### Ostra
- **Address:** 1 Charles Street South, Boston, MA 02116
- **Phone:** (617) 421-1200
- **Next Step:** Request three-course dinner details

### Mistral
- **Address:** 223 Columbus Avenue, Boston, MA 02116
- **Phone:** (617) 867-9300
- **Next Step:** Inquire about Le Salon du Mistral

### Abe & Louie's
- **Location:** Back Bay, Boston
- **Email:** BostonEvents@TavistockRestaurants.com
- **Phone:** (617) 425-5206
- **Next Step:** Request brunch event details

---

## Questions to Ask Venues

### Availability & Logistics
- [ ] Is my preferred date available?
- [ ] What are the minimum/maximum guest counts?
- [ ] How long is the event space reserved?
- [ ] What is the deposit and payment schedule?
- [ ] What is the cancellation policy?

### Menu & Service
- [ ] Can I customize the menu?
- [ ] Are dietary restrictions accommodated?
- [ ] What does the service include (servers, bartenders, etc.)?
- [ ] Can we do a tasting before the event?
- [ ] Are beverages included or separate?

### Venue Details
- [ ] Can I tour the private dining space?
- [ ] What is included in the room setup?
- [ ] Is A/V equipment available?
- [ ] Where do cocktail hour and dinner take place?
- [ ] What are the parking/transportation options?

### Additional Costs
- [ ] Is the 20% gratuity mandatory?
- [ ] What is the exact tax rate?
- [ ] Are there any room fees or minimums?
- [ ] What about cake cutting fees?
- [ ] Any additional service charges?

---

## Budget Planning

### Your Current Budget: $5,000
**Includes:** Food, 20% gratuity, 10% tax for 25 guests

### Not Included in Venue Pricing
Consider budgeting separately for:
- **Flowers/Centerpieces:** $300-800
- **Photography:** $500-2,000+
- **Invitations:** $100-300
- **Favors:** $100-250
- **Music/Entertainment:** $300-1,500
- **Transportation:** $200-500
- **Wedding attire:** $500-2,000+

### Budget Tracking
Use the wedding planning agent's budget tracker skill:
```bash
python3 main.py skills execute budget_tracker --expenses '{"venue_deposit": 1000, "venue_balance": 2234}'
```

---

## Using the Wedding Planning Agent

### Negotiate Better Rates
```bash
# Analyze a quote
python3 main.py negotiate --vendor "The Banks" --amount 3234 --category catering

# Batch negotiate multiple quotes
python3 main.py negotiate-batch data/organized/catering/
```

### Compare Vendors Side-by-Side
```bash
python3 main.py skills execute vendor_comparison \
  --vendors '{"The Banks": {"price": 3234, "rating": 5}, "CLINK": {"price": 3102, "rating": 4.8}}'
```

### Generate Timeline
```bash
# Comprehensive timeline
python3 main.py skills execute timeline_generator --wedding_date "2026-06-15" --style comprehensive

# Minimal timeline
python3 main.py skills execute timeline_generator --wedding_date "2026-06-15" --style minimal
```

### Analyze Contracts
```bash
python3 main.py skills execute contract_analyzer --contract_text "$(cat vendor_contract.txt)"
```

---

## Decision Matrix

Use this to score your top choices:

| Factor (Weight) | The Banks | CLINK | Bistro du Midi |
|----------------|-----------|-------|----------------|
| **Price** (30%) | | | |
| **Food Quality** (25%) | | | |
| **Venue Beauty** (20%) | | | |
| **Location** (15%) | | | |
| **Flexibility** (10%) | | | |
| **TOTAL** | | | |

*Score each factor 1-10, multiply by weight percentage, sum for total*

---

## Recommended Timeline

### This Week
1. Review all analysis documents
2. Discuss preferences with partner
3. Create shortlist of 3-5 venues

### Next Week  
4. Contact top venues for availability
5. Schedule tours/tastings
6. Request detailed proposals

### Following Week
7. Compare final proposals
8. Make decision
9. Secure venue with deposit

---

## Files in This Analysis Folder

1. **budget_summary.md** - All options with costs
2. **top_recommendations.md** - Curated picks by category
3. **restaurant_details.md** - Full venue information
4. **next_steps.md** - This file (action plan)

---

## Need Help?

Use the wedding planning agent for:
- Budget tracking and recommendations
- Contract analysis and red flags
- Vendor comparison scoring
- Timeline generation
- Negotiation email drafting

Run `python3 main.py skills list` to see all available capabilities.
