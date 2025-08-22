import spotipy
from spotipy.oauth2 import SpotifyOAuth
from typing import List, Dict, Any, Optional
from loguru import logger
from .config import Config

class SpotifyClient:
    """Client for interacting with Spotify API."""
    
    def __init__(self):
        """Initialize Spotify client with OAuth authentication."""
        self.sp = None
        self._authenticate()
    
    def _authenticate(self) -> None:
        """Authenticate with Spotify API using OAuth."""
        try:
            auth_manager = SpotifyOAuth(
                client_id=Config.SPOTIFY_CLIENT_ID,
                client_secret=Config.SPOTIFY_CLIENT_SECRET,
                redirect_uri=Config.SPOTIFY_REDIRECT_URI,
                scope=Config.SPOTIFY_SCOPE,
                cache_path=".spotify_cache"
            )
            
            self.sp = spotipy.Spotify(auth_manager=auth_manager)
            
            # Test authentication
            user = self.sp.current_user()
            logger.info(f"Successfully authenticated with Spotify as: {user['display_name']}")
            
        except Exception as e:
            logger.error(f"Failed to authenticate with Spotify: {e}")
            raise
    
    def get_user_playlists(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get all user playlists including liked songs and followed playlists."""
        try:
            playlists = []
            results = self.sp.current_user_playlists(limit=limit)
            
            while results:
                for playlist in results['items']:
                    # Include all playlists (owned, followed, and system playlists like Liked Songs)
                    playlists.append({
                        'id': playlist['id'],
                        'name': playlist['name'],
                        'description': playlist['description'],
                        'track_count': playlist['tracks']['total'],
                        'public': playlist['public'],
                        'collaborative': playlist['collaborative'],
                        'owner': playlist['owner']['display_name'] or playlist['owner']['id']
                    })
                
                if results['next']:
                    results = self.sp.next(results)
                else:
                    break
            
            # Add "Liked Songs" as a special playlist if user has saved tracks
            try:
                saved_tracks = self.sp.current_user_saved_tracks(limit=1)
                if saved_tracks['total'] > 0:
                    playlists.insert(0, {
                        'id': 'liked_songs',
                        'name': 'Liked Songs',
                        'description': 'Your liked songs from Spotify',
                        'track_count': saved_tracks['total'],
                        'public': False,
                        'collaborative': False,
                        'owner': 'Spotify'
                    })
            except Exception as e:
                logger.warning(f"Could not fetch liked songs: {e}")
            
            logger.info(f"Found {len(playlists)} playlists (including followed and system playlists)")
            return playlists
            
        except Exception as e:
            logger.error(f"Failed to get user playlists: {e}")
            raise
    
    def get_playlist_tracks(self, playlist_id: str) -> List[Dict[str, Any]]:
        """Get all tracks from a specific playlist."""
        try:
            tracks = []
            
            # Handle special case for "Liked Songs"
            if playlist_id == 'liked_songs':
                results = self.sp.current_user_saved_tracks(limit=50)
            else:
                results = self.sp.playlist_tracks(playlist_id, limit=100)
            
            while results:
                for item in results['items']:
                    if item['track'] and item['track']['type'] == 'track':
                        track = item['track']
                        
                        # Extract artist names
                        artists = [artist['name'] for artist in track['artists']]
                        
                        # Get album information
                        album = track['album']
                        
                        track_info = {
                            'id': track['id'],
                            'name': track['name'],
                            'artists': artists,
                            'primary_artist': artists[0] if artists else '',
                            'album': album['name'],
                            'release_date': album['release_date'],
                            'duration_ms': track['duration_ms'],
                            'popularity': track['popularity'],
                            'explicit': track['explicit'],
                            'preview_url': track['preview_url'],
                            'external_urls': track['external_urls'],
                            'isrc': track.get('external_ids', {}).get('isrc'),
                            'search_query': self._create_search_query(track['name'], artists)
                        }
                        
                        tracks.append(track_info)
                
                if results['next']:
                    results = self.sp.next(results)
                else:
                    break
            
            logger.info(f"Retrieved {len(tracks)} tracks from playlist {playlist_id}")
            return tracks
            
        except Exception as e:
            logger.error(f"Failed to get playlist tracks: {e}")
            raise
    
    def get_playlist_info(self, playlist_id: str) -> Dict[str, Any]:
        """Get detailed information about a playlist."""
        try:
            # Handle special case for "Liked Songs"
            if playlist_id == 'liked_songs':
                # Get user info for owner name
                user = self.sp.current_user()
                # Get saved tracks count
                saved_tracks = self.sp.current_user_saved_tracks(limit=1)
                
                return {
                    'id': 'liked_songs',
                    'name': 'Liked Songs',
                    'description': 'Your liked songs collection',
                    'owner': user['display_name'],
                    'track_count': saved_tracks['total'],
                    'public': False,
                    'collaborative': False,
                    'followers': 0,
                    'external_urls': {},
                    'images': []
                }
            
            playlist = self.sp.playlist(playlist_id)
            
            return {
                'id': playlist['id'],
                'name': playlist['name'],
                'description': playlist['description'],
                'owner': playlist['owner']['display_name'],
                'track_count': playlist['tracks']['total'],
                'public': playlist['public'],
                'collaborative': playlist['collaborative'],
                'followers': playlist['followers']['total'],
                'external_urls': playlist['external_urls'],
                'images': playlist['images']
            }
            
        except Exception as e:
            logger.error(f"Failed to get playlist info: {e}")
            raise
    
    def search_track(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for tracks on Spotify."""
        try:
            results = self.sp.search(q=query, type='track', limit=limit)
            tracks = []
            
            for track in results['tracks']['items']:
                artists = [artist['name'] for artist in track['artists']]
                
                track_info = {
                    'id': track['id'],
                    'name': track['name'],
                    'artists': artists,
                    'primary_artist': artists[0] if artists else '',
                    'album': track['album']['name'],
                    'popularity': track['popularity'],
                    'duration_ms': track['duration_ms']
                }
                
                tracks.append(track_info)
            
            return tracks
            
        except Exception as e:
            logger.error(f"Failed to search tracks: {e}")
            raise
    
    @staticmethod
    def _create_search_query(track_name: str, artists: List[str]) -> str:
        """Create a search query string for YouTube Music."""
        # Clean track name (remove features, remixes, etc. for better matching)
        clean_name = track_name
        
        # Remove common suffixes that might not exist on YouTube Music
        suffixes_to_remove = [
            ' - Remastered', ' - Remaster', ' (Remastered)', ' (Remaster)',
            ' - Radio Edit', ' (Radio Edit)', ' - Single Version', ' (Single Version)'
        ]
        
        for suffix in suffixes_to_remove:
            if suffix.lower() in clean_name.lower():
                clean_name = clean_name.replace(suffix, '')
        
        # Combine primary artist and track name
        primary_artist = artists[0] if artists else ''
        return f"{primary_artist} {clean_name}".strip()