"""
API Client for DDoSia Monitor
Handles all HTTP requests to the DDoSia Monitor API endpoints
"""

import requests
import json
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin


class DDoSiaAPIClient:
    """Client for interacting with DDoSia Monitor API"""
    
    def __init__(self, base_url: str, timeout: int = 30):
        """
        Initialize the API client
        
        Args:
            base_url: Base URL of the DDoSia Monitor instance (e.g., 'https://example.com')
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.api_base = f"{self.base_url}/api"
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'DDoSINT-CLI/1.0.0',
            'Accept': 'application/json'
        })
    
    def _request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make a GET request to the API
        
        Args:
            endpoint: API endpoint path (e.g., 'stats.php')
            params: Query parameters
            
        Returns:
            JSON response as dictionary
            
        Raises:
            requests.RequestException: If the request fails
            ValueError: If the API returns an error
        """
        url = urljoin(f"{self.api_base}/", endpoint)
        
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            # Check for API-level errors
            if 'error' in data:
                raise ValueError(f"API Error: {data['error']}")
            
            return data
            
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(
                f"Failed to connect to API: {str(e)}"
            )
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response: {str(e)}")
    
    def get_stats(self, stat_type: str = 'overview') -> Dict[str, Any]:
        """
        Get statistics from the API
        
        Args:
            stat_type: Type of statistics ('overview', 'by_year', 'by_month', 
                      'by_day', 'timeseries_monthly', 'timeseries_daily')
        
        Returns:
            Statistics data
        """
        return self._request('stats.php', {'type': stat_type})
    
    def get_recent_targets(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get recent targets (last 2 days)
        
        Args:
            limit: Maximum number of results
            
        Returns:
            List of recent targets
        """
        return self._request('recent_targets.php', {'limit': limit})
    
    def search_host(self, host: str) -> Dict[str, Any]:
        """
        Search for targets by host
        
        Args:
            host: Host name or partial match
            
        Returns:
            Search results with stats, targets, and timeline
        """
        return self._request('search_host.php', {'host': host})
    
    def get_targets_by_date(self, date: str) -> Dict[str, Any]:
        """
        Get all targets for a specific date
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            Targets data with stats for the specified date
        """
        # Validate date format
        import re
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
            raise ValueError("Date must be in YYYY-MM-DD format")
        
        return self._request('targets_by_date.php', {'date': date})
    
    def get_available_dates(self) -> List[Dict[str, Any]]:
        """
        Get list of available dates with data
        
        Returns:
            List of dates with target and request counts
        """
        return self._request('available_dates.php')

