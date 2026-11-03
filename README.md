# Wedding Planning Agent

I'm Jen Kelleman, and I design how AI agents talk to people. I built this one while planning a 20-person wedding in Boston, when I had 68 vendor PDFs from 11 restaurants, 15 browser tabs, three spreadsheets, and no idea whether $130 a head was a good deal or a bad one.

Sorting the PDFs turned out to be the easy part. What I kept getting stuck on was the writing. What do I ask this restaurant? How do I ask a stranger to lower their price without sounding cheap or rude? Why should I believe a spreadsheet that says one venue is a better fit than another? Every one of those is a conversation design question, so I treated the project like one.

## Making the agent show its work

A ranked list of venues didn't help me much. I'd look at the top pick and wonder what the agent knew that I didn't. So the recommender attaches its reasons to every result, in words I could check against the menu sitting next to me:

```
Score: 76/100
Why:  Within budget ($8,000 <= $10,000)
      Matches dietary needs: vegetarian, gluten-free
```

If I disagreed with a result, I could point at the exact line I disagreed with. Maybe I didn't care about the budget headroom, or maybe "matches gluten-free" needed a phone call to confirm. Either way I knew what to argue with.

The negotiation helper does the same with counter-offers. It doesn't just suggest a number. It writes the sentence you'd use to defend it ("aligns with our $10,000 budget allocation, brings price closer to market average"), which was the part I actually needed before hitting send.

## Three ways to ask for a discount

Asking a vendor to come down on price is awkward, and how awkward depends on how much you want them. So the agent writes the same request three ways, and you pick. Here's how each version opens and closes, straight from the templates:

**Friendly** starts with "First off - we absolutely love what you do!" and ends by asking for a quick chat. It's for when you've already fallen for the place and the gap is small.

**Professional** thanks them, explains the budget plainly, and asks for a short call. This is the default, because it keeps every door open.

**Firm** says the evaluation is finished, cites the market average, and closes with "This is our best and final offer" plus a deadline. Use it only if you'd genuinely walk away.

The facts and the number stay identical across all three. Only the relationship changes. You set your usual tone in `config.yaml` and override it per email with `--tone`.

I never sent the firm one. Knowing it was ready still made every vendor conversation easier.

## Asking for the reply you want

The [vendor inquiry](examples/planning/01_venue_and_catering/vendor_inquiry_email.txt) I sent our venue is the piece of writing I'm proudest of in this repo. The easy version would have been "Could you tell me more about your dinner packages?", which is a great way to get back a PDF you already have and nothing else.

The version I sent lays out exactly what I'd picked and what I thought it would cost, down to how many crab cake sliders, so they could correct my math before we went any further. Then it asks 21 numbered questions, grouped by dietary needs, drinks, timing, fees, and next steps, so they could answer by number. It explains that some guests need strictly gluten-free food and one needs nut-free, and that about half won't be drinking, without making anyone justify why. And it ends by asking them to box up the leftovers, because I was not leaving lobster bisque behind.

## Same party, different reader

The venue got a dense, numbered, every-fee-listed email. My family got [something else](examples/planning/01_venue_and_catering/guest_invitation_details.txt) entirely: where to go, which room, when cocktails start, what's on the menu, and a nudge to tell us about allergies. Same event and same facts, written for people who wanted to know if there'd be dessert.

Every finished example in `examples/` has a blank version in `templates/`. That's how I like to write guidelines for agents, too. Show a good one first, then hand over the empty frame.

## Where it landed

The agent narrowed 68 documents down to 18 realistic options in an afternoon. I compared a [$5,000 plan](examples/analysis_5000/) against a [$6,700 one](examples/analysis_6500/) side by side, and the final proposal came in around $5,400 for 20 guests with every fee spelled out. The nine templates have since been passed around to a few friends who are planning their own.

The real difference was in my head. I started out thinking "I have no idea if this is a good price." By the end I knew where each quote sat against the market, what I cared about most, and what I was giving up to get it.

## How it works

```
Vendor PDFs, menus, screenshots
        │
        ▼
  scan       OCR and text extraction (Tesseract, PyPDF2)
  organize   pulls category, vendor, and price into metadata
  recommend  fit score with the reasons attached
  negotiate  market comparison, counter-offer, and a drafted email in your tone
  skills     contract red flags, timelines, budget tracking, vendor comparison
```

I kept the scoring simple enough to explain in one breath. Every option starts at 50, gains points for coming in under budget, covering your dietary needs, and fitting your guest count, and loses points for going over budget or being too small.

To try it:

```bash
pip install -r requirements.txt
brew install tesseract          # or your OS's package manager

python main.py init
python main.py organize --input-dir examples/data/raw    # runs on the fictional samples
python main.py recommend --input-dir examples/data/raw
python main.py negotiate path/to/quote.pdf --draft --tone friendly
python main.py skills list
```

Put your own budget, guest count, dietary needs, and tone in `config.yaml`. [`docs/QUICKSTART.md`](docs/QUICKSTART.md) walks through the rest.

```
examples/
  planning/01_venue_and_catering/   the real venue email and the family details
  analysis_5000/, analysis_6500/    the two budget scenarios
  data/raw/                         fictional vendor files to experiment with
templates/                          blank versions of every worksheet and message
src/                                scanner, organizer, recommender, negotiator, skills/
config.yaml                         budget, preferences, tone
main.py                             command line
```

Real vendor files and anything the agent generates stay on your machine. They're git-ignored.

## If I kept going

I'd put a language model behind the drafting step and give it these templates as its style guide and the reasons list as its facts. I'd teach it to read a vendor's reply and match each answer to the question it belongs to. And I'd add a tone check that catches a "friendly" email quietly turning into a firm one.

## Say hi

I'm looking for content and conversation design work on AI agents, especially the messages that sit between what a model figures out and what a person decides to do about it.

[Portfolio](https://www.jkelleman.com) · [LinkedIn](https://www.linkedin.com/in/jenniferkelleman) · [AI with Jen](https://aiwithjen.com) · [Medium](https://medium.com/@jenkelleman) · [GitHub](https://github.com/jkelleman)

MIT License
