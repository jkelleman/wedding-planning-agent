"""
Base skill class for creating extensible agent capabilities.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import importlib
import inspect
from pathlib import Path


class BaseSkill(ABC):
    """
    Abstract base class for agent skills.
    
    All skills must inherit from this class and implement the required methods.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the skill with configuration.
        
        Args:
            config: Configuration dictionary from config.yaml
        """
        self.config = config
        self.enabled = True
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the skill name (must be unique)."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Return a brief description of what this skill does."""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Return the skill version."""
        pass
    
    @property
    def category(self) -> str:
        """Return the skill category (planning, analysis, communication, etc.)."""
        return "general"
    
    @property
    def required_config_keys(self) -> List[str]:
        """Return list of required configuration keys for this skill."""
        return []
    
    @abstractmethod
    def execute(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Execute the skill's main functionality.
        
        Returns:
            Dict with 'status', 'result', and optional 'message' keys
        """
        pass
    
    def validate_config(self) -> bool:
        """Validate that required configuration is present."""
        for key in self.required_config_keys:
            if key not in self.config:
                print(f"Warning: Skill '{self.name}' missing required config key: {key}")
                return False
        return True
    
    def get_help(self) -> str:
        """Return detailed help text for this skill."""
        return f"""
Skill: {self.name}
Version: {self.version}
Category: {self.category}
Description: {self.description}

Required Configuration:
{', '.join(self.required_config_keys) if self.required_config_keys else 'None'}

Usage: See documentation for specific usage patterns.
"""


class SkillRegistry:
    """
    Registry for managing and discovering skills.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the skill registry.
        
        Args:
            config: Global configuration dictionary
        """
        self.config = config
        self.skills: Dict[str, BaseSkill] = {}
        self._discover_skills()
    
    def _discover_skills(self):
        """Automatically discover and register all skills in the skills directory."""
        skills_dir = Path(__file__).parent
        
        for file_path in skills_dir.glob('*.py'):
            if file_path.name.startswith('_') or file_path.name == 'base_skill.py':
                continue
            
            try:
                module_name = f"src.skills.{file_path.stem}"
                module = importlib.import_module(module_name)
                
                # Find all classes that inherit from BaseSkill
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, BaseSkill) and obj is not BaseSkill:
                        skill_instance = obj(self.config)
                        if skill_instance.validate_config():
                            self.register_skill(skill_instance)
            except Exception as e:
                print(f"Warning: Could not load skill from {file_path.name}: {e}")
    
    def register_skill(self, skill: BaseSkill):
        """
        Register a skill instance.
        
        Args:
            skill: Instance of a skill class
        """
        if skill.name in self.skills:
            print(f"Warning: Skill '{skill.name}' already registered. Overwriting.")
        
        self.skills[skill.name] = skill
        print(f"✓ Registered skill: {skill.name} (v{skill.version})")
    
    def get_skill(self, name: str) -> Optional[BaseSkill]:
        """
        Get a skill by name.
        
        Args:
            name: Name of the skill
        
        Returns:
            Skill instance or None if not found
        """
        return self.skills.get(name)
    
    def list_skills(self) -> List[Dict[str, str]]:
        """
        List all registered skills.
        
        Returns:
            List of dictionaries with skill information
        """
        return [
            {
                'name': skill.name,
                'version': skill.version,
                'category': skill.category,
                'description': skill.description,
                'enabled': skill.enabled
            }
            for skill in self.skills.values()
        ]
    
    def execute_skill(self, skill_name: str, *args, **kwargs) -> Dict[str, Any]:
        """
        Execute a skill by name.
        
        Args:
            skill_name: Name of the skill to execute
            *args, **kwargs: Arguments to pass to the skill
        
        Returns:
            Result dictionary from skill execution
        """
        skill = self.get_skill(skill_name)
        
        if not skill:
            return {
                'status': 'error',
                'message': f"Skill '{skill_name}' not found"
            }
        
        if not skill.enabled:
            return {
                'status': 'error',
                'message': f"Skill '{skill_name}' is disabled"
            }
        
        try:
            return skill.execute(*args, **kwargs)
        except Exception as e:
            return {
                'status': 'error',
                'message': f"Error executing skill '{skill_name}': {str(e)}"
            }
    
    def get_skills_by_category(self, category: str) -> List[BaseSkill]:
        """
        Get all skills in a specific category.
        
        Args:
            category: Category name
        
        Returns:
            List of skills in that category
        """
        return [
            skill for skill in self.skills.values()
            if skill.category == category
        ]
    
    def print_skill_summary(self):
        """Print a summary of all registered skills."""
        print("\n" + "=" * 70)
        print("REGISTERED SKILLS")
        print("=" * 70)
        
        if not self.skills:
            print("\nNo skills registered.")
            return
        
        # Group by category
        by_category = {}
        for skill in self.skills.values():
            if skill.category not in by_category:
                by_category[skill.category] = []
            by_category[skill.category].append(skill)
        
        for category, skills in sorted(by_category.items()):
            print(f"\n{category.upper()}")
            print("─" * 70)
            for skill in skills:
                status = "✓" if skill.enabled else "✗"
                print(f"  {status} {skill.name} (v{skill.version})")
                print(f"     {skill.description}")
        
        print("\n" + "=" * 70)
