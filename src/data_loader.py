"""
Simple data loader for HotpotQA - Phase 1
"""
import json
from pathlib import Path

class HotpotQADataLoader:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.processed_dir = self.data_dir / "processed"
    
    def load_subset(self, subset_name: str = "dev_subset_100") -> list:
        """Load the processed subset - FIXED VERSION"""
        subset_path = self.processed_dir / f"{subset_name}.json"
        
        if not subset_path.exists():
            raise FileNotFoundError(f"Subset not found: {subset_path}")
        
        with open(subset_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # EXTRACT THE EXAMPLES CORRECTLY
        if isinstance(data, dict):
            # Try to find examples list
            if 'examples' in data:
                return data['examples']
            elif 'data' in data:
                return data['data']
            else:
                # Search for any list in the dict
                for value in data.values():
                    if isinstance(value, list):
                        return value
                return []
        elif isinstance(data, list):
            return data
        else:
            return []
