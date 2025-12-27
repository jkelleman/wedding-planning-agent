"""
Negotiation agent for analyzing quotes and suggesting better rates.
"""
import re
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path


class NegotiationAgent:
    """Analyzes vendor quotes and helps negotiate better rates."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.budget = config.get('budget', {})
        self.negotiation_settings = config.get('negotiation', {})
        self.market_data = self._load_market_data()
    
    def analyze_quote(self, scan_result: Dict) -> Dict:
        """
        Analyze a vendor quote and identify negotiation opportunities.
        
        Args:
            scan_result: Result from DocumentScanner.scan_file()
        
        Returns:
            Analysis with negotiation strategies and talking points
        """
        metadata = scan_result.get('metadata', {})
        category = metadata.get('category', 'other')
        price = metadata.get('price')
        
        if not price:
            return {
                'status': 'error',
                'message': 'No price found in document'
            }
        
        analysis = {
            'vendor': metadata.get('venue_name', 'Unknown Vendor'),
            'category': category,
            'quoted_price': price,
            'budget_allocation': self.budget.get(category, 0),
            'over_budget': price > self.budget.get(category, 0),
            'negotiation_potential': self._assess_negotiation_potential(category, price),
            'suggested_counter_offer': self._calculate_counter_offer(category, price),
            'strategies': self._generate_strategies(category, price, metadata),
            'talking_points': self._generate_talking_points(category, price, metadata),
            'market_comparison': self._compare_to_market(category, price)
        }
        
        return analysis
    
    def draft_negotiation_email(self, analysis: Dict, tone: str = 'professional') -> str:
        """
        Draft a negotiation email based on analysis.
        
        Args:
            analysis: Result from analyze_quote()
            tone: 'professional', 'friendly', or 'firm'
        
        Returns:
            Formatted email text
        """
        vendor = analysis['vendor']
        quoted_price = analysis['quoted_price']
        counter_offer = analysis['suggested_counter_offer']
        category = analysis['category']
        
        email_templates = {
            'professional': self._professional_template,
            'friendly': self._friendly_template,
            'firm': self._firm_template
        }
        
        template_func = email_templates.get(tone, self._professional_template)
        return template_func(analysis)
    
    def _assess_negotiation_potential(self, category: str, price: float) -> str:
        """Assess how much room there is for negotiation."""
        market_avg = self.market_data.get(category, {}).get('average', price)
        
        if price > market_avg * 1.3:
            return 'HIGH - Significantly above market rate'
        elif price > market_avg * 1.1:
            return 'MEDIUM - Above market rate'
        elif price > market_avg * 0.9:
            return 'LOW - At market rate'
        else:
            return 'MINIMAL - Below market rate (good deal)'
    
    def _calculate_counter_offer(self, category: str, quoted_price: float) -> Dict:
        """Calculate a reasonable counter-offer."""
        budget_allocation = self.budget.get(category, quoted_price * 0.8)
        market_avg = self.market_data.get(category, {}).get('average', quoted_price * 0.9)
        
        # Strategy: Aim for 15-20% below quoted price, but not below market average
        target_reduction = quoted_price * 0.15
        counter_price = quoted_price - target_reduction
        
        # Don't go too low - maintain credibility
        min_reasonable = market_avg * 0.85
        counter_price = max(counter_price, min_reasonable)
        
        # Ideally within budget
        if counter_price > budget_allocation:
            counter_price = budget_allocation
        
        return {
            'amount': round(counter_price, 2),
            'reduction': round(quoted_price - counter_price, 2),
            'reduction_percentage': round((quoted_price - counter_price) / quoted_price * 100, 1),
            'rationale': self._explain_counter_offer(quoted_price, counter_price, market_avg, budget_allocation)
        }
    
    def _explain_counter_offer(self, quoted: float, counter: float, market: float, budget: float) -> str:
        """Explain the reasoning behind the counter-offer."""
        reasons = []
        
        if counter <= budget:
            reasons.append(f"aligns with our ${budget:,.0f} budget allocation")
        
        if quoted > market * 1.1:
            reasons.append(f"brings price closer to market average (${market:,.0f})")
        
        reduction_pct = (quoted - counter) / quoted * 100
        if reduction_pct >= 10:
            reasons.append("reflects a fair negotiation from both parties")
        
        return ", ".join(reasons)
    
    def _generate_strategies(self, category: str, price: float, metadata: Dict) -> List[str]:
        """Generate negotiation strategies based on context."""
        strategies = []
        
        # Budget-based strategy
        budget_allocation = self.budget.get(category, 0)
        if price > budget_allocation:
            strategies.append(f"Emphasize budget constraints (${budget_allocation:,.0f} allocated for {category})")
        
        # Market comparison strategy
        market_avg = self.market_data.get(category, {}).get('average', price)
        if price > market_avg * 1.15:
            strategies.append(f"Reference market rates (average: ${market_avg:,.0f})")
        
        # Package deal strategy
        strategies.append("Offer to book multiple services together for a discount")
        
        # Timing strategy
        strategies.append("Ask about off-season or weekday discounts")
        
        # Flexibility strategy
        if category == 'catering':
            strategies.append("Consider reducing guest count or simplifying menu options")
        elif category == 'venue':
            strategies.append("Inquire about shorter rental periods or alternative dates")
        
        # Competition strategy
        strategies.append("Mention you're comparing multiple vendors (creates urgency)")
        
        # Payment terms
        strategies.append("Offer upfront payment or flexible payment schedule in exchange for discount")
        
        return strategies
    
    def _generate_talking_points(self, category: str, price: float, metadata: Dict) -> List[str]:
        """Generate specific talking points for negotiation."""
        points = []
        
        budget_allocation = self.budget.get(category, 0)
        if price > budget_allocation:
            points.append(f"Our budget for {category} is ${budget_allocation:,.0f}")
        
        # Positive framing
        points.append(f"We love what you offer and want to work with you")
        
        # Market awareness
        market_avg = self.market_data.get(category, {}).get('average')
        if market_avg and price > market_avg:
            points.append(f"We've researched market rates for {category} in this area")
        
        # Multiple vendors
        points.append("We're evaluating several options and want to make a decision soon")
        
        # Flexibility
        points.append("We're flexible on dates/details if it helps with pricing")
        
        # Value proposition
        points.append("This is a significant investment for us and we want to ensure it's within budget")
        
        # Referral potential
        points.append("We'd be happy to provide testimonials and referrals for future clients")
        
        return points
    
    def _compare_to_market(self, category: str, price: float) -> Dict:
        """Compare quoted price to market averages."""
        market_info = self.market_data.get(category, {})
        average = market_info.get('average', price)
        low_end = market_info.get('low', average * 0.7)
        high_end = market_info.get('high', average * 1.3)
        
        position = 'average'
        if price < average * 0.9:
            position = 'below average'
        elif price > average * 1.15:
            position = 'above average'
        
        return {
            'market_average': average,
            'market_range': {'low': low_end, 'high': high_end},
            'position': position,
            'difference_from_avg': price - average,
            'difference_percentage': round((price - average) / average * 100, 1)
        }
    
    def _load_market_data(self) -> Dict:
        """Load market average pricing data."""
        # Default market data - in production, this could come from an API or database
        return {
            'venue': {
                'average': 12000,
                'low': 5000,
                'high': 25000
            },
            'catering': {
                'average': 8500,
                'low': 3500,
                'high': 15000
            },
            'floral': {
                'average': 2500,
                'low': 800,
                'high': 5000
            },
            'photography': {
                'average': 4000,
                'low': 1500,
                'high': 8000
            },
            'entertainment': {
                'average': 2000,
                'low': 800,
                'high': 5000
            }
        }
    
    def _professional_template(self, analysis: Dict) -> str:
        """Professional tone email template."""
        vendor = analysis['vendor']
        quoted = analysis['quoted_price']
        counter = analysis['suggested_counter_offer']
        category = analysis['category']
        
        email = f"""Subject: Re: {category.capitalize()} Quote - Following Up

