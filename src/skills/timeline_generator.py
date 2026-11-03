"""
Timeline Generator Skill - Creates wedding planning timelines and checklists.
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta
from .base_skill import BaseSkill


class TimelineGeneratorSkill(BaseSkill):
    """Generates wedding planning timelines and task checklists."""
    
    @property
    def name(self) -> str:
        return "timeline_generator"
    
    @property
    def description(self) -> str:
        return "Generates customized wedding planning timelines with tasks and deadlines"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def category(self) -> str:
        return "planning"
    
    def execute(self, wedding_date: str, style: str = "comprehensive") -> Dict[str, Any]:
        """
        Generate a wedding planning timeline.
        
        Args:
            wedding_date: Wedding date in YYYY-MM-DD format
            style: Timeline style - 'comprehensive', 'minimal', or 'rushed'
        
        Returns:
            Timeline with tasks organized by time period
        """
        try:
            wedding_date_obj = datetime.strptime(wedding_date, "%Y-%m-%d")
        except ValueError:
            return {
                'status': 'error',
                'message': 'Invalid date format. Use YYYY-MM-DD (e.g., 2026-06-15)'
            }
        
        today = datetime.now()
        days_until_wedding = (wedding_date_obj - today).days
        
        if days_until_wedding < 0:
            return {
                'status': 'error',
                'message': 'Wedding date is in the past'
            }
        
        # Select timeline based on time available
        if days_until_wedding < 90:
            style = 'rushed'
        elif days_until_wedding < 180:
            style = 'minimal'
        
        timeline = self._generate_timeline(wedding_date_obj, today, style)
        
        return {
            'status': 'success',
            'result': {
                'wedding_date': wedding_date,
                'days_until_wedding': days_until_wedding,
                'style': style,
                'timeline': timeline,
                'summary': self._generate_summary(timeline)
            }
        }
    
    def _generate_timeline(self, wedding_date: datetime, today: datetime, style: str) -> Dict[str, List[Dict]]:
        """Generate timeline tasks based on style and time available."""
        
        if style == 'rushed':
            return self._rushed_timeline(wedding_date, today)
        elif style == 'minimal':
            return self._minimal_timeline(wedding_date, today)
        else:
            return self._comprehensive_timeline(wedding_date, today)
    
    def _comprehensive_timeline(self, wedding_date: datetime, today: datetime) -> Dict[str, List[Dict]]:
        """12+ months planning timeline."""
        timeline = {}
        
        # 12 months before
        milestone_date = wedding_date - timedelta(days=365)
        if milestone_date >= today:
            timeline["12 Months Before"] = [
                {'task': 'Announce engagement', 'category': 'general', 'priority': 'high'},
                {'task': 'Set wedding budget with partner/family', 'category': 'budget', 'priority': 'high'},
                {'task': 'Create guest list (rough estimate)', 'category': 'guests', 'priority': 'high'},
                {'task': 'Start researching venues', 'category': 'venue', 'priority': 'high'},
                {'task': 'Hire wedding planner (optional)', 'category': 'planning', 'priority': 'medium'},
            ]
        
        # 9-11 months before
        milestone_date = wedding_date - timedelta(days=300)
        if milestone_date >= today:
            timeline["9-11 Months Before"] = [
                {'task': 'Book ceremony and reception venues', 'category': 'venue', 'priority': 'high'},
                {'task': 'Hire photographer and videographer', 'category': 'photography', 'priority': 'high'},
                {'task': 'Research and book caterer', 'category': 'catering', 'priority': 'high'},
                {'task': 'Choose wedding party members', 'category': 'general', 'priority': 'high'},
                {'task': 'Start dress/suit shopping', 'category': 'attire', 'priority': 'medium'},
                {'task': 'Book band or DJ', 'category': 'entertainment', 'priority': 'medium'},
            ]
        
        # 6-8 months before
        milestone_date = wedding_date - timedelta(days=210)
        if milestone_date >= today:
            timeline["6-8 Months Before"] = [
                {'task': 'Order wedding dress/suit', 'category': 'attire', 'priority': 'high'},
                {'task': 'Book florist', 'category': 'floral', 'priority': 'high'},
                {'task': 'Finalize guest list', 'category': 'guests', 'priority': 'high'},
                {'task': 'Choose and order invitations', 'category': 'stationery', 'priority': 'medium'},
                {'task': 'Book hotel room blocks for guests', 'category': 'accommodations', 'priority': 'medium'},
                {'task': 'Register for gifts', 'category': 'general', 'priority': 'low'},
            ]
        
        # 4-5 months before
        milestone_date = wedding_date - timedelta(days=135)
        if milestone_date >= today:
            timeline["4-5 Months Before"] = [
                {'task': 'Order wedding cake', 'category': 'catering', 'priority': 'high'},
                {'task': 'Book hair and makeup artists', 'category': 'beauty', 'priority': 'medium'},
                {'task': 'Finalize menu with caterer', 'category': 'catering', 'priority': 'high'},
                {'task': 'Book transportation (limo, shuttles)', 'category': 'transportation', 'priority': 'medium'},
                {'task': 'Purchase wedding rings', 'category': 'attire', 'priority': 'high'},
            ]
        
        # 2-3 months before
        milestone_date = wedding_date - timedelta(days=75)
        if milestone_date >= today:
            timeline["2-3 Months Before"] = [
                {'task': 'Mail invitations', 'category': 'stationery', 'priority': 'high'},
                {'task': 'Schedule dress/suit fittings', 'category': 'attire', 'priority': 'high'},
                {'task': 'Finalize ceremony details', 'category': 'ceremony', 'priority': 'high'},
                {'task': 'Apply for marriage license', 'category': 'legal', 'priority': 'high'},
                {'task': 'Book rehearsal dinner venue', 'category': 'catering', 'priority': 'medium'},
                {'task': 'Create wedding website', 'category': 'general', 'priority': 'low'},
            ]
        
        # 1 month before
        milestone_date = wedding_date - timedelta(days=30)
        if milestone_date >= today:
            timeline["1 Month Before"] = [
                {'task': 'Final dress/suit fitting', 'category': 'attire', 'priority': 'high'},
                {'task': 'Confirm final guest count with vendors', 'category': 'catering', 'priority': 'high'},
                {'task': 'Create seating chart', 'category': 'reception', 'priority': 'high'},
                {'task': 'Finalize timeline with photographer', 'category': 'photography', 'priority': 'medium'},
                {'task': 'Write vows (if personal)', 'category': 'ceremony', 'priority': 'medium'},
                {'task': 'Get marriage license', 'category': 'legal', 'priority': 'high'},
            ]
        
        # 1-2 weeks before
        milestone_date = wedding_date - timedelta(days=10)
        if milestone_date >= today:
            timeline["1-2 Weeks Before"] = [
                {'task': 'Confirm all vendor arrival times', 'category': 'general', 'priority': 'high'},
                {'task': 'Pick up wedding dress/suit', 'category': 'attire', 'priority': 'high'},
                {'task': 'Rehearsal and rehearsal dinner', 'category': 'ceremony', 'priority': 'high'},
                {'task': 'Prepare vendor payments and tips', 'category': 'budget', 'priority': 'high'},
                {'task': 'Pack for honeymoon', 'category': 'honeymoon', 'priority': 'medium'},
                {'task': 'Delegate day-of responsibilities', 'category': 'general', 'priority': 'medium'},
            ]
        
        # Week of wedding
        milestone_date = wedding_date - timedelta(days=3)
        if milestone_date >= today:
            timeline["Week of Wedding"] = [
                {'task': 'Get manicure/pedicure', 'category': 'beauty', 'priority': 'low'},
                {'task': 'Confirm final headcount with caterer', 'category': 'catering', 'priority': 'high'},
                {'task': 'Break in wedding shoes', 'category': 'attire', 'priority': 'low'},
                {'task': 'Prepare emergency kit', 'category': 'general', 'priority': 'medium'},
                {'task': 'Rest and relax!', 'category': 'general', 'priority': 'high'},
            ]
        
        return timeline
    
    def _minimal_timeline(self, wedding_date: datetime, today: datetime) -> Dict[str, List[Dict]]:
        """6-month planning timeline."""
        timeline = {}
        
        # Immediate priorities
        timeline["Immediate (Week 1-2)"] = [
            {'task': 'Set budget and guest count', 'category': 'budget', 'priority': 'high'},
            {'task': 'Book venue (ceremony + reception)', 'category': 'venue', 'priority': 'high'},
            {'task': 'Book photographer', 'category': 'photography', 'priority': 'high'},
            {'task': 'Book caterer', 'category': 'catering', 'priority': 'high'},
        ]
        
        # Month 1-2
        milestone_date = wedding_date - timedelta(days=150)
        if milestone_date >= today:
            timeline["Months 1-2"] = [
                {'task': 'Order dress/suit', 'category': 'attire', 'priority': 'high'},
                {'task': 'Book florist and DJ/band', 'category': 'vendors', 'priority': 'high'},
                {'task': 'Finalize guest list', 'category': 'guests', 'priority': 'high'},
                {'task': 'Order invitations', 'category': 'stationery', 'priority': 'medium'},
            ]
        
        # Months 3-4
        milestone_date = wedding_date - timedelta(days=90)
        if milestone_date >= today:
            timeline["Months 3-4"] = [
                {'task': 'Mail invitations', 'category': 'stationery', 'priority': 'high'},
                {'task': 'Book hair/makeup', 'category': 'beauty', 'priority': 'medium'},
                {'task': 'Order wedding cake', 'category': 'catering', 'priority': 'high'},
                {'task': 'Purchase rings', 'category': 'attire', 'priority': 'high'},
            ]
        
        # Last month
        milestone_date = wedding_date - timedelta(days=30)
        if milestone_date >= today:
            timeline["Final Month"] = [
                {'task': 'Final fittings', 'category': 'attire', 'priority': 'high'},
                {'task': 'Get marriage license', 'category': 'legal', 'priority': 'high'},
                {'task': 'Confirm all vendor details', 'category': 'vendors', 'priority': 'high'},
                {'task': 'Create seating chart', 'category': 'reception', 'priority': 'high'},
            ]
        
        return timeline
    
    def _rushed_timeline(self, wedding_date: datetime, today: datetime) -> Dict[str, List[Dict]]:
        """Under 3-month planning timeline."""
        timeline = {
            "ASAP (This Week!)": [
                {'task': 'Set budget immediately', 'category': 'budget', 'priority': 'high'},
                {'task': 'Book venue NOW', 'category': 'venue', 'priority': 'high'},
                {'task': 'Book photographer NOW', 'category': 'photography', 'priority': 'high'},
                {'task': 'Book caterer NOW', 'category': 'catering', 'priority': 'high'},
                {'task': 'Order dress/suit off-the-rack', 'category': 'attire', 'priority': 'high'},
            ],
            "Week 2-3": [
                {'task': 'Send digital invitations', 'category': 'stationery', 'priority': 'high'},
                {'task': 'Book DJ or create playlist', 'category': 'entertainment', 'priority': 'medium'},
                {'task': 'Order simple floral arrangements', 'category': 'floral', 'priority': 'medium'},
                {'task': 'Purchase rings', 'category': 'attire', 'priority': 'high'},
            ],
            "Month 2": [
                {'task': 'Finalize menu', 'category': 'catering', 'priority': 'high'},
                {'task': 'Get marriage license', 'category': 'legal', 'priority': 'high'},
                {'task': 'Book hair/makeup or DIY plan', 'category': 'beauty', 'priority': 'medium'},
                {'task': 'Create simple ceremony plan', 'category': 'ceremony', 'priority': 'high'},
            ],
            "Final Weeks": [
                {'task': 'Confirm all vendor details', 'category': 'vendors', 'priority': 'high'},
                {'task': 'Final dress fitting', 'category': 'attire', 'priority': 'high'},
                {'task': 'Create seating chart', 'category': 'reception', 'priority': 'high'},
                {'task': 'Breathe! You got this!', 'category': 'general', 'priority': 'high'},
            ]
        }
        
        return timeline
    
    def _generate_summary(self, timeline: Dict) -> str:
        """Generate a summary of the timeline."""
        total_tasks = sum(len(tasks) for tasks in timeline.values())
        high_priority = sum(
            1 for tasks in timeline.values() 
            for task in tasks 
            if task['priority'] == 'high'
        )
        
        return f"Total tasks: {total_tasks} | High priority: {high_priority} | Time periods: {len(timeline)}"
