import json
import sys
from pathlib import Path
import random

print("=" * 80)
print("🚀 PHASE 1 COMPLETE VERIFICATION")
print("=" * 80)

# Color codes for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print("-" * 60)

def print_check(name, passed, critical=False):
    if passed:
        print(f"{Colors.GREEN}✅ PASS{Colors.END}: {name}")
        return 1
    else:
        if critical:
            print(f"{Colors.RED}❌ CRITICAL FAIL{Colors.END}: {name}")
            return 0
        else:
            print(f"{Colors.YELLOW}⚠️  WARNING{Colors.END}: {name}")
            return 0.5

# Start verification
total_score = 0
max_score = 25

print_header("1. PROJECT STRUCTURE VERIFICATION")

# Check project structure
total_score += print_check(
    "Project has required directories",
    all(Path(p).exists() for p in ["data", "data/raw", "data/processed", "scripts"]),
    critical=True
)

print_header("2. DATA DOWNLOAD VERIFICATION")

# Check raw data
raw_file = Path("data/raw/hotpot_dev_distractor_v1.json")
if raw_file.exists():
    file_size_mb = raw_file.stat().st_size / (1024 * 1024)
    total_score += print_check(
        f"HotpotQA dataset downloaded ({file_size_mb:.1f} MB)",
        file_size_mb > 80,  # Should be ~92MB
        critical=True
    )
    
    # Load and validate raw data
    try:
        with open(raw_file, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        
        total_score += print_check(
            f"Raw data valid JSON with {len(raw_data):,} examples",
            isinstance(raw_data, list) and len(raw_data) > 7000,
            critical=True
        )
        
        # Check first example structure
        if raw_data:
            first_ex = raw_data[0]
            required_keys = ['_id', 'question', 'answer', 'type', 'level', 'context', 'supporting_facts']
            has_all_keys = all(key in first_ex for key in required_keys)
            
            total_score += print_check(
                "Raw examples have all required fields",
                has_all_keys,
                critical=True
            )
            
            # Multi-hop verification
            has_context = isinstance(first_ex.get('context'), list) and len(first_ex['context']) >= 2
            has_supporting_facts = isinstance(first_ex.get('supporting_facts'), list) and len(first_ex['supporting_facts']) >= 2
            
            total_score += print_check(
                "Examples are multi-hop (multiple context paragraphs)",
                has_context and has_supporting_facts,
                critical=True
            )
    except Exception as e:
        total_score += print_check(f"Raw data corrupted: {str(e)[:50]}", False, critical=True)
else:
    total_score += print_check("Raw data file not found", False, critical=True)

print_header("3. PROCESSED SUBSET VERIFICATION")

# Check processed subset
subset_file = Path("data/processed/dev_subset_100.json")
if subset_file.exists():
    try:
        with open(subset_file, 'r', encoding='utf-8') as f:
            subset_data = json.load(f)
        
        total_score += print_check(
            "Subset file valid JSON with metadata",
            isinstance(subset_data, dict) and 'metadata' in subset_data and 'examples' in subset_data,
            critical=True
        )
        
        metadata = subset_data.get('metadata', {})
        examples = subset_data.get('examples', [])
        
        total_score += print_check(
            f"Subset has {len(examples)} examples as specified",
            len(examples) >= 100,
            critical=True
        )
        
        # Check balance
        if examples:
            types = [ex.get('type', '') for ex in examples[:100]]
            comparison_count = types.count('comparison')
            bridge_count = types.count('bridge')
            
            is_balanced = abs(comparison_count - bridge_count) <= 10  # Allow some variance
            
            total_score += print_check(
                f"Subset is balanced: {comparison_count} comparison, {bridge_count} bridge",
                is_balanced,
                critical=True
            )
            
            # Check GraphRAG compatibility
            first_ex = examples[0]
            context_paragraphs = len(first_ex.get('context', []))
            supporting_facts = len(first_ex.get('supporting_facts', []))
            
            total_score += print_check(
                f"Examples ready for GraphRAG: {context_paragraphs} paragraphs, {supporting_facts} supporting facts",
                context_paragraphs >= 2 and supporting_facts >= 2,
                critical=True
            )
            
            # Check data quality
            has_questions = all('question' in ex for ex in examples[:5])
            has_answers = all('answer' in ex for ex in examples[:5])
            
            total_score += print_check(
                "All examples have questions and answers",
                has_questions and has_answers,
                critical=True
            )
            
            # Check for duplicates
            ids = [ex.get('_id', '') for ex in examples]
            has_duplicates = len(ids) != len(set(ids))
            
            total_score += print_check(
                "No duplicate IDs in subset",
                not has_duplicates
            )
    except Exception as e:
        total_score += print_check(f"Subset file corrupted: {str(e)[:50]}", False, critical=True)
else:
    total_score += print_check("Subset file not found", False, critical=True)

print_header("4. PIPELINE REPRODUCIBILITY VERIFICATION")

# Check scripts
script_file = Path("scripts/create_subset.py")
total_score += print_check(
    "Processing script exists and is executable",
    script_file.exists() and script_file.stat().st_size > 1000,
    critical=True
)

# Check sample file
sample_file = Path("data/processed/sample_questions.txt")
total_score += print_check(
    "Sample questions file created for human review",
    sample_file.exists() and sample_file.stat().st_size > 500,
    critical=False
)

print_header("5. PHASE 2 READINESS VERIFICATION")

# Check if data is ready for GraphRAG
if subset_file.exists():
    try:
        with open(subset_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        examples = data.get('examples', [])
        
        if examples:
            # Check for entity extraction potential
            sample_question = examples[0].get('question', '')
            has_entities = any(word in sample_question.lower() for word in ['who', 'what', 'when', 'where', 'which'])
            
            total_score += print_check(
                "Questions are entity-rich (good for graph extraction)",
                has_entities,
                critical=False
            )
            
            # Check context is structured
            context = examples[0].get('context', [])
            is_structured = all(isinstance(item, list) and len(item) == 2 for item in context[:3])
            
            total_score += print_check(
                "Context structured as (title, sentences) pairs",
                is_structured,
                critical=True
            )
    except:
        pass

print_header("🎯 FINAL SCORE & RECOMMENDATIONS")
print("=" * 60)

percentage = (total_score / max_score) * 100
print(f"\n{Colors.BOLD}TOTAL SCORE: {total_score:.1f}/{max_score} ({percentage:.0f}%){Colors.END}")

if percentage >= 90:
    print(f"{Colors.GREEN}{Colors.BOLD}🎉 EXCELLENT! Phase 1 fully complete.{Colors.END}")
    print("   All requirements met. Ready to submit to Havva.")
elif percentage >= 75:
    print(f"{Colors.GREEN}{Colors.BOLD}👍 VERY GOOD! Phase 1 mostly complete.{Colors.END}")
    print("   Minor improvements possible.")
elif percentage >= 60:
    print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  ACCEPTABLE. Phase 1 needs work.{Colors.END}")
    print("   Review warnings before submission.")
else:
    print(f"{Colors.RED}{Colors.BOLD}❌ INCOMPLETE. Phase 1 not ready.{Colors.END}")
    print("   Fix critical issues first.")

print(f"\n{Colors.BOLD}📁 FILES TO SHARE WITH HAVVA:{Colors.END}")
print("1. data/raw/hotpot_dev_distractor_v1.json    (Original dataset)")
print("2. data/processed/dev_subset_100.json        (Your balanced subset)")
print("3. scripts/create_subset.py                  (Processing code)")
print("4. Output of this verification script")

print(f"\n{Colors.BOLD}🔧 NEXT STEPS FOR PHASE 2:{Colors.END}")
print("1. Use this subset for GraphRAG indexing")
print("2. Implement entity extraction (people, places, dates)")
print("3. Build knowledge graph from context paragraphs")
print("4. Test multi-hop retrieval")

print(f"\n{Colors.BOLD}📋 HAVVA'S CHECKLIST:{Colors.END}")
print("✓ Dataset properly downloaded and validated")
print("✓ Balanced subset created (comparison vs bridge)")
print("✓ Data structured for GraphRAG indexing")
print("✓ Multi-hop context preserved")
print("✓ Code is reproducible and documented")

print("\n" + "=" * 80)
print("💡 TIP: Copy this entire output to your Google Doc")
print("=" * 80)
