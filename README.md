# Wedding Planning Agent

**A conversation design case study: what does an agent need to say so people can make high-stakes decisions with confidence?**

I'm Jen Kelleman, a content and conversation designer who works on AI agents. I built this agent while planning a small wedding in Boston, because the hard part wasn't finding vendors. It was knowing what to ask, how to ask it, and whether to trust the answers.

This repo is the working agent plus the real messages it helped me write. It's a portfolio piece about the words an agent produces: how it explains itself, how it adapts its tone, and how it turns messy input into a message someone can actually send.

---

## The problem was a conversation problem

I collected about 68 vendor PDFs, menus, and email threads from 11 restaurants. Every one used different language for pricing, minimums, fees, and dietary accommodation. The data was messy, but the bigger issue was the back-and-forth:

- **I didn't know what to ask.** Each vague inquiry led to two more rounds of email.
- **Recommendations without reasons were useless.** "This one's a good fit" doesn't help when you're spending thousands of dollars.
- **Tone mattered and was hard to get right.** Asking a vendor to come down on price is uncomfortable. Too soft and nothing changes; too firm and you burn the relationship.
- **Different audiences needed different messages.** Vendors needed precise, numbered questions. Family needed warmth and wayfinding.

So I designed the agent's output first, then built the system to produce it.

---

## Conversation design decisions

### 1. Every recommendation explains itself

The agent never returns a bare score. Each ranked option comes with plain-language reasons, written so a person can disagree with one specific reason instead of distrusting the whole result:

```
Score: 76/100
Why:  Within budget ($8,000 <= $10,000)
      Matches dietary needs: vegetarian, gluten-free
```

Counter-offers work the same way. The agent tells you *why* a number is reasonable ("aligns with our $10,000 budget allocation, brings price closer to market average") so you can say it out loud with a straight face.

**Principle:** Show the reasoning in the user's terms, not the model's. Trust comes from being able to check the work.

### 2. Tone is a parameter, not an accident

The negotiation agent drafts the same request in three registers: **professional**, **friendly**, and **firm**. Same facts, same counter-offer, different relationship posture:

| Tone | Opens with | Closes with | Use when |
|---|---|---|---|
| Friendly | Enthusiasm for the vendor | An invitation to chat | You want this vendor and the gap is small |
| Professional | Thanks and context | A request for a short call | Default; keeps options open |
| Firm | Evaluation is complete | A deadline and alternatives | You have real alternatives and a hard budget |

Tone is set in `config.yaml` (`default_tone`) or per command (`--tone`), so the choice is deliberate and reversible.

**Principle:** Separate *what* the agent says from *how* it says it, and give the person control of the how.

### 3. Structure the ask to cut the back-and-forth

The vendor inquiry email in [`examples/planning/01_venue_and_catering/vendor_inquiry_email.txt`](examples/planning/01_venue_and_catering/vendor_inquiry_email.txt) is the clearest example. Instead of "Can you tell me more?", it:

- States the selection and the math up front, so the vendor can correct a wrong assumption immediately
- Groups 21 numbered questions by topic (dietary, beverages, logistics, fees, next steps) so the reply can be numbered too
- Names constraints plainly (strict gluten-free, nut-free, many non-drinkers) without over-explaining anyone's reasons

One email replaced what would have been several rounds of clarification.

**Principle:** Design the message for the reply you want back.

### 4. Write for the reader in front of you

The same event produced two very different pieces of content:

- **For the venue:** dense, numbered, cost-transparent
- **For family** ([`guest_invitation_details.txt`](examples/planning/01_venue_and_catering/guest_invitation_details.txt)): warm, scannable, organized around the questions guests actually have (where, when, what's to eat, what to tell us)

**Principle:** Audience first. The facts don't change; the shape, order, and voice do.

### 5. Examples beside templates

Every worked example in `examples/` has a blank, reusable counterpart in `templates/`. People learn the pattern by seeing it filled in, then adapt it. This is the same approach I use for agent prompt and response guidelines: show the good output, then hand over the scaffold.

---

## What came out of it

- **68 vendor documents → 18 realistic options** in an afternoon, filtered by budget, capacity, and dietary needs
- **Two budget scenarios** ([$5,000](examples/analysis_5000/) and [$6,700](examples/analysis_6500/)) compared side by side, so the tradeoffs were visible before committing
- **A final venue proposal** at about $5,400 for 20 guests, under the $6,700 ceiling, with every fee broken out
- **9 reusable templates** for venue, catering, photography, music, and budgeting

The metric I cared about most was confidence. Before: "I have no idea if this is a good price." After: "I know where this sits in the market, what I'm optimizing for, and what I'm trading away." I didn't end up sending the firm negotiation email, but having a draft I trusted changed how I walked into every conversation.

---

## How it works

```
Vendor PDFs, menus, screenshots
        │
        ▼
  scan       → OCR + text extraction (Tesseract, PyPDF2)
  organize   → category, vendor, and price pulled into structured metadata
  recommend  → transparent fit score + plain-language reasons
  negotiate  → market comparison, counter-offer, drafted email in your chosen tone
  skills     → contract red flags, planning timeline, budget tracking, vendor comparison
```

The fit score is deliberately simple so it can be explained in a sentence: start at 50, add points for coming in under budget, matching dietary needs, and fitting the guest count; subtract for going over budget or being too small.

### Run it

```bash
pip install -r requirements.txt
brew install tesseract          # or your OS's package manager

python main.py init                                   # create working folders
python main.py organize --input-dir examples/data/raw   # try it on the fictional samples
python main.py recommend --input-dir examples/data/raw
python main.py negotiate path/to/quote.pdf --draft --tone friendly
python main.py skills list
```

Set your budget, guest count, dietary needs, and default tone in `config.yaml`. See [`docs/QUICKSTART.md`](docs/QUICKSTART.md) for the full walkthrough.

---

## Repository map

```
examples/
  planning/01_venue_and_catering/   Real vendor inquiry + guest-facing details
  analysis_5000/                    $5,000 scenario: recommendations, negotiation, next steps
  analysis_6500/                    $6,700 scenario and comparison
  data/raw/                         Fictional sample vendor files to try the agent on
templates/                          Blank, reusable versions of every worksheet and message
src/
  scanner.py      recommender.py    organizer.py    negotiator.py
  skills/         Plugin skills sharing one interface (name, description, execute)
docs/QUICKSTART.md
config.yaml       Budget, preferences, and tone
main.py           CLI
```

Personal vendor files, screenshots, and generated output are git-ignored and stay local.

---

## What I'd do next

- Put an LLM behind the drafting step, with the current templates as the style guide and the reasons list as grounding
- Let the agent read vendor replies and map answers back to the numbered questions
- Add a "tone check" that flags when a draft drifts from the selected register

---

## Let's talk

I'm interested in content and conversation design roles for AI agents: agent voice and tone, explainability, and the messages that sit between a model's output and a person's decision.

- **Portfolio:** [jkelleman.com](https://www.jkelleman.com)
- **LinkedIn:** [linkedin.com/in/jenniferkelleman](https://www.linkedin.com/in/jenniferkelleman)
- **Writing:** [AI with Jen](https://aiwithjen.com) · [Medium](https://medium.com/@jenkelleman)
- **GitHub:** [@jkelleman](https://github.com/jkelleman)

## License

MIT
