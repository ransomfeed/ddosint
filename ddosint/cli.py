"""
Command-line interface for DDoSINT
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Optional
from datetime import datetime

from ddosint.api_client import DDoSiaAPIClient
from ddosint.export import DataExporter


class DDoSINTCLI:
    """Main CLI class"""
    
    def __init__(self):
        self.client: Optional[DDoSiaAPIClient] = None
        self.exporter = DataExporter()
    
    def setup_client(self, base_url: str) -> None:
        """Initialize API client"""
        self.client = DDoSiaAPIClient(base_url)
    
    def cmd_extract(self, args: argparse.Namespace) -> int:
        """
        Extract targets for a specific date
        
        Args:
            args: Parsed command-line arguments
            
        Returns:
            Exit code (0 for success, 1 for error)
        """
        if not self.client:
            self.setup_client(args.base_url)
        
        try:
            print(f"Fetching targets for date: {args.date}")
            data = self.client.get_targets_by_date(args.date)
            
            if not data.get('targets'):
                print(f"No targets found for date {args.date}")
                return 1
            
            # Determine output directory
            output_dir = args.output_dir or os.getcwd()
            output_dir = Path(output_dir).expanduser().resolve()
            
            # Export data
            output_file = self.exporter.export_targets_by_date(
                data,
                str(output_dir),
                format=args.format,
                filename_prefix=args.prefix
            )
            
            # Print summary
            stats = data.get('stats', {})
            print(f"\n✓ Export completed successfully!")
            print(f"  Date: {args.date}")
            print(f"  Total Targets: {stats.get('total_targets', 0)}")
            print(f"  Total Requests: {stats.get('total_requests', 0)}")
            print(f"  Unique Hosts: {stats.get('unique_hosts', 0)}")
            print(f"  Format: {args.format.upper()}")
            print(f"  Output: {output_file}")
            
            return 0
            
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            return 1
    
    def cmd_search(self, args: argparse.Namespace) -> int:
        """
        Search for targets by host
        
        Args:
            args: Parsed command-line arguments
            
        Returns:
            Exit code (0 for success, 1 for error)
        """
        if not self.client:
            self.setup_client(args.base_url)
        
        try:
            print(f"Searching for host: {args.host}")
            data = self.client.search_host(args.host)
            
            stats = data.get('stats', {})
            targets = data.get('targets', [])
            
            print(f"\nSearch Results:")
            print(f"  Total Targets: {stats.get('total_targets', 0)}")
            print(f"  Total Requests: {stats.get('total_requests', 0)}")
            print(f"  Unique IPs: {stats.get('unique_ips', 0)}")
            print(f"  Active Days: {stats.get('active_days', 0)}")
            print(f"  First Seen: {stats.get('first_seen', 'N/A')}")
            print(f"  Last Seen: {stats.get('last_seen', 'N/A')}")
            print(f"  Types: {', '.join(stats.get('types', []))}")
            print(f"  Methods: {', '.join(stats.get('methods', []))}")
            
            if args.limit and targets:
                print(f"\nShowing first {min(args.limit, len(targets))} targets:")
                for i, target in enumerate(targets[:args.limit], 1):
                    print(f"\n  [{i}] {target.get('host', 'N/A')}")
                    if 'ip' in target:
                        print(f"      IP: {target['ip']}")
                    if 'detected_at' in target:
                        print(f"      Detected: {target['detected_at']}")
            
            # Export if requested
            if args.export:
                output_dir = args.output_dir or os.getcwd()
                output_dir = Path(output_dir).expanduser().resolve()
                
                if args.format == 'json':
                    output_file = self.exporter.export_json(
                        data,
                        output_dir / f"search_{args.host.replace('.', '_')}.json"
                    )
                elif args.format == 'csv':
                    output_file = self.exporter.export_csv(
                        targets,
                        output_dir / f"search_{args.host.replace('.', '_')}.csv"
                    )
                
                print(f"\n✓ Exported to: {output_file}")
            
            return 0
            
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            return 1
    
    def cmd_stats(self, args: argparse.Namespace) -> int:
        """
        Display statistics
        
        Args:
            args: Parsed command-line arguments
            
        Returns:
            Exit code (0 for success, 1 for error)
        """
        if not self.client:
            self.setup_client(args.base_url)
        
        try:
            data = self.client.get_stats(args.type)
            
            if args.type == 'overview':
                print("\n=== Overview Statistics ===")
                print(f"Total Targets: {data.get('total_targets', 0)}")
                print(f"Total Requests: {data.get('total_requests', 0)}")
                print(f"Total Hosts: {data.get('total_hosts', 0)}")
                print(f"Total IPs: {data.get('total_ips', 0)}")
                print(f"Total Imports: {data.get('total_imports', 0)}")
                print(f"Last Detected: {data.get('last_detected', 'N/A')}")
            else:
                # Print as table
                print(f"\n=== Statistics ({args.type}) ===")
                if isinstance(data, list) and data:
                    # Print header
                    keys = list(data[0].keys())
                    print(" | ".join(keys))
                    print("-" * (len(" | ".join(keys)) + 10))
                    # Print rows
                    for row in data:
                        values = [str(row.get(k, '')) for k in keys]
                        print(" | ".join(values))
            
            # Export if requested
            if args.export:
                output_dir = args.output_dir or os.getcwd()
                output_dir = Path(output_dir).expanduser().resolve()
                
                output_file = self.exporter.export_json(
                    data,
                    output_dir / f"stats_{args.type}.json"
                )
                print(f"\n✓ Exported to: {output_file}")
            
            return 0
            
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            return 1
    
    def cmd_dates(self, args: argparse.Namespace) -> int:
        """
        List available dates
        
        Args:
            args: Parsed command-line arguments
            
        Returns:
            Exit code (0 for success, 1 for error)
        """
        if not self.client:
            self.setup_client(args.base_url)
        
        try:
            dates = self.client.get_available_dates()
            
            if not dates:
                print("No dates with data available")
                return 0
            
            print(f"\n=== Available Dates ({len(dates)} total) ===")
            print("Date       | Targets | Requests")
            print("-" * 40)
            
            for date_info in dates[:args.limit] if args.limit else dates:
                date = date_info.get('date', 'N/A')
                targets = date_info.get('target_count', 0)
                requests = date_info.get('request_count', 0)
                print(f"{date} | {targets:7d} | {requests:8d}")
            
            if args.limit and len(dates) > args.limit:
                print(f"\n... and {len(dates) - args.limit} more dates")
            
            return 0
            
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            return 1


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='DDoSINT - DDoSia Intelligence CLI Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract targets for a specific date
  ddosint extract 2024-01-15 --format csv --output-dir ./exports
  
  # Search for a host
  ddosint search example.com --limit 10
  
  # Get overview statistics
  ddosint stats overview
  
  # List available dates
  ddosint dates --limit 20
        """
    )
    
    # Global arguments
    parser.add_argument(
        '--base-url',
        default=os.getenv('DDOSIA_BASE_URL', 'https://ddosia.rfeed.it'),
        help='Base URL of DDoSia Monitor instance (default: from DDOSIA_BASE_URL env var or https://ddosia.rfeed.it)'
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract targets for a specific date')
    extract_parser.add_argument('date', help='Date in YYYY-MM-DD format')
    extract_parser.add_argument(
        '--format',
        choices=['json', 'csv'],
        default='json',
        help='Output format (default: json)'
    )
    extract_parser.add_argument(
        '--output-dir',
        help='Output directory (default: current directory)'
    )
    extract_parser.add_argument(
        '--prefix',
        default='targets',
        help='Filename prefix (default: targets)'
    )
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for targets by host')
    search_parser.add_argument('host', help='Host name or partial match')
    search_parser.add_argument(
        '--limit',
        type=int,
        help='Limit number of results displayed'
    )
    search_parser.add_argument(
        '--export',
        action='store_true',
        help='Export results to file'
    )
    search_parser.add_argument(
        '--format',
        choices=['json', 'csv'],
        default='json',
        help='Export format (default: json)'
    )
    search_parser.add_argument(
        '--output-dir',
        help='Output directory (default: current directory)'
    )
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Display statistics')
    stats_parser.add_argument(
        'type',
        choices=['overview', 'by_year', 'by_month', 'by_day', 'timeseries_monthly', 'timeseries_daily'],
        help='Type of statistics to retrieve'
    )
    stats_parser.add_argument(
        '--export',
        action='store_true',
        help='Export results to JSON file'
    )
    stats_parser.add_argument(
        '--output-dir',
        help='Output directory (default: current directory)'
    )
    
    # Dates command
    dates_parser = subparsers.add_parser('dates', help='List available dates with data')
    dates_parser.add_argument(
        '--limit',
        type=int,
        help='Limit number of dates displayed'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Initialize CLI
    cli = DDoSINTCLI()
    
    # Execute command
    if args.command == 'extract':
        return cli.cmd_extract(args)
    elif args.command == 'search':
        return cli.cmd_search(args)
    elif args.command == 'stats':
        return cli.cmd_stats(args)
    elif args.command == 'dates':
        return cli.cmd_dates(args)
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())

