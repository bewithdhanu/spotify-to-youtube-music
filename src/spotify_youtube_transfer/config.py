import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for Spotify to YouTube Music transfer tool."""
    
    # Spotify API Configuration
    SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI', 'http://localhost:8080/callback')
    SPOTIFY_SCOPE = 'playlist-read-private playlist-read-collaborative user-library-read'
    
    # YouTube Music Configuration
    YOUTUBE_CLIENT_ID = os.getenv('YOUTUBE_CLIENT_ID')
    YOUTUBE_CLIENT_SECRET = os.getenv('YOUTUBE_CLIENT_SECRET')
    
    # Matching Configuration
    MATCH_THRESHOLD = float(os.getenv('MATCH_THRESHOLD', '0.8'))  # Fuzzy matching threshold
    MAX_SEARCH_RESULTS = int(os.getenv('MAX_SEARCH_RESULTS', '5'))
    
    # Transfer Settings
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', '50'))  # Number of tracks to process at once
    RETRY_ATTEMPTS = int(os.getenv('RETRY_ATTEMPTS', '3'))
    RETRY_DELAY = float(os.getenv('RETRY_DELAY', '1.0'))  # Seconds between retries
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'spotify_to_youtube.log')
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """Validate required configuration values."""
        errors = []
        warnings = []
        
        # Spotify validation
        if not cls.SPOTIFY_CLIENT_ID:
            errors.append('SPOTIFY_CLIENT_ID is required')
        if not cls.SPOTIFY_CLIENT_SECRET:
            errors.append('SPOTIFY_CLIENT_SECRET is required')
        
        # YouTube Music validation
        oauth_path = 'oauth.json'
        if not os.path.exists(oauth_path):
            errors.append(f'YouTube Music OAuth file not found: {oauth_path}')
            errors.append('Run: python -c "from ytmusicapi import setup_oauth; setup_oauth(\'oauth.json\')" to set up OAuth')
        
        if not cls.YOUTUBE_CLIENT_ID or not cls.YOUTUBE_CLIENT_SECRET:
            warnings.append('YOUTUBE_CLIENT_ID and YOUTUBE_CLIENT_SECRET not set - token refresh will not be available')
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    @classmethod
    def get_spotify_config(cls) -> Dict[str, str]:
        """Get Spotify API configuration."""
        return {
            'client_id': cls.SPOTIFY_CLIENT_ID,
            'client_secret': cls.SPOTIFY_CLIENT_SECRET,
            'redirect_uri': cls.SPOTIFY_REDIRECT_URI,
            'scope': cls.SPOTIFY_SCOPE
        }