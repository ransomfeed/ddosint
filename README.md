# DDoSINT - DDoSia Intelligence CLI Tool

**DDoSINT** is a command-line interface (CLI) tool for querying and extracting data from the DDoSia Monitor platform. It provides OSINT capabilities for analyzing DDoSia botnet targets.

## Features

- 🔍 **Search targets by host** - Search for specific hosts or partial matches
- 📅 **Extract targets by date** - Export all targets detected on a specific date
- 📊 **Retrieve statistics** - Get overview, yearly, monthly, and daily statistics
- 📋 **Multiple export formats** - Export data in JSON or CSV format
- 🗓️ **List available dates** - View all dates with available target data
- ⚙️ **Configurable** - Customize API base URL and output directories

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Install from source

1. Clone the repository:
```bash
git clone <repository-url>
cd ddosint
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package (optional, for global CLI access):
```bash
pip install -e .
```

### Prebuilt binaries (no install)

Starting from v1.0.0, we publish ready-to-run binaries for macOS, Linux and Windows in the GitHub Releases. Download the archive for your OS, extract it, and run `ddosint` (or `ddosint.exe` on Windows) from any folder.

```bash
# macOS / Linux example
./ddosint stats overview

# Windows (PowerShell)
./ddosint.exe stats overview
```

## Configuration

### Environment Variables

You can set the default DDoSia Monitor base URL using an environment variable:

```bash
export DDOSIA_BASE_URL="https://your-ddosia-monitor-instance.com"
```

If not set, the default is `https://ddosia.rfeed.it`.

### Command-line Options

All commands support the `--base-url` option to specify the API endpoint:

```bash
ddosint extract 2024-01-15 --base-url https://example.com
```

## Usage

### Extract Targets by Date

Extract all targets detected on a specific date:

```bash
# Export as JSON (default)
ddosint extract 2024-01-15

# Export as CSV
ddosint extract 2024-01-15 --format csv

# Specify output directory
ddosint extract 2024-01-15 --format csv --output-dir ./exports

# Custom filename prefix
ddosint extract 2024-01-15 --format json --prefix ddosia_targets
```

**Output:**
- JSON: Full API response including stats and targets array
- CSV: Only the targets list (one row per target)

### Search by Host

Search for targets matching a host name:

```bash
# Basic search
ddosint search example.com

# Limit displayed results
ddosint search example.com --limit 10

# Export results
ddosint search example.com --export --format json

# Export to specific directory
ddosint search example.com --export --format csv --output-dir ./results
```

### Get Statistics

Retrieve various statistics from the platform:

```bash
# Overview statistics
ddosint stats overview

# Statistics by year
ddosint stats by_year

# Statistics by month (last 12 months)
ddosint stats by_month

# Statistics by day (last 30 days)
ddosint stats by_day

# Monthly timeseries (for graphs)
ddosint stats timeseries_monthly

# Daily timeseries (last 30 days)
ddosint stats timeseries_daily

# Export statistics
ddosint stats overview --export --output-dir ./stats
```

### List Available Dates

View all dates with available target data:

```bash
# List all dates
ddosint dates

# Limit number of dates shown
ddosint dates --limit 20
```

## Examples

### Extract targets for multiple dates

```bash
# Extract targets for a week
for date in 2024-01-{15..21}; do
    ddosint extract $date --format csv --output-dir ./exports/week1
done
```

### Search and export

```bash
# Search for a domain and export results
ddosint search example.com --export --format json --output-dir ./searches
```

### Get daily statistics

```bash
# Get daily statistics and export
ddosint stats by_day --export --output-dir ./stats
```

## Output Formats

### JSON Format

JSON exports include the full API response with metadata:

```json
{
  "date": "2024-01-15",
  "stats": {
    "total_targets": 25,
    "total_requests": 80,
    "unique_hosts": 15,
    "unique_ips": 10,
    "types": ["http", "https"],
    "methods": ["GET", "POST"]
  },
  "targets": [
    {
      "target_id": "...",
      "request_id": "...",
      "host": "example.com",
      "ip": "192.168.1.1",
      "type": "http",
      "method": "GET",
      "port": 80,
      "use_ssl": 0,
      "path": "/api/endpoint",
      "detected_at": "2024-01-15 14:30:00",
      "imported_at": "2024-01-15 14:35:00"
    }
  ],
  "count": 80
}
```

### CSV Format

CSV exports contain only the targets list with all available fields:

```csv
target_id,request_id,host,ip,type,method,port,use_ssl,path,detected_at,imported_at
target_123,req_456,example.com,192.168.1.1,http,GET,80,0,/api/endpoint,2024-01-15 14:30:00,2024-01-15 14:35:00
```

## Error Handling

The CLI provides clear error messages for common issues:

- **Invalid date format**: Date must be in YYYY-MM-DD format
- **API connection errors**: Network or server issues
- **API errors**: Errors returned by the DDoSia Monitor API
- **File system errors**: Permission or path issues

## Exit Codes

- `0`: Success
- `1`: Error (invalid input, API error, etc.)

## Development

### Project Structure

# Local binary build (optional)
./scripts/build_local.sh
# Binary will be in ./dist
```
ddosint/
├── ddosint/
│   ├── __init__.py
│   ├── api_client.py      # API client implementation
│   ├── cli.py             # CLI interface
│   └── export.py          # Export utilities
├── setup.py
├── requirements.txt
├── README.md
└── .gitignore
```

### Running Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is part of the Ransomfeed project ecosystem.

## Related Projects

- [DDoSia Monitor](https://ddosia.rfeed.it) - The web platform this CLI interfaces with

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.

---

**DDoSINT** - DDoSia Intelligence CLI Tool  
Part of the Ransomfeed project ecosystem