Dear {vendor} Team,

Thank you for providing your detailed quote for our wedding {category}. We were impressed with your offerings and the quality of service you provide.

After carefully reviewing our overall wedding budget and comparing various options, we would like to discuss the pricing. Your quoted amount of ${quoted:,.2f} is slightly above our allocated budget for this category.

We would like to propose a revised price of ${counter['amount']:,.2f}, which represents a {counter['reduction_percentage']}% adjustment. This {counter['rationale']}.

We are very interested in working with you and believe this pricing would allow us to move forward confidently. We are flexible on certain details and would be happy to discuss how we can make this work for both parties.

Would you be available for a brief call this week to discuss this further? We are hoping to finalize our vendor selections soon and would love to include you in our plans.

Thank you for your consideration, and we look forward to hearing from you.

Best regards,
[Your Name]
"""
        return email
    
    def _friendly_template(self, analysis: Dict) -> str:
        """Friendly, warm tone email template."""
        vendor = analysis['vendor']
        quoted = analysis['quoted_price']
        counter = analysis['suggested_counter_offer']
        category = analysis['category']
        
        email = f"""Subject: Excited to Work Together! Quick Question on Pricing

Hi {vendor} team!

First off - we absolutely love what you do! Your {category} options are exactly what we've been dreaming of for our wedding.

