"""Wedding Planning Agent - Main CLI Interface"""
import sys
import argparse
from pathlib import Path
import yaml
import json

from src.scanner import DocumentScanner
from src.organizer import FileOrganizer
from src.recommender import WeddingRecommender
from src.negotiator import NegotiationAgent
from src.skills import SkillRegistry


def load_config(config_path: str = "config.yaml") -> dict:
    """Load configuration from YAML file."""
    config_file = Path(config_path)
    if not config_file.exists():
        print(f"Error: Config file not found: {config_path}")
        print("Creating default config.yaml...")
        # Create default config
        default_config = {
            "budget": {
                "max_total": 50000,
                "venue": 15000,
                "catering": 10000,
                "floral": 3000,
                "photography": 5000
            },
            "preferences": {
                "dietary_restrictions": ["vegetarian", "gluten-free"],
                "guest_count": 150,
                "preferred_season": "fall",
                "location_preference": "outdoor"
            },
            "file_organization": {
                "categories": ["venue", "catering", "floral", "photography", "entertainment", "other"],
                "input_dir": "data/raw",
                "output_dir": "data/organized",
                "recommendations_dir": "outputs/recommendations"
            }
        }
        with open(config_file, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)
        return default_config
    
    with open(config_file) as f:
        return yaml.safe_load(f)


def cmd_scan(args):
    """Scan a single file or directory."""
    scanner = DocumentScanner()
    file_path = Path(args.path)
    
    if file_path.is_file():
        result = scanner.scan_file(str(file_path))
        print(json.dumps(result, indent=2))
    elif file_path.is_dir():
        print(f"Scanning directory: {file_path}")
        for item in file_path.rglob('*'):
            if item.is_file() and item.suffix.lower() in ['.pdf', '.png', '.jpg', '.jpeg']:
                print(f"\n--- {item.name} ---")
                result = scanner.scan_file(str(item))
                print(f"Category: {result['metadata'].get('category', 'unknown')}")
                print(f"Price: ${result['metadata'].get('price', 'N/A')}")
                print(f"Capacity: {result['metadata'].get('capacity', 'N/A')}")
                if result['metadata'].get('dietary_options'):
                    print(f"Dietary: {', '.join(result['metadata']['dietary_options'])}")
    else:
        print(f"Error: Path not found: {file_path}")


def cmd_organize(args):
    """Organize files from input directory."""
    config = load_config(args.config)
    organizer = FileOrganizer(config)
    
    input_dir = args.input_dir or config['file_organization']['input_dir']
    results = organizer.organize_directory(input_dir)
    
    print(f"\n{'='*60}")
    print("FILE ORGANIZATION RESULTS")
    print(f"{'='*60}\n")
    
    success_count = 0
    for result in results:
        if result.get("status") == "success":
            success_count += 1
            print(f"✓ {Path(result['old_path']).name}")
            print(f"  → {result['category']}/{Path(result['new_path']).name}")
        else:
            print(f"✗ {result.get('old_path', 'unknown')}: {result.get('message', 'error')}")
    
    print(f"\n{success_count}/{len(results)} files organized successfully.")
    print(f"Output directory: {config['file_organization']['output_dir']}")


def cmd_recommend(args):
    """Generate recommendations based on organized files."""
    config = load_config(args.config)
    organizer = FileOrganizer(config)
    recommender = WeddingRecommender(config)
    
    # First organize files
    input_dir = args.input_dir or config['file_organization']['input_dir']
    print("Organizing files...")
    organized_results = organizer.organize_directory(input_dir)
    
    # Generate recommendations
    print("Analyzing options...")
    recommendations = recommender.analyze_options(organized_results)
    
    # Generate report
    report = recommender.generate_report(recommendations)
    print("\n" + report)
    
    # Save report to file
    output_dir = Path(config['file_organization']['recommendations_dir'])
    output_dir.mkdir(parents=True, exist_ok=True)
    
    from datetime import datetime
    report_file = output_dir / f"recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"\nReport saved to: {report_file}")


