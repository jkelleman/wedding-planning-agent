# Wedding Planning Agent - Repository Structure

This repository is organized to help you plan an intimate wedding or elopement celebration. It's designed to be both a working planning tool and a template for future brides.

---

## 📁 Repository Organization

### `/planning/` - YOUR WEDDING PLANNING FILES
This is where YOUR specific wedding planning documents live. These are customized for your event.

#### `/planning/01_venue_and_catering/`
**Purpose:** Venue selection, menu planning, cost analysis, and vendor communications for your reception venue.

**Files:**
- `venue_cost_analysis.md` - Complete cost breakdown with menu, beverages, fees
- `vendor_inquiry_email.txt` - Email to send to venue with questions and menu selections
- `vendor_inquiry_email_formatted.txt` - Formatted version for Gmail/Outlook
- `guest_invitation_details.txt` - Guest-facing information about venue, menu, timing
- `guest_invitation_details_formatted.txt` - Formatted version for Word/email

**Why this structure:** Keep all venue-related documents together so you can easily reference costs, send inquiries, and share details with guests.

---

#### `/planning/02_photography/`
**Purpose:** Photographer research, vendor selection, timeline planning, and day-of logistics.

**Files:**
- `photographer_comparison.md` - Analysis of 15+ photographers with pricing, BPL experience, recommendations
- `photographer_contacts.md` - Complete contact info (emails, phones) for all photographers
- `photographer_inquiry_email.txt` - Email templates to send photographers
- `wedding_day_timeline_and_logistics.md` - Detailed timeline, shot list, location logistics, planning checklist

**Why this structure:** Separates research/selection phase from execution planning. Easy to share timeline with photographer once booked.

---

#### `/planning/03_music/`
**Purpose:** Music planning for ceremony, cocktail hour, and reception.

**Files:**
- `playlist_planning.md` - Music needs by timeline section, delivery options, questions

**Why this structure:** Music planning separate from other vendors. Can be expanded with specific playlists once finalized.

---

#### `/planning/04_other_vendors/` (Future)
**Purpose:** Florals, officiant, transportation, accommodations, etc.

**Files:** (Add as you plan these elements)
- Florist research and quotes
- Officiant contact and ceremony script
- Hotel blocks
- Transportation logistics

---

### `/templates/` - REUSABLE TEMPLATES FOR OTHER BRIDES
These are blank templates that can be copied and customized for any wedding. Share these with friends!

#### `/templates/venue_and_catering/`
- `venue_cost_analysis_template.md` - Blank cost breakdown worksheet
- `vendor_inquiry_email_template.txt` - Customizable vendor inquiry email
- `guest_invitation_template.txt` - Blank guest information document

#### `/templates/photography/`
- `photographer_comparison_template.md` - Worksheet for comparing photographers
- `photographer_inquiry_template.txt` - Email template for photographer outreach
- `wedding_timeline_template.md` - Blank timeline worksheet with shot list
- `photography_questions_checklist.md` - Questions to ask photographers

#### `/templates/music/`
- `playlist_planning_template.md` - Music planning worksheet

#### `/templates/budget/`
- `budget_tracker_template.md` - Overall wedding budget tracker
- `vendor_comparison_template.md` - Generic vendor comparison worksheet

---

### `/data/` - RAW VENDOR MATERIALS
**Purpose:** Store PDFs, brochures, and raw materials from vendors.

**Structure:**
```
/data/
  /organized/
    /catering/      - Restaurant menus, pricing sheets
    /entertainment/ - DJ/band info
    /floral/        - Florist catalogs
    /photography/   - Photographer portfolios
    /venue/         - Venue contracts, floor plans
    /other/         - Miscellaneous
  /raw/             - Unsorted vendor materials
```

**Why this structure:** Keep original vendor documents organized by category. Easy to reference when making decisions.

---

### `/src/` - AUTOMATION TOOLS (Optional)
**Purpose:** Python scripts to help automate wedding planning tasks.

**Files:**
- `scanner.py` - Scan and extract text from vendor PDFs
- `organizer.py` - Organize vendor documents
- `recommender.py` - Analyze and recommend vendors
- `negotiator.py` - Help draft negotiation emails

**Why this structure:** If you're tech-savvy, these tools can help. If not, you can ignore this folder.

---

### `/outputs/` - GENERATED REPORTS (Optional)
**Purpose:** Auto-generated analysis from Python scripts.

---

## ️ How to Use This Repository

### For Your Own Wedding:
1. **Start in `/planning/`** - This is YOUR workspace
2. **Copy vendor materials to `/data/`** - Keep PDFs organized
3. **Use existing files as examples** - Customize for your needs
4. **Reference `/templates/`** - If you need a fresh start on any document

### To Share With Other Brides:
1. **Point them to `/templates/`** - These are the reusable documents
2. **Share the README.md** - Explains how to use the system
3. **They copy templates to their own `/planning/` folder** - Customize for their event

---

## 📋 Suggested Workflow

### Phase 1: Research & Budget (Weeks 1-4)
- Set overall budget
- Research venues, photographers, vendors
- Use comparison templates to evaluate options

### Phase 2: Vendor Selection & Booking (Weeks 5-12)
- Send inquiry emails using templates
- Compare quotes and availability
- Book vendors and pay deposits
- Store contracts in `/data/organized/`

### Phase 3: Detailed Planning (Weeks 13-8 before)
- Finalize menu selections
- Create detailed photography timeline
- Plan music playlists
- Draft guest communications

### Phase 4: Final Coordination (Weeks 8-1 before)
- Send final details to vendors
- Share timeline with photographer
- Create day-of coordination documents
- Confirm all logistics

### Phase 5: Enjoy Your Wedding! 

---

##  Tips for Using This System

**Keep it organized:**
- One folder per vendor category
- Date your files if creating multiple versions
- Use descriptive filenames

**Make it reusable:**
- When you create a useful document, also create a blank template version
- Add it to `/templates/` for future brides

**Stay flexible:**
- Not every bride needs every folder
- Add folders as needed for your specific vendors
- Delete folders you won't use

**Share the love:**
- If this system helped you, share it with engaged friends
- Contribute improvements back to the template

---

##  Quick Reference: Where Do I Find...?

| What I Need | Where to Look |
|-------------|---------------|
| My venue cost breakdown | `/planning/01_venue_and_catering/venue_cost_analysis.md` |
| Email to send to venue | `/planning/01_venue_and_catering/vendor_inquiry_email.txt` |
| Photographer comparison | `/planning/02_photography/photographer_comparison.md` |
| Wedding day photo timeline | `/planning/02_photography/wedding_day_timeline_and_logistics.md` |
| Music planning | `/planning/03_music/playlist_planning.md` |
| Blank templates to start fresh | `/templates/` (by category) |
| Vendor PDFs and brochures | `/data/organized/` (by category) |
| Budget tracking | Create from `/templates/budget/budget_tracker_template.md` |

---

## 🤝 Contributing

If you found this repository helpful and created additional useful templates or documents, consider:
- Adding them to the `/templates/` folder
- Updating this README with tips
- Sharing with other brides planning intimate weddings

**This repository is designed to be a gift to the wedding planning community!** ️
