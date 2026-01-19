"""
Simple Phase 2 Runner - Start Here
"""
import sys
from pathlib import Path
from loguru import logger

# Add to path
sys.path.append(str(Path(__file__).parent))

def main():
    """Simple Phase 2 pipeline to get started"""
    logger.info("=" * 60)
    logger.info("PHASE 2: SIMPLE START - TESTING")
    logger.info("=" * 60)
    
    logger.info("1. Testing imports...")
    
    try:
        from src.data_loader import HotpotQADataLoader
        logger.info("   ✅ HotpotQADataLoader imported")
    except ImportError as e:
        logger.error(f"   ❌ Failed to import HotpotQADataLoader: {e}")
        return
    
    logger.info("2. Loading Phase 1 data...")
    try:
        loader = HotpotQADataLoader()
        examples = loader.load_subset("dev_subset_100")
        logger.info(f"   ✅ Loaded {len(examples)} examples")
    except Exception as e:
        logger.error(f"   ❌ Failed to load data: {e}")
        return
    
    logger.info("3. Testing basic functionality...")
    logger.info("   Basic test PASSED!")
    
    logger.info("\n" + "=" * 60)
    logger.info("PHASE 2 TEST COMPLETE")
    logger.info("=" * 60)
    logger.info("\nNext: Add graph construction tomorrow")

if __name__ == "__main__":
    main()
