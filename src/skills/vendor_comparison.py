"""
Vendor Comparison Skill - Creates side-by-side comparisons of multiple vendors.
"""
from typing import Dict, Any, List
from pathlib import Path
from .base_skill import BaseSkill


class VendorComparisonSkill(BaseSkill):
    """Generates side-by-side vendor comparisons to help with decision making."""
    
    @property
    def name(self) -> str:
        return "vendor_comparison"
    
    @property
    def description(self) -> str:
        return "Creates detailed side-by-side comparisons of multiple vendors in the same category"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def category(self) -> str:
        return "analysis"
    
    def execute(self, category: str = None, vendors: List[Dict] = None) -> Dict[str, Any]:
        """
        Compare multiple vendors.
        
        Args:
            category: Category to compare (venue, catering, etc.)
            vendors: List of vendor dictionaries with keys: name, price, pros, cons, rating
        
        Returns:
            Formatted comparison table and recommendation
        """
        if not vendors or len(vendors) < 2:
            return {
                'status': 'error',
                'message': 'Must provide at least 2 vendors to compare'
            }
        
        comparison = self._create_comparison(category or "Vendors", vendors)
        recommendation = self._generate_recommendation(vendors)
        
        return {
            'status': 'success',
            'result': {
                'category': category,
                'vendor_count': len(vendors),
                'comparison_table': comparison,
                'recommendation': recommendation,
                'summary': self._create_summary(vendors)
            }
        }
    
    def _create_comparison(self, category: str, vendors: List[Dict]) -> str:
        """Create a formatted comparison table."""
        lines = []
        lines.append(f"\n{'='*80}")
        lines.append(f"{category.upper()} VENDOR COMPARISON")
        lines.append(f"{'='*80}\n")
        
        # Determine fields to compare
        all_fields = set()
        for vendor in vendors:
            all_fields.update(vendor.keys())
        
        # Standard fields in specific order
        standard_fields = ['name', 'price', 'rating', 'capacity', 'pros', 'cons']
        other_fields = sorted(all_fields - set(standard_fields) - {'pros', 'cons'})
        fields_order = [f for f in standard_fields if f in all_fields] + other_fields
        
        # Create comparison rows
        for field in fields_order:
            if field == 'name':
                continue  # Names are headers
            
            lines.append(f"\n{field.upper().replace('_', ' ')}")
            lines.append("─" * 80)
            
            for vendor in vendors:
                vendor_name = vendor.get('name', 'Unknown')
                value = vendor.get(field, 'N/A')
                
                # Format different types of values
                if field == 'price' and isinstance(value, (int, float)):
                    value = f"${value:,.2f}"
                elif field == 'rating' and isinstance(value, (int, float)):
                    stars = '★' * int(value) + '☆' * (5 - int(value))
                    value = f"{stars} ({value}/5)"
                elif field == 'pros' and isinstance(value, list):
                    value = '\n     • ' + '\n     • '.join(value)
                elif field == 'cons' and isinstance(value, list):
                    value = '\n     • ' + '\n     • '.join(value)
                
                lines.append(f"  {vendor_name}: {value}")
        
        return '\n'.join(lines)
    
    def _generate_recommendation(self, vendors: List[Dict]) -> Dict[str, Any]:
        """Generate a recommendation based on vendor comparison."""
        # Score each vendor
        scored_vendors = []
        
        for vendor in vendors:
            score = 0
            reasons = []
            
            # Price scoring (lower is better, but not too low)
            price = vendor.get('price', 0)
            if price:
                prices = [v.get('price', float('inf')) for v in vendors if v.get('price')]
                avg_price = sum(prices) / len(prices) if prices else price
                
                if price < avg_price * 0.8:
                    score += 30
                    reasons.append("Excellent price point")
                elif price < avg_price:
                    score += 20
                    reasons.append("Good value")
                elif price < avg_price * 1.2:
                    score += 10
                    reasons.append("Fair pricing")
            
            # Rating scoring
            rating = vendor.get('rating', 0)
            if rating >= 4.5:
                score += 30
                reasons.append("Outstanding reviews")
            elif rating >= 4.0:
                score += 20
                reasons.append("Highly rated")
            elif rating >= 3.5:
                score += 10
                reasons.append("Good reviews")
            
            # Pros/cons balance
            pros_count = len(vendor.get('pros', []))
            cons_count = len(vendor.get('cons', []))
            
            if pros_count > cons_count * 2:
                score += 20
                reasons.append("Strong advantages")
            elif pros_count > cons_count:
                score += 10
            
            scored_vendors.append({
                'vendor': vendor,
                'score': score,
                'reasons': reasons
            })
        
        # Sort by score
        scored_vendors.sort(key=lambda x: x['score'], reverse=True)
        
        winner = scored_vendors[0]
        
        return {
            'recommended_vendor': winner['vendor'].get('name', 'Unknown'),
            'score': winner['score'],
            'reasons': winner['reasons'],
            'runner_up': scored_vendors[1]['vendor'].get('name', 'Unknown') if len(scored_vendors) > 1 else None
        }
    
    def _create_summary(self, vendors: List[Dict]) -> str:
        """Create a brief summary of the comparison."""
        vendor_names = [v.get('name', 'Unknown') for v in vendors]
        prices = [v.get('price', 0) for v in vendors if v.get('price')]
        
        summary_parts = [
            f"Comparing {len(vendors)} vendors: {', '.join(vendor_names)}"
        ]
        
        if prices:
            price_range = f"${min(prices):,.0f} - ${max(prices):,.0f}"
            summary_parts.append(f"Price range: {price_range}")
        
        return "; ".join(summary_parts)
