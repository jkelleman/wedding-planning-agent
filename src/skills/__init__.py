"""
Skills package for wedding planning agent.
Provides extensible plugin architecture for adding new capabilities.
"""
from .base_skill import BaseSkill, SkillRegistry

__all__ = ['BaseSkill', 'SkillRegistry']
