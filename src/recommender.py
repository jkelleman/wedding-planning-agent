"""
Recommendation engine for suggesting best options based on preferences.
"""
from typing import Dict, List
from pathlib import Path


class WeddingRecommender:
    """Provides recommendations based on budget, preferences, and scanned data."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.budget = config['budget']
        self.preferences = config['preferences']
    
    def analyze_options(self, organized_results: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Analyze organized files and provide categorized recommendations.
        
        Returns:
            Dict with recommendations by category.
        """
        # Group by category
        by_category = {}
        for result in organized_results:
            if result.get("status") != "success":
                continue
            
            category = result.get("category", "other")
            if category not in by_category:
                by_category[category] = []
            
            by_category[category].append(result)
        
        # Generate recommendations for each category
        recommendations = {}
        for category, items in by_category.items():
            recommendations[category] = self._rank_category_options(category, items)
        
        return recommendations
    
    def _rank_category_options(self, category: str, items: List[Dict]) -> List[Dict]:
        """Rank options within a category based on fit to budget and preferences."""
        ranked = []
        
        for item in items:
            metadata = item.get("scan_metadata", {})
            score = self._calculate_fit_score(category, metadata)
            
            ranked_item = {
                "file": item["new_path"],
                "score": score,
                "price": metadata.get("price"),
                "capacity": metadata.get("capacity"),
                "dietary_options": metadata.get("dietary_options", []),
                "reasons": []
            }
            
            # Add reasons for ranking
            if metadata.get("price"):
                budget_for_category = self.budget.get(category, self.budget['max_total'] * 0.2)
                if metadata["price"] <= budget_for_category:
                    ranked_item["reasons"].append(f"Within budget (${metadata['price']:,.0f} <= ${budget_for_category:,.0f})")
                else:
                    ranked_item["reasons"].append(f"Over budget (${metadata['price']:,.0f} > ${budget_for_category:,.0f})")
            
            if category == "catering" and metadata.get("dietary_options"):
                pref_dietary = set(self.preferences.get("dietary_restrictions", []))
                found_dietary = set(metadata["dietary_options"])
                matches = pref_dietary.intersection(found_dietary)
                if matches:
                    ranked_item["reasons"].append(f"Matches dietary needs: {', '.join(matches)}")
            
            if metadata.get("capacity"):
                guest_count = self.preferences.get("guest_count", 100)
                if metadata["capacity"] >= guest_count:
                    ranked_item["reasons"].append(f"Sufficient capacity ({metadata['capacity']} >= {guest_count} guests)")
            
            ranked.append(ranked_item)
        
        # Sort by score (descending)
        ranked.sort(key=lambda x: x["score"], reverse=True)
        
        return ranked
    
    def _calculate_fit_score(self, category: str, metadata: Dict) -> float:
        """Calculate how well an option fits user preferences (0-100)."""
        score = 50.0  # Base score
        
        # Budget fit
        if metadata.get("price"):
            budget_for_category = self.budget.get(category, self.budget['max_total'] * 0.2)
            price_ratio = metadata["price"] / budget_for_category
            if price_ratio <= 1.0:
                # Within budget: higher score the cheaper it is
                score += 30 * (1.0 - price_ratio)
            else:
                # Over budget: penalize
                score -= 40 * (price_ratio - 1.0)
        
        # Dietary preferences (for catering)
        if category == "catering" and metadata.get("dietary_options"):
            pref_dietary = set(self.preferences.get("dietary_restrictions", []))
            found_dietary = set(metadata["dietary_options"])
            match_count = len(pref_dietary.intersection(found_dietary))
            if pref_dietary:
                score += 20 * (match_count / len(pref_dietary))
        
        # Capacity fit (for venue)
        if category == "venue" and metadata.get("capacity"):
            guest_count = self.preferences.get("guest_count", 100)
            capacity_ratio = metadata["capacity"] / guest_count
            if capacity_ratio >= 1.0 and capacity_ratio <= 1.5:
                # Ideal capacity: not too small, not too large
                score += 15
            elif capacity_ratio < 1.0:
                # Too small
                score -= 30
        
        # Ensure score is between 0 and 100
        return max(0.0, min(100.0, score))
    
    def generate_report(self, recommendations: Dict[str, List[Dict]]) -> str:
        """Generate a human-readable report."""
        lines = []
        lines.append("=" * 60)
        lines.append("WEDDING PLANNING RECOMMENDATIONS")
        lines.append("=" * 60)
        lines.append(f"\nBudget Summary:")
        lines.append(f"  Max Total: ${self.budget['max_total']:,}")
        for category, amount in self.budget.items():
            if category != 'max_total':
                lines.append(f"  {category.capitalize()}: ${amount:,}")
        
        lines.append(f"\nPreferences:")
        lines.append(f"  Guest Count: {self.preferences['guest_count']}")
        lines.append(f"  Dietary Restrictions: {', '.join(self.preferences['dietary_restrictions'])}")
        
        lines.append(f"\n{'=' * 60}")
        lines.append("RECOMMENDATIONS BY CATEGORY")
        lines.append("=" * 60)
        
        for category, items in recommendations.items():
            lines.append(f"\n### {category.upper()} ###")
            
            if not items:
                lines.append("  No options found.")
                continue
            
            for i, item in enumerate(items[:5], 1):  # Top 5 per category
                lines.append(f"\n{i}. {Path(item['file']).name}")
                lines.append(f"   Score: {item['score']:.1f}/100")
                if item.get("price"):
                    lines.append(f"   Price: ${item['price']:,.0f}")
                if item.get("capacity"):
                    lines.append(f"   Capacity: {item['capacity']} guests")
                if item.get("dietary_options"):
                    lines.append(f"   Dietary Options: {', '.join(item['dietary_options'])}")
                if item.get("reasons"):
                    lines.append(f"   Why: {'; '.join(item['reasons'])}")
        
        lines.append(f"\n{'=' * 60}")
        return "\n".join(lines)
