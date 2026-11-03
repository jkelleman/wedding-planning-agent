# Wedding Planning Agent

I design how AI agents talk to people. This one started with my own wedding.

Twenty guests, eleven Boston restaurants, 68 vendor PDFs. Every menu priced things differently, and I couldn't tell if $130 a head was a steal or a scam.

Organizing the PDFs was the easy part. The hard part was the conversation around them: what to ask, how to ask it, and whether to trust the answer. That's a design problem, so I designed for it.

## The design problem

Three questions shaped everything the agent says.

**Why should I trust this?** A ranked list with no reasons just made me second-guess it.

**How do I say this?** Asking a stranger to lower their price is awkward. Get the tone wrong and you lose the deal or the relationship.

**Who's reading?** A venue manager and my family need the same facts in completely different shapes.

## Trust: show the reasons

Every recommendation comes with its reasons attached, in words you can check against the menu in front of you.

```
Score: 76/100
Why:  Within budget ($8,000 <= $10,000)
      Matches dietary needs: vegetarian, gluten-free
```

Disagree with a result? Point at the line you disagree with. Counter-offers work the same way. The agent hands you the sentence that defends the number, which was the part I actually needed before hitting send.

## Tone: let the person choose

Same request, same number, three voices.

**Friendly** opens with "First off - we absolutely love what you do!" Use it when you've already fallen for the place.

**Professional** thanks them, states the budget, and asks for a call. It's the default because it keeps every door open.

**Firm** cites the market rate and says "This is our best and final offer." Only use it if you'd really walk.

I never sent the firm one. Knowing it was ready still made every vendor conversation easier.

## Audience: write for the reply you want

The easy email says "Could you tell me more about your dinner packages?" and gets back a PDF you already have.

[The one I sent](examples/planning/01_venue_and_catering/vendor_inquiry_email.txt) spells out my picks and my math so they can correct me early. It asks 21 numbered questions, grouped so they can answer by number. It names our gluten-free, nut-free, and non-drinking guests without making anyone explain themselves. And it asks them to box up the leftovers, because I was not leaving lobster bisque behind.

My family got [a different version](examples/planning/01_venue_and_catering/guest_invitation_details.txt): where, when, what's for dinner, and tell us about allergies. Same party, written for people who mostly wanted to know about dessert.

## What happened

68 documents became 18 real options in one afternoon. I compared a [$5,000 plan](examples/analysis_5000/) with a [$6,700 one](examples/analysis_6500/), and landed at about $5,400 for 20 guests with every fee visible.

I went from "is this a good price?" to knowing exactly what I was paying for and what I was giving up.

## Try it

```bash
pip install -r requirements.txt
brew install tesseract

python main.py organize --input-dir examples/data/raw    # fictional sample vendors
python main.py recommend --input-dir examples/data/raw
python main.py negotiate path/to/quote.pdf --draft --tone friendly
```

Set your budget, guests, dietary needs, and default tone in `config.yaml`. The [quickstart](docs/QUICKSTART.md) covers the rest. Every worked example in `examples/` has a blank copy in `templates/`.

Under the hood: OCR pulls text from PDFs and photos, a simple scorer ranks options (start at 50, gain or lose points for budget, diet, and capacity), and the negotiator drafts emails from tone templates.

## Next

Put a language model behind the drafts, with these templates as its style guide. Teach it to match a vendor's reply to the questions it answers. Add a check that catches a "friendly" email drifting firm.

## Say hi

I'm looking for content and conversation design work on AI agents.

[Portfolio](https://www.jkelleman.com) · [LinkedIn](https://www.linkedin.com/in/jenniferkelleman) · [AI with Jen](https://aiwithjen.com) · [Medium](https://medium.com/@jenkelleman)

MIT License