def cmd_init(args):
    """Initialize project directories."""
    config = load_config(args.config)
    
    # Create directories
    dirs = [
        config['file_organization']['input_dir'],
        config['file_organization']['output_dir'],
        config['file_organization']['recommendations_dir'],
        config['negotiation'].get('drafts_dir', 'outputs/negotiation'),
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {dir_path}")
    
    for category in config['file_organization']['categories']:
        cat_dir = Path(config['file_organization']['output_dir']) / category
        cat_dir.mkdir(exist_ok=True)
        print(f"✓ Created: {cat_dir}")
    
    print("\n✓ Project initialized!")
    print(f"\nNext steps:")
    print(f"1. Add your wedding PDFs/PNGs to: {config['file_organization']['input_dir']}")
    print(f"2. Update config.yaml with your budget and preferences")
    print(f"3. Run: python main.py recommend")


def cmd_negotiate(args):
    """Analyze vendor quotes and draft negotiation emails."""
    config = load_config(args.config)
    negotiator = NegotiationAgent(config)
    scanner = DocumentScanner()
    
    # Scan the quote file
    print(f"Analyzing quote: {args.quote_file}")
    scan_result = scanner.scan_file(args.quote_file)
    
    if "error" in scan_result:
        print(f"Error: {scan_result['error']}")
        return
    
    # Analyze the quote
    analysis = negotiator.analyze_quote(scan_result)
    
    if analysis.get('status') == 'error':
        print(f"Error: {analysis['message']}")
        return
    
    # Print analysis
    print(f"\n{'='*70}")
    print(f"NEGOTIATION ANALYSIS: {analysis['vendor']}")
    print(f"{'='*70}")
    print(f"\nQuoted Price: ${analysis['quoted_price']:,.2f}")
    print(f"Budget Allocation: ${analysis['budget_allocation']:,.2f}")
    print(f"Over Budget: {'Yes' if analysis['over_budget'] else 'No'}")
    print(f"Negotiation Potential: {analysis['negotiation_potential']}")
    
    counter = analysis['suggested_counter_offer']
    print(f"\nSuggested Counter-Offer: ${counter['amount']:,.2f}")
    print(f"  Reduction: ${counter['reduction']:,.2f} ({counter['reduction_percentage']}%)")
    print(f"  Rationale: {counter['rationale']}")
    
    market = analysis['market_comparison']
    print(f"\nMarket Comparison:")
    print(f"  Market Average: ${market['market_average']:,.2f}")
    print(f"  This Quote: {market['position']}")
    print(f"  Difference: ${market['difference_from_avg']:+,.2f} ({market['difference_percentage']:+.1f}%)")
    
    print(f"\nTop Negotiation Strategies:")
    for i, strategy in enumerate(analysis['strategies'][:5], 1):
        print(f"  {i}. {strategy}")
    
    # Draft email if requested
    if args.draft:
        tone = args.tone or config['negotiation'].get('default_tone', 'professional')
        email = negotiator.draft_negotiation_email(analysis, tone)
        
        print(f"\n{'='*70}")
        print(f"DRAFT NEGOTIATION EMAIL ({tone.upper()} TONE)")
        print(f"{'='*70}\n")
        print(email)
        
        # Save draft if configured
        if config['negotiation'].get('auto_save_drafts', True):
            drafts_dir = Path(config['negotiation'].get('drafts_dir', 'outputs/negotiation'))
            drafts_dir.mkdir(parents=True, exist_ok=True)
            
            from datetime import datetime
            filename = f"{analysis['category']}_{analysis['vendor'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            draft_file = drafts_dir / filename
            
            with open(draft_file, 'w') as f:
                f.write(email)
            
            print(f"\n✓ Draft saved to: {draft_file}")


def cmd_negotiate_batch(args):
    """Analyze multiple quotes and generate negotiation report."""
    config = load_config(args.config)
    negotiator = NegotiationAgent(config)
    scanner = DocumentScanner()
    
    quotes_dir = Path(args.directory)
    if not quotes_dir.exists():
        print(f"Error: Directory not found: {quotes_dir}")
        return
    
    analyses = []
    print(f"Analyzing quotes in: {quotes_dir}\n")
    
    for file_path in quotes_dir.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in ['.pdf', '.png', '.jpg', '.jpeg']:
            print(f"  - {file_path.name}")
            scan_result = scanner.scan_file(str(file_path))
            if "error" not in scan_result:
                analysis = negotiator.analyze_quote(scan_result)
                if analysis.get('status') != 'error':
                    analyses.append(analysis)
    
    if not analyses:
        print("\nNo valid quotes found.")
        return
    
    # Generate comprehensive report
    report = negotiator.generate_negotiation_report(analyses)
    print("\n" + report)
    
    # Save report
    drafts_dir = Path(config['negotiation'].get('drafts_dir', 'outputs/negotiation'))
    drafts_dir.mkdir(parents=True, exist_ok=True)
    
    from datetime import datetime
    report_file = drafts_dir / f"negotiation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"\n✓ Report saved to: {report_file}")


def cmd_skills(args):
    """Manage and execute skills."""
    config = load_config(args.config)
    
    if not config.get('skills', {}).get('enabled', True):
        print("Skills are disabled in config.yaml")
        return
    
    registry = SkillRegistry(config)
    
    if args.skill_action == 'list':
        registry.print_skill_summary()
    
    elif args.skill_action == 'run':
        if not args.skill_name:
            print("Error: Must specify skill name with --name")
            return
        
        # Parse additional arguments as JSON if provided
        skill_args = {}
        if args.skill_args:
            try:
                skill_args = json.loads(args.skill_args)
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON in --args: {args.skill_args}")
                return
        
        result = registry.execute_skill(args.skill_name, **skill_args)
        
        if result['status'] == 'error':
            print(f"Error: {result['message']}")
        else:
            print(json.dumps(result, indent=2))
    
    elif args.skill_action == 'help':
        if not args.skill_name:
            print("Available skills:")
            for skill_info in registry.list_skills():
                print(f"  - {skill_info['name']}: {skill_info['description']}")
            print("\nUse: python main.py skills help --name <skill_name> for details")
        else:
            skill = registry.get_skill(args.skill_name)
            if skill:
                print(skill.get_help())
            else:
                print(f"Skill not found: {args.skill_name}")


def main():
    parser = argparse.ArgumentParser(
        description="Wedding Planning Agent - Organize and recommend wedding vendors"
    )
    parser.add_argument('--config', default='config.yaml', help='Path to config file')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Init command
    parser_init = subparsers.add_parser('init', help='Initialize project directories')
    parser_init.set_defaults(func=cmd_init)
    
    # Scan command
    parser_scan = subparsers.add_parser('scan', help='Scan a file or directory')
    parser_scan.add_argument('path', help='Path to file or directory to scan')
    parser_scan.set_defaults(func=cmd_scan)
    
    # Organize command
    parser_organize = subparsers.add_parser('organize', help='Organize files')
    parser_organize.add_argument('--input-dir', help='Input directory (overrides config)')
    parser_organize.set_defaults(func=cmd_organize)
    
    # Recommend command
    parser_recommend = subparsers.add_parser('recommend', help='Generate recommendations')
    parser_recommend.add_argument('--input-dir', help='Input directory (overrides config)')
    parser_recommend.set_defaults(func=cmd_recommend)
    
    # Negotiate command
    parser_negotiate = subparsers.add_parser('negotiate', help='Analyze quote and draft negotiation email')
    parser_negotiate.add_argument('quote_file', help='Path to vendor quote (PDF or PNG)')
    parser_negotiate.add_argument('--draft', action='store_true', help='Draft negotiation email')
    parser_negotiate.add_argument('--tone', choices=['professional', 'friendly', 'firm'], help='Email tone')
    parser_negotiate.set_defaults(func=cmd_negotiate)
    
    # Negotiate batch command
    parser_negotiate_batch = subparsers.add_parser('negotiate-batch', help='Analyze multiple quotes')
    parser_negotiate_batch.add_argument('directory', help='Directory containing quote files')
    parser_negotiate_batch.set_defaults(func=cmd_negotiate_batch)
    
    # Skills command
    parser_skills = subparsers.add_parser('skills', help='Manage and execute skills')
    parser_skills.add_argument('skill_action', choices=['list', 'run', 'help'], help='Skill action')
    parser_skills.add_argument('--name', dest='skill_name', help='Skill name')
    parser_skills.add_argument('--args', dest='skill_args', help='Skill arguments as JSON')
    parser_skills.set_defaults(func=cmd_skills)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    args.func(args)


if __name__ == '__main__':
    main()