We're working on finalizing everything and doing our best to stay within budget (you know how wedding planning goes! 😊). Your quote came in at ${quoted:,.2f}, and we're wondering if there's any flexibility to bring it closer to ${counter['amount']:,.2f}?

We're comparing a few options but honestly, you're our top choice. We're flexible on dates and details, and we'd love to find a way to make this work!

Any chance we could chat about this? We're ready to move forward quickly once we nail down the details.

Thanks so much for understanding, and we hope we can work together to make our day special!

Warmly,
[Your Name]
"""
        return email
    
    def _firm_template(self, analysis: Dict) -> str:
        """Firm, business-like tone email template."""
        vendor = analysis['vendor']
        quoted = analysis['quoted_price']
        counter = analysis['suggested_counter_offer']
        category = analysis['category']
        market = analysis['market_comparison']
        
        email = f"""Subject: {category.capitalize()} Quote Review - Revised Proposal

Dear {vendor},

Thank you for your quote dated [DATE]. We have completed our vendor evaluation process and are moving forward with final selections.

Your quoted price of ${quoted:,.2f} exceeds our budget allocation by ${quoted - self.budget.get(category, quoted):,.2f}. Based on market research, similar services in this area average ${market['market_average']:,.2f}.

We are prepared to move forward at ${counter['amount']:,.2f}, which we believe is a fair market rate that {counter['rationale']}.

This is our best and final offer. Please confirm by [DATE + 3 days] if you can accommodate this pricing, as we have alternative vendors prepared to move forward.

We appreciate your consideration and look forward to your prompt response.

Regards,
[Your Name]
"""
        return email
    
    def generate_negotiation_report(self, analyses: List[Dict]) -> str:
        """Generate a comprehensive negotiation report for multiple quotes."""
        lines = []
        lines.append("=" * 70)
        lines.append("WEDDING VENDOR NEGOTIATION REPORT")
        lines.append("=" * 70)
        lines.append(f"\nGenerated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
        
        total_quoted = sum(a['quoted_price'] for a in analyses)
        total_counter = sum(a['suggested_counter_offer']['amount'] for a in analyses)
        total_savings = total_quoted - total_counter
        
        lines.append(f"\nOVERALL SUMMARY")
        lines.append(f"  Total Quoted: ${total_quoted:,.2f}")
        lines.append(f"  Total Counter-Offers: ${total_counter:,.2f}")
        lines.append(f"  Potential Savings: ${total_savings:,.2f} ({total_savings/total_quoted*100:.1f}%)")
        lines.append(f"  Total Budget: ${self.budget.get('max_total', 0):,.2f}")
        
        lines.append(f"\n{'=' * 70}")
        lines.append("VENDOR-BY-VENDOR ANALYSIS")
        lines.append("=" * 70)
        
        for i, analysis in enumerate(analyses, 1):
            lines.append(f"\n{i}. {analysis['vendor']} ({analysis['category'].upper()})")
            lines.append(f"   {'─' * 65}")
            lines.append(f"   Quoted Price: ${analysis['quoted_price']:,.2f}")
            lines.append(f"   Suggested Counter: ${analysis['suggested_counter_offer']['amount']:,.2f}")
            lines.append(f"   Potential Savings: ${analysis['suggested_counter_offer']['reduction']:,.2f} ({analysis['suggested_counter_offer']['reduction_percentage']}%)")
            lines.append(f"   Negotiation Potential: {analysis['negotiation_potential']}")
            
            market = analysis['market_comparison']
            lines.append(f"\n   Market Comparison:")
            lines.append(f"     • Market Average: ${market['market_average']:,.2f}")
            lines.append(f"     • This Quote: {market['position']} (${market['difference_from_avg']:+,.2f})")
            
            lines.append(f"\n   Negotiation Strategies:")
            for strategy in analysis['strategies'][:4]:  # Top 4 strategies
                lines.append(f"     • {strategy}")
            
            lines.append(f"\n   Key Talking Points:")
            for point in analysis['talking_points'][:3]:  # Top 3 points
                lines.append(f"     • {point}")
        
        lines.append(f"\n{'=' * 70}")
        lines.append("NEXT STEPS")
        lines.append("=" * 70)
        lines.append("\n1. Review each vendor's negotiation potential")
        lines.append("2. Draft personalized emails using the 'negotiate' command")
        lines.append("3. Schedule follow-up calls within 3-5 business days")
        lines.append("4. Be prepared to walk away from vendors significantly over budget")
        lines.append("5. Consider package deals when negotiating multiple services")
        
        return "\n".join(lines)
