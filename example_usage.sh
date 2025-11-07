#!/bin/bash
# Example usage script for DDoSINT CLI

# Set base URL (optional, can use environment variable)
export DDOSIA_BASE_URL="https://ddosia.rfeed.it"

echo "=== DDoSINT CLI Examples ==="
echo ""

echo "1. Extract targets for a specific date (JSON):"
echo "   ddosint extract 2024-01-15"
echo ""

echo "2. Extract targets for a specific date (CSV):"
echo "   ddosint extract 2024-01-15 --format csv --output-dir ./exports"
echo ""

echo "3. Search for a host:"
echo "   ddosint search example.com --limit 10"
echo ""

echo "4. Search and export results:"
echo "   ddosint search example.com --export --format json --output-dir ./results"
echo ""

echo "5. Get overview statistics:"
echo "   ddosint stats overview"
echo ""

echo "6. Get statistics by year:"
echo "   ddosint stats by_year"
echo ""

echo "7. List available dates:"
echo "   ddosint dates --limit 20"
echo ""

echo "8. Extract with custom prefix:"
echo "   ddosint extract 2024-01-15 --format csv --prefix ddosia --output-dir ./exports"
echo ""

