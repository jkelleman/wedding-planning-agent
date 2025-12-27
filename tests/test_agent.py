"""Tests for the wedding planning agent."""
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scanner import DocumentScanner
from src.organizer import FileOrganizer
from src.recommender import WeddingRecommender


def test_scanner():
    """Test the document scanner with sample text."""
    print("Testing DocumentScanner...")
    scanner = DocumentScanner()
    
    # Test metadata extraction
    sample_text = """
    Grand Ballroom Wedding Venue
    
    Capacity: 200 guests
    Price: $15,000 for full day rental
    
    Includes:
    - Tables and chairs
    - Dance floor
    - Vegetarian and gluten-free options available
    """
    
    metadata = scanner._extract_metadata(sample_text)
    
    assert metadata['category'] == 'venue', f"Expected 'venue', got {metadata['category']}"
    assert metadata['capacity'] == 200, f"Expected 200, got {metadata['capacity']}"
    assert metadata['price'] == 15000.0, f"Expected 15000.0, got {metadata['price']}"
    assert 'vegetarian' in metadata['dietary_options'], "Expected 'vegetarian' in dietary_options"
    assert 'gluten-free' in metadata['dietary_options'], "Expected 'gluten-free' in dietary_options"
    
    print("✓ Scanner tests passed!")


def test_recommender():
    """Test the recommendation engine."""
    print("\nTesting WeddingRecommender...")
    
    config = {
        'budget': {
            'max_total': 50000,
            'venue': 15000,
            'catering': 10000,
            'floral': 3000,
            'photography': 5000
        },
        'preferences': {
            'dietary_restrictions': ['vegetarian', 'gluten-free'],
            'guest_count': 150,
            'preferred_season': 'fall',
            'location_preference': 'outdoor'
        },
        'file_organization': {
            'categories': ['venue', 'catering', 'floral', 'photography', 'entertainment', 'other'],
            'input_dir': 'data/raw',
            'output_dir': 'data/organized',
            'recommendations_dir': 'outputs/recommendations'
        }
    }
    
    recommender = WeddingRecommender(config)
    
    # Test fit score calculation
    venue_metadata = {
        'category': 'venue',
        'price': 14000,
        'capacity': 180
    }
    score = recommender._calculate_fit_score('venue', venue_metadata)
    assert score > 70, f"Expected high score for good venue fit, got {score}"
    
    catering_metadata = {
        'category': 'catering',
        'price': 8000,
        'dietary_options': ['vegetarian', 'gluten-free', 'vegan']
    }
    score = recommender._calculate_fit_score('catering', catering_metadata)
    assert score > 80, f"Expected high score for good catering fit, got {score}"
    
    # Test over-budget penalty
    expensive_venue = {
        'category': 'venue',
        'price': 25000,
        'capacity': 200
    }
    score = recommender._calculate_fit_score('venue', expensive_venue)
    assert score < 50, f"Expected low score for over-budget venue, got {score}"
    
    print("✓ Recommender tests passed!")


def test_file_organization():
    """Test file organizer logic."""
    print("\nTesting FileOrganizer...")
    
    config = {
        'budget': {'max_total': 50000},
        'preferences': {'guest_count': 150},
        'file_organization': {
            'categories': ['venue', 'catering', 'floral', 'photography', 'entertainment', 'other'],
            'input_dir': 'data/raw',
            'output_dir': 'data/organized',
            'recommendations_dir': 'outputs/recommendations'
        }
    }
    
    organizer = FileOrganizer(config)
    
    # Test filename sanitization
    dirty_name = 'Grand <Hall>: Venue/Proposal*2024'
    clean_name = organizer._sanitize_filename(dirty_name)
    assert '<' not in clean_name and '>' not in clean_name, f"Expected clean name, got {clean_name}"
    
    print("✓ Organizer tests passed!")


def main():
    """Run all tests."""
    print("="*60)
    print("RUNNING WEDDING PLANNING AGENT TESTS")
    print("="*60)
    
    try:
        test_scanner()
        test_recommender()
        test_file_organization()
        
        print("\n" + "="*60)
        print("✓ ALL TESTS PASSED!")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
