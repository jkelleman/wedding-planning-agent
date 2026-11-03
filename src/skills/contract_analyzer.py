"""
Contract Analyzer Skill - Analyzes vendor contracts for key terms and red flags.
"""
from typing import Dict, Any, List
import re
from pathlib import Path
from .base_skill import BaseSkill


class ContractAnalyzerSkill(BaseSkill):
    """Analyzes vendor contracts to extract key terms and identify potential issues."""
    
    @property
    def name(self) -> str:
        return "contract_analyzer"
    
    @property
    def description(self) -> str:
        return "Analyzes vendor contracts for payment terms, cancellation policies, and red flags"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def category(self) -> str:
        return "analysis"
    
    def execute(self, contract_text: str = None, contract_file: str = None) -> Dict[str, Any]:
        """
        Analyze a contract for key terms and potential issues.
        
        Args:
            contract_text: Raw contract text (optional if contract_file provided)
            contract_file: Path to contract file (optional if contract_text provided)
        
        Returns:
            Analysis results with extracted terms and warnings
        """
        if not contract_text and not contract_file:
            return {
                'status': 'error',
                'message': 'Must provide either contract_text or contract_file'
            }
        
        # Load contract text if file provided
        if contract_file and not contract_text:
            try:
                # Use the scanner to extract text from PDF
                from ..scanner import DocumentScanner
                scanner = DocumentScanner()
                scan_result = scanner.scan_file(contract_file)
                contract_text = scan_result.get('text', '')
            except Exception as e:
                return {
                    'status': 'error',
                    'message': f'Failed to read contract file: {e}'
                }
        
        analysis = {
            'status': 'success',
            'result': {
                'payment_terms': self._extract_payment_terms(contract_text),
                'cancellation_policy': self._extract_cancellation_policy(contract_text),
                'deposit_info': self._extract_deposit_info(contract_text),
                'liability_clauses': self._extract_liability_clauses(contract_text),
                'red_flags': self._identify_red_flags(contract_text),
                'important_dates': self._extract_dates(contract_text),
                'summary': self._generate_summary(contract_text)
            }
        }
        
        return analysis
    
    def _extract_payment_terms(self, text: str) -> Dict[str, Any]:
        """Extract payment schedule and terms."""
        terms = {
            'total_amount': None,
            'deposit_required': None,
            'payment_schedule': [],
            'payment_methods': []
        }
        
        # Extract total amount
        total_patterns = [
            r'total\s+(?:cost|price|fee)[\s:]+\$?([\d,]+(?:\.\d{2})?)',
            r'grand\s+total[\s:]+\$?([\d,]+(?:\.\d{2})?)'
        ]
        for pattern in total_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                terms['total_amount'] = float(match.group(1).replace(',', ''))
                break
        
        # Extract payment schedule mentions
        if 'installment' in text.lower():
            terms['payment_schedule'].append('Installment payments available')
        if 'net 30' in text.lower() or 'net 60' in text.lower():
            terms['payment_schedule'].append('Net payment terms specified')
        
        # Payment methods
        methods = ['credit card', 'check', 'cash', 'wire transfer', 'venmo', 'paypal']
        for method in methods:
            if method in text.lower():
                terms['payment_methods'].append(method)
        
        return terms
    
    def _extract_cancellation_policy(self, text: str) -> Dict[str, Any]:
        """Extract cancellation and refund policy."""
        policy = {
            'refundable': None,
            'cancellation_deadline': None,
            'penalty': None,
            'policy_text': None
        }
        
        # Look for cancellation section
        cancel_pattern = r'(cancellation.*?(?:policy|terms).*?)(?:\n\n|\. [A-Z])'
        match = re.search(cancel_pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            policy['policy_text'] = match.group(1).strip()
        
        # Check if non-refundable
        if 'non-refundable' in text.lower() or 'not refundable' in text.lower():
            policy['refundable'] = False
        elif 'refundable' in text.lower():
            policy['refundable'] = True
        
        # Extract cancellation deadline
        deadline_pattern = r'cancel(?:lation)?\s+(?:within|by|before)\s+(\d+)\s+(day|week|month)'
        match = re.search(deadline_pattern, text, re.IGNORECASE)
        if match:
            policy['cancellation_deadline'] = f"{match.group(1)} {match.group(2)}s before event"
        
        return policy
    
    def _extract_deposit_info(self, text: str) -> Dict[str, Any]:
        """Extract deposit requirements."""
        deposit = {
            'amount': None,
            'percentage': None,
            'due_date': None,
            'non_refundable': None
        }
        
        # Deposit amount
        deposit_patterns = [
            r'deposit.*?\$?([\d,]+(?:\.\d{2})?)',
            r'\$?([\d,]+(?:\.\d{2})?)\s+deposit'
        ]
        for pattern in deposit_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                deposit['amount'] = float(match.group(1).replace(',', ''))
                break
        
        # Deposit percentage
        percent_pattern = r'deposit.*?(\d+)%|(\d+)%\s+deposit'
        match = re.search(percent_pattern, text, re.IGNORECASE)
        if match:
            deposit['percentage'] = int(match.group(1) or match.group(2))
        
        # Non-refundable deposit
        if 'non-refundable deposit' in text.lower():
            deposit['non_refundable'] = True
        
        return deposit
    
    def _extract_liability_clauses(self, text: str) -> List[str]:
        """Extract liability and insurance clauses."""
        clauses = []
        
        liability_keywords = [
            'liability',
            'insurance required',
            'hold harmless',
            'indemnify',
            'responsible for damage'
        ]
        
        for keyword in liability_keywords:
            if keyword in text.lower():
                # Extract sentence containing the keyword
                pattern = r'([^.]*' + re.escape(keyword) + r'[^.]*\.)'
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    clauses.append(match.group(1).strip())
        
        return clauses
    
    def _identify_red_flags(self, text: str) -> List[Dict[str, str]]:
        """Identify potential red flags in the contract."""
        red_flags = []
        
        # Check for concerning terms
        concerns = {
            '100% non-refundable': 'No refund policy - high risk if you need to cancel',
            'final sale': 'No refund or exchange policy',
            'as-is': 'No guarantees on quality or condition',
            'not responsible for': 'Vendor disclaims responsibility - check what they\'re not covering',
            'additional fees may apply': 'Potential for unexpected charges',
            'subject to change': 'Terms may change without notice',
            'force majeure': 'Vendor can cancel without penalty in certain circumstances',
            'minimum guest count': 'You may be charged for guests who don\'t attend'
        }
        
        for term, explanation in concerns.items():
            if term in text.lower():
                red_flags.append({
                    'term': term,
                    'explanation': explanation,
                    'severity': 'high' if 'non-refundable' in term or 'not responsible' in term else 'medium'
                })
        
        # Check for missing important terms
        important_terms = {
            'cancellation': 'No cancellation policy found',
            'refund': 'No refund policy mentioned',
            'insurance': 'No insurance requirements specified'
        }
        
        for term, warning in important_terms.items():
            if term not in text.lower():
                red_flags.append({
                    'term': f'Missing: {term}',
                    'explanation': warning,
                    'severity': 'low'
                })
        
        return red_flags
    
    def _extract_dates(self, text: str) -> List[str]:
        """Extract important dates from contract."""
        dates = []
        
        # Common date patterns
        date_contexts = [
            'deposit due',
            'final payment due',
            'event date',
            'cancellation deadline',
            'contract expires'
        ]
        
        for context in date_contexts:
            pattern = r'' + context + r'.*?(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                dates.append(f"{context}: {match.group(1)}")
        
        return dates
    
    def _generate_summary(self, text: str) -> str:
        """Generate a brief summary of contract key points."""
        summary_parts = []
        
        # Check payment structure
        if 'deposit' in text.lower():
            summary_parts.append("Requires deposit")
        
        # Check refund policy
        if 'non-refundable' in text.lower():
            summary_parts.append("Non-refundable terms present")
        elif 'refundable' in text.lower():
            summary_parts.append("Refund policy included")
        
        # Check for flexibility
        if 'reschedule' in text.lower() or 'postpone' in text.lower():
            summary_parts.append("Rescheduling options available")
        
        # Check for guarantees
        if 'guarantee' in text.lower():
            summary_parts.append("Contains service guarantees")
        
        if not summary_parts:
            return "Standard contract - review all terms carefully"
        
        return "; ".join(summary_parts)
