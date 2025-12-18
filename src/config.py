"""
Configuration for Phase 1: Data Preparation
"""
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Config:
    """Configuration parameters for Phase 1."""
    
    # Project paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent
    
    # Data directories
    DATA_DIR: Path = PROJECT_ROOT / "data"
    RAW_DATA_DIR: Path = DATA_DIR / "raw"
    PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
    REPORTS_DIR: Path = PROJECT_ROOT / "reports"
    
    # Data files
    HOTPOTQA_URL: str = "http://curtis.ml.cmu.edu/datasets/hotpot/hotpot_dev_distractor_v1.json"
    HOTPOTQA_FILENAME: str = "hotpot_dev_distractor_v1.json"
    
    # Processing parameters
    SUBSET_SIZE: int = 500
    CHUNK_SIZE: int = 1200  # tokens (as per LightRAG paper)
    CHUNK_OVERLAP: int = 200  # tokens
    
    # Random seed for reproducibility
    RANDOM_SEED: int = 42
    
    def __post_init__(self):
        """Create directories if they don't exist."""
        for dir_path in [
            self.RAW_DATA_DIR, 
            self.PROCESSED_DATA_DIR, 
            self.REPORTS_DIR / "data_analysis"
        ]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    @property
    def raw_data_path(self) -> Path:
        return self.RAW_DATA_DIR / self.HOTPOTQA_FILENAME
    
    @property
    def subset_json_path(self) -> Path:
        return self.PROCESSED_DATA_DIR / f"dev_subset_{self.SUBSET_SIZE}.json"
