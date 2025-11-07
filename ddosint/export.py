"""
Export utilities for saving data in various formats
"""

import json
import csv
import os
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime


class DataExporter:
    """Handle data export to JSON and CSV formats"""
    
    @staticmethod
    def export_json(data: Any, output_path: str, pretty: bool = True) -> str:
        """
        Export data to JSON file
        
        Args:
            data: Data to export (dict, list, etc.)
            output_path: Full path to output file
            pretty: Whether to format JSON with indentation
            
        Returns:
            Path to the created file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            if pretty:
                json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                json.dump(data, f, ensure_ascii=False)
        
        return str(output_path)
    
    @staticmethod
    def export_csv(targets: List[Dict[str, Any]], output_path: str) -> str:
        """
        Export targets list to CSV file
        
        Args:
            targets: List of target dictionaries
            output_path: Full path to output file
            
        Returns:
            Path to the created file
        """
        if not targets:
            raise ValueError("No targets to export")
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Get all unique keys from all targets
        fieldnames = set()
        for target in targets:
            fieldnames.update(target.keys())
        fieldnames = sorted(list(fieldnames))
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(targets)
        
        return str(output_path)
    
    @staticmethod
    def export_targets_by_date(
        api_data: Dict[str, Any],
        output_dir: str,
        format: str = 'json',
        filename_prefix: str = 'targets'
    ) -> str:
        """
        Export targets by date data to file
        
        Args:
            api_data: Data from get_targets_by_date API call
            output_dir: Directory to save the file
            format: Export format ('json' or 'csv')
            filename_prefix: Prefix for the output filename
            
        Returns:
            Path to the created file
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        date = api_data.get('date', datetime.now().strftime('%Y-%m-%d'))
        targets = api_data.get('targets', [])
        
        if format.lower() == 'json':
            # Export full API response as JSON
            filename = f"{filename_prefix}_{date}.json"
            output_path = output_dir / filename
            return DataExporter.export_json(api_data, output_path)
        
        elif format.lower() == 'csv':
            # Export only targets list as CSV
            filename = f"{filename_prefix}_{date}.csv"
            output_path = output_dir / filename
            return DataExporter.export_csv(targets, output_path)
        
        else:
            raise ValueError(f"Unsupported format: {format}. Use 'json' or 'csv'")

