from ytmusicapi import YTMusic, OAuthCredentials
from ytmusicapi import setup_oauth
from typing import List, Dict, Any, Optional
from loguru import logger
from .config import Config
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class YouTubeMusicClient:
    """Client for interacting with YouTube Music API."""
    
    def __init__(self):
        """Initialize YouTube Music client."""
        self.ytmusic = None
        self._authenticate()
    
    def _authenticate(self) -> None:
        """Authenticate with YouTube Music API using OAuth2."""
        oauth_path = 'oauth.json'
        
        if not os.path.exists(oauth_path):
            logger.error("YouTube Music OAuth authentication file not found.")
            logger.info("Please set up YouTube Music OAuth2 authentication:")
            logger.info("")
            logger.info("1. Go to Google Cloud Console (https://console.cloud.google.com/)")
            logger.info("2. Create a project and enable YouTube Data API v3")
            logger.info("3. Create OAuth2 credentials (TVs and Limited Input devices)")
            logger.info("4. Add YOUTUBE_CLIENT_ID and YOUTUBE_CLIENT_SECRET to your .env file")
            logger.info("5. Run: python -c \"from ytmusicapi import setup_oauth; setup_oauth('oauth.json')\"")
            logger.info("6. Follow the authentication flow in your browser")
            raise FileNotFoundError("YouTube Music OAuth authentication not configured")
        
        try:
            # Load OAuth credentials from environment if available
            client_id = os.getenv('YOUTUBE_CLIENT_ID')
            client_secret = os.getenv('YOUTUBE_CLIENT_SECRET')
            
            if client_id and client_secret:
                # Use OAuth with credentials for token refresh
                oauth_credentials = OAuthCredentials(
                    client_id=client_id,
                    client_secret=client_secret
                )
                self.ytmusic = YTMusic(oauth_path, oauth_credentials=oauth_credentials)
                logger.info("YouTube Music OAuth2 initialized with token refresh capability")
            else:
                # Use OAuth token file only (no refresh capability)
                self.ytmusic = YTMusic(oauth_path)
                logger.warning("YouTube Music OAuth2 initialized without refresh capability")
                logger.warning("Add YOUTUBE_CLIENT_ID and YOUTUBE_CLIENT_SECRET to .env for token refresh")
            
            # Test OAuth authentication
            playlists = self.ytmusic.get_library_playlists(limit=1)
            logger.info("Successfully authenticated with YouTube Music using OAuth2")
            
        except Exception as e:
            logger.error(f"OAuth authentication failed: {e}")
            logger.info("Please check your OAuth setup:")
            logger.info("1. Ensure oauth.json exists and is valid")
            logger.info("2. Check YOUTUBE_CLIENT_ID and YOUTUBE_CLIENT_SECRET in .env")
            logger.info("3. Re-run OAuth setup if needed: python -c \"from ytmusicapi import setup_oauth; setup_oauth('oauth.json')\"")
            raise
    
    def search_song(self, query: str, limit: int = None) -> List[Dict[str, Any]]:
        """Search for songs on YouTube Music."""
        try:
            if limit is None:
                limit = Config.MAX_SEARCH_RESULTS
            
            results = self.ytmusic.search(query, filter='songs', limit=limit)
            
            songs = []
            for result in results:
                if result.get('resultType') == 'song':
                    # Extract artist information
                    artists = []
                    if 'artists' in result and result['artists']:
                        artists = [artist['name'] for artist in result['artists']]
                    
                    song_info = {
                        'videoId': result.get('videoId'),
                        'title': result.get('title', ''),
                        'artists': artists,
                        'primary_artist': artists[0] if artists else '',
                        'album': result.get('album', {}).get('name', '') if result.get('album') else '',
                        'duration': result.get('duration', ''),
                        'thumbnails': result.get('thumbnails', []),
                        'isExplicit': result.get('isExplicit', False),
                        'feedbackTokens': result.get('feedbackTokens')
                    }
                    
                    songs.append(song_info)
            
            logger.debug(f"Found {len(songs)} songs for query: {query}")
            return songs
            
        except Exception as e:
            logger.error(f"Failed to search for song '{query}': {e}")
            return []
    
    def create_playlist(self, title: str, description: str = '', privacy_status: str = 'PRIVATE') -> Optional[str]:
        """Create a new playlist on YouTube Music."""
        try:
            playlist_id = self.ytmusic.create_playlist(
                title=title,
                description=description,
                privacy_status=privacy_status
            )
            
            logger.info(f"Created playlist '{title}' with ID: {playlist_id}")
            return playlist_id
            
        except Exception as e:
            logger.error(f"Failed to create playlist '{title}': {e}")
            return None
    
    def add_songs_to_playlist(self, playlist_id: str, video_ids: List[str]) -> bool:
        """Add songs to a playlist."""
        try:
            if not video_ids:
                logger.warning("No video IDs provided to add to playlist")
                return True
            
            # YouTube Music API can handle multiple songs at once
            response = self.ytmusic.add_playlist_items(
                playlistId=playlist_id,
                videoIds=video_ids
            )
            
            if response.get('status') == 'STATUS_SUCCEEDED':
                logger.info(f"Successfully added {len(video_ids)} songs to playlist {playlist_id}")
                return True
            else:
                logger.error(f"Failed to add songs to playlist: {response}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to add songs to playlist {playlist_id}: {e}")
            return False
    
    def get_library_playlists(self, limit: int = 25, fetch_track_counts: bool = True) -> List[Dict[str, Any]]:
        """Get user's library playlists with accurate track counts."""
        try:
            playlists = self.ytmusic.get_library_playlists(limit=limit)
            
            playlist_info = []
            for playlist in playlists:
                info = {
                    'playlistId': playlist.get('playlistId'),
                    'title': playlist.get('title', ''),
                    'description': playlist.get('description', ''),
                    'count': playlist.get('count', 0),
                    'thumbnails': playlist.get('thumbnails', [])
                }
                
                # Fetch actual track count if requested
                if fetch_track_counts:
                    try:
                        # Get playlist with limit=None to retrieve all tracks
                        detailed = self.ytmusic.get_playlist(playlist.get('playlistId'), limit=None)
                        if detailed and 'tracks' in detailed:
                            info['actual_count'] = len(detailed['tracks'])
                        else:
                            info['actual_count'] = 0
                    except Exception as e:
                        logger.warning(f"Failed to get track count for playlist {playlist.get('title', 'Unknown')}: {e}")
                        info['actual_count'] = info['count']  # Fallback to metadata count
                else:
                    info['actual_count'] = info['count']
                
                playlist_info.append(info)
            
            logger.info(f"Retrieved {len(playlist_info)} library playlists")
            return playlist_info
            
        except Exception as e:
            logger.error(f"Failed to get library playlists: {e}")
            return []
    
    def get_playlist(self, playlist_id: str, limit: int = None) -> Optional[Dict[str, Any]]:
        """Get playlist information and tracks."""
        try:
            playlist = self.ytmusic.get_playlist(playlist_id, limit=limit)
            
            if not playlist:
                return None
            
            # Extract track information
            tracks = []
            for track in playlist.get('tracks', []):
                track_info = {
                    'videoId': track.get('videoId'),
                    'title': track.get('title', ''),
                    'artists': [artist['name'] for artist in track.get('artists', [])],
                    'album': track.get('album', {}).get('name', '') if track.get('album') else '',
                    'duration': track.get('duration', ''),
                    'thumbnails': track.get('thumbnails', [])
                }
                tracks.append(track_info)
            
            playlist_info = {
                'id': playlist.get('id'),
                'title': playlist.get('title', ''),
                'description': playlist.get('description', ''),
                'owner': playlist.get('owner', ''),
                'trackCount': len(tracks),
                'tracks': tracks,
                'thumbnails': playlist.get('thumbnails', [])
            }
            
            return playlist_info
            
        except Exception as e:
            logger.error(f"Failed to get playlist {playlist_id}: {e}")
            return None
    
    def delete_playlist(self, playlist_id: str) -> bool:
        """Delete a playlist."""
        try:
            response = self.ytmusic.delete_playlist(playlist_id)
            logger.info(f"Deleted playlist {playlist_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete playlist {playlist_id}: {e}")
            return False
    
    def like_song(self, video_id: str) -> bool:
        """Like a song and add it to the liked songs playlist."""
        try:
            response = self.ytmusic.rate_song(video_id, 'LIKE')
            logger.debug(f"Successfully liked song {video_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to like song {video_id}: {e}")
            return False
    
    @staticmethod
    def setup_oauth_authentication() -> str:
        """Helper method to set up YouTube Music OAuth2 authentication."""
        logger.info("Setting up YouTube Music OAuth2 authentication...")
        logger.info("")
        logger.info("Prerequisites:")
        logger.info("1. Go to Google Cloud Console (https://console.cloud.google.com/)")
        logger.info("2. Create a project and enable YouTube Data API v3")
        logger.info("3. Create OAuth2 credentials (TVs and Limited Input devices)")
        logger.info("4. Add YOUTUBE_CLIENT_ID and YOUTUBE_CLIENT_SECRET to your .env file")
        logger.info("")
        logger.info("Setting up OAuth2 token...")
        
        try:
            oauth_path = 'oauth.json'
            setup_oauth(filepath=oauth_path)
            logger.info(f"OAuth2 authentication file created: {oauth_path}")
            logger.info("YouTube Music OAuth2 setup completed successfully!")
            return oauth_path
        except Exception as e:
            logger.error(f"Failed to setup OAuth2 authentication: {e}")
            logger.info("Make sure you have:")
            logger.info("1. Valid Google Cloud Console project with YouTube Data API v3 enabled")
            logger.info("2. OAuth2 credentials configured for 'TVs and Limited Input devices'")
            logger.info("3. YOUTUBE_CLIENT_ID and YOUTUBE_CLIENT_SECRET in your .env file")
            raise