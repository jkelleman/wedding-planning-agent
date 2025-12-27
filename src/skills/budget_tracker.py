"""
Budget Tracker Skill - Tracks wedding expenses and budget allocation.
"""
from typing import Dict, Any, List
from datetime import datetime
from .base_skill import BaseSkill


class BudgetTrackerSkill(BaseSkill):
    """Tracks wedding expenses and provides budget insights."""
    
    @property
    def name(self) -> str:
        return "budget_tracker"
    
    @property
    def description(self) -> str:
        return "Tracks expenses, compares to budget, and provides spending insights"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def category(self) -> str:
        return "financial"
    
    def execute(self, action: str = "summary", **kwargs) -> Dict[str, Any]:
        """
        Execute budget tracking actions.
        
        Args:
            action: 'summary', 'add_expense', 'forecast', or 'recommendations'
            **kwargs: Additional parameters based on action
        
        Returns:
            Budget tracking results
        """
        if action == "summary":
            return self._generate_summary()
        elif action == "add_expense":
            return self._add_expense(**kwargs)
        elif action == "forecast":
            return self._forecast_remaining(**kwargs)
        elif action == "recommendations":
            return self._generate_recommendations()
        else:
            return {
                'status': 'error',
                'message': f'Unknown action: {action}. Use: summary, add_expense, forecast, or recommendations'
            }
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate current budget summary from config."""
        budget = self.config.get('budget', {})
        total_budget = budget.get('max_total', 0)
        
        # Calculate allocated vs unallocated
        allocated = sum(
            amount for key, amount in budget.items() 
            if key != 'max_total' and isinstance(amount, (int, float))
        )
        unallocated = total_budget - allocated
        
        categories = {
            key: {
                'budget': amount,
                'spent': 0,  # Would track from actual expenses
                'remaining': amount,
                'percentage': (amount / total_budget * 100) if total_budget > 0 else 0
            }
            for key, amount in budget.items()
            if key != 'max_total' and isinstance(amount, (int, float))
        }
        
        return {
            'status': 'success',
            'result': {
                'total_budget': total_budget,
                'allocated': allocated,
                'unallocated': unallocated,
                'categories': categories,
                'alerts': self._generate_alerts(categories, total_budget)
            }
        }
    
    def _add_expense(self, category: str, amount: float, vendor: str, description: str = "") -> Dict[str, Any]:
        """
        Add an expense (note: this is a demo - real implementation would persist data).
        
        Args:
            category: Budget category (venue, catering, etc.)
            amount: Expense amount
            vendor: Vendor name
            description: Optional description
        
        Returns:
            Updated budget status
        """
        budget = self.config.get('budget', {})
        category_budget = budget.get(category, 0)
        
        return {
            'status': 'success',
            'result': {
                'expense_added': {
                    'category': category,
                    'amount': amount,
                    'vendor': vendor,
                    'description': description,
                    'date': datetime.now().strftime('%Y-%m-%d')
                },
                'category_status': {
                    'budget': category_budget,
                    'spent': amount,
                    'remaining': category_budget - amount,
                    'over_budget': amount > category_budget
                },
                'message': f'Expense recorded: ${amount:,.2f} to {vendor} ({category})'
            }
        }
    
    def _forecast_remaining(self, estimated_expenses: Dict[str, float] = None) -> Dict[str, Any]:
        """
        Forecast budget with estimated remaining expenses.
        
        Args:
            estimated_expenses: Dict of {category: estimated_amount}
        
        Returns:
            Forecast analysis
        """
        budget = self.config.get('budget', {})
        total_budget = budget.get('max_total', 0)
        
        if not estimated_expenses:
            estimated_expenses = {}
        
        forecast = {
            'total_budget': total_budget,
            'estimated_total_cost': sum(estimated_expenses.values()),
            'projected_remaining': total_budget - sum(estimated_expenses.values()),
            'categories': {}
        }
        
        for category, estimated in estimated_expenses.items():
            category_budget = budget.get(category, 0)
            forecast['categories'][category] = {
                'budget': category_budget,
                'estimated': estimated,
                'variance': category_budget - estimated,
                'status': 'under' if estimated <= category_budget else 'over'
            }
        
        return {
            'status': 'success',
            'result': forecast
        }
    
    def _generate_recommendations(self) -> Dict[str, Any]:
        """Generate budget recommendations."""
        budget = self.config.get('budget', {})
        total_budget = budget.get('max_total', 0)
        
        recommendations = []
        
        # Industry standard percentages
        industry_standards = {
            'venue': 0.30,  # 30% of budget
            'catering': 0.28,  # 28%
            'photography': 0.12,  # 12%
            'floral': 0.08,  # 8%
            'entertainment': 0.08,  # 8%
            'attire': 0.08,  # 8%
            'other': 0.06  # 6%
        }
        
        for category, percentage in industry_standards.items():
            recommended = total_budget * percentage
            current = budget.get(category, 0)
            
            if current == 0:
                recommendations.append({
                    'category': category,
                    'current': current,
                    'recommended': recommended,
                    'advice': f'Consider allocating ${recommended:,.0f} ({percentage*100:.0f}% of total budget)'
                })
            elif abs(current - recommended) / recommended > 0.2:  # >20% difference
                if current > recommended:
                    recommendations.append({
                        'category': category,
                        'current': current,
                        'recommended': recommended,
                        'advice': f'Allocated amount is {((current-recommended)/recommended*100):.0f}% above industry standard'
                    })
                else:
                    recommendations.append({
                        'category': category,
                        'current': current,
                        'recommended': recommended,
                        'advice': f'Consider increasing allocation (currently {((recommended-current)/recommended*100):.0f}% below standard)'
                    })
        
        return {
            'status': 'success',
            'result': {
                'recommendations': recommendations,
                'industry_standards': industry_standards,
                'total_budget': total_budget
            }
        }
    
    def _generate_alerts(self, categories: Dict, total_budget: float) -> List[str]:
        """Generate budget alerts."""
        alerts = []
        
        # Check for over-allocation
        total_allocated = sum(cat['budget'] for cat in categories.values())
        if total_allocated > total_budget:
            alerts.append(f'⚠️ Over-allocated by ${total_allocated - total_budget:,.0f}')
        
        # Check for uneven distribution
        for name, info in categories.items():
            if info['percentage'] > 40:
                alerts.append(f'⚠️ {name} takes up {info["percentage"]:.0f}% of budget')
        
        return alerts
