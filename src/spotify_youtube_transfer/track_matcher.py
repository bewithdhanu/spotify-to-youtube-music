from typing import List, Dict, Any, Optional, Tuple
from fuzzywuzzy import fuzz, process
from loguru import logger
from .config import Config
import re

class TrackMatcher:
    """Handles matching Spotify tracks to YouTube Music tracks."""
    
    def __init__(self, youtube_client):
        """Initialize track matcher with YouTube Music client."""
        self.youtube_client = youtube_client
        self.match_threshold = Config.MATCH_THRESHOLD
    
    def find_best_match(self, spotify_track: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find the best YouTube Music match for a Spotify track."""
        try:
            # Create search queries with different strategies
            search_queries = self._generate_search_queries(spotify_track)
            
            best_match = None
            best_score = 0
            
            for query in search_queries:
                logger.debug(f"Searching YouTube Music with query: {query}")
                
                # Search YouTube Music
                youtube_results = self.youtube_client.search_song(query)
                
                if not youtube_results:
                    continue
                
                # Find best match from results
                match, score = self._find_best_match_from_results(
                    spotify_track, youtube_results
                )
                
                if match and score > best_score:
                    best_match = match
                    best_score = score
                    
                    # If we found a very good match, stop searching
                    if score >= 0.95:
                        break
            
            if best_match and best_score >= self.match_threshold:
                logger.info(
                    f"Found match for '{spotify_track['name']}' by {spotify_track['primary_artist']} "
                    f"-> '{best_match['title']}' by {best_match['primary_artist']} (score: {best_score:.2f})"
                )
                return {
                    **best_match,
                    'match_score': best_score,
                    'spotify_track': spotify_track
                }
            else:
                logger.warning(
                    f"No suitable match found for '{spotify_track['name']}' by {spotify_track['primary_artist']} "
                    f"(best score: {best_score:.2f})"
                )
                return None
                
        except Exception as e:
            logger.error(f"Error finding match for '{spotify_track['name']}': {e}")
            return None
    
    def _generate_search_queries(self, spotify_track: Dict[str, Any]) -> List[str]:
        """Generate multiple search query variations for better matching."""
        track_name = spotify_track['name']
        primary_artist = spotify_track['primary_artist']
        all_artists = spotify_track['artists']
        
        queries = []
        
        # Clean track name
        clean_track_name = self._clean_track_name(track_name)
        
        # Strategy 1: Primary artist + clean track name
        queries.append(f"{primary_artist} {clean_track_name}")
        
        # Strategy 2: Original track name + primary artist
        queries.append(f"{primary_artist} {track_name}")
        
        # Strategy 3: Just track name + primary artist (reversed)
        queries.append(f"{clean_track_name} {primary_artist}")
        
        # Strategy 4: Track name only (for very popular songs)
        if len(clean_track_name) > 10:  # Only for longer track names
            queries.append(clean_track_name)
        
        # Strategy 5: Include featuring artists if present
        if len(all_artists) > 1:
            featuring_artists = ' '.join(all_artists[:3])  # Limit to first 3 artists
            queries.append(f"{featuring_artists} {clean_track_name}")
        
        # Strategy 6: Remove common words that might not match
        simplified_name = self._simplify_track_name(track_name)
        if simplified_name != clean_track_name:
            queries.append(f"{primary_artist} {simplified_name}")
        
        # Remove duplicates while preserving order
        unique_queries = []
        for query in queries:
            if query not in unique_queries:
                unique_queries.append(query)
        
        return unique_queries[:5]  # Limit to 5 queries to avoid rate limiting
    
    def _clean_track_name(self, track_name: str) -> str:
        """Clean track name by removing common suffixes and parenthetical content."""
        clean_name = track_name
        
        # Remove remaster/reissue information
        patterns_to_remove = [
            r'\s*-\s*Remaster(ed)?.*$',
            r'\s*\(Remaster(ed)?.*?\)',
            r'\s*-\s*\d{4}\s*Remaster.*$',
            r'\s*\(\d{4}\s*Remaster.*?\)',
            r'\s*-\s*Radio Edit.*$',
            r'\s*\(Radio Edit.*?\)',
            r'\s*-\s*Single Version.*$',
            r'\s*\(Single Version.*?\)',
            r'\s*-\s*Album Version.*$',
            r'\s*\(Album Version.*?\)',
            r'\s*-\s*Explicit.*$',
            r'\s*\(Explicit.*?\)',
        ]
        
        for pattern in patterns_to_remove:
            clean_name = re.sub(pattern, '', clean_name, flags=re.IGNORECASE)
        
        return clean_name.strip()
    
    def _simplify_track_name(self, track_name: str) -> str:
        """Further simplify track name by removing more content."""
        simplified = self._clean_track_name(track_name)
        
        # Remove all parenthetical content
        simplified = re.sub(r'\s*\([^)]*\)', '', simplified)
        
        # Remove content after dash (often remix/version info)
        if ' - ' in simplified:
            simplified = simplified.split(' - ')[0]
        
        # Remove featuring information
        feat_patterns = [
            r'\s*feat\.?\s+.*$',
            r'\s*featuring\s+.*$',
            r'\s*ft\.?\s+.*$',
            r'\s*with\s+.*$'
        ]
        
        for pattern in feat_patterns:
            simplified = re.sub(pattern, '', simplified, flags=re.IGNORECASE)
        
        return simplified.strip()
    
    def _find_best_match_from_results(
        self, 
        spotify_track: Dict[str, Any], 
        youtube_results: List[Dict[str, Any]]
    ) -> Tuple[Optional[Dict[str, Any]], float]:
        """Find the best match from YouTube Music search results."""
        best_match = None
        best_score = 0
        
        spotify_title = spotify_track['name'].lower()
        spotify_artist = spotify_track['primary_artist'].lower()
        spotify_artists = [artist.lower() for artist in spotify_track['artists']]
        
        for result in youtube_results:
            youtube_title = result['title'].lower()
            youtube_artist = result['primary_artist'].lower()
            youtube_artists = [artist.lower() for artist in result['artists']]
            
            # Calculate title similarity
            title_score = fuzz.ratio(spotify_title, youtube_title) / 100.0
            
            # Calculate artist similarity
            artist_score = 0
            
            # Check primary artist match
            primary_artist_score = fuzz.ratio(spotify_artist, youtube_artist) / 100.0
            
            # Check if any Spotify artist matches any YouTube artist
            cross_artist_scores = []
            for s_artist in spotify_artists:
                for y_artist in youtube_artists:
                    cross_artist_scores.append(fuzz.ratio(s_artist, y_artist) / 100.0)
            
            if cross_artist_scores:
                max_cross_score = max(cross_artist_scores)
                artist_score = max(primary_artist_score, max_cross_score)
            else:
                artist_score = primary_artist_score
            
            # Calculate combined score with weights
            # Title is more important than artist for matching
            combined_score = (title_score * 0.7) + (artist_score * 0.3)
            
            # Bonus for exact artist match
            if artist_score > 0.9:
                combined_score += 0.05
            
            # Bonus for similar duration (if available)
            if 'duration_ms' in spotify_track and result.get('duration'):
                duration_bonus = self._calculate_duration_bonus(
                    spotify_track['duration_ms'], 
                    result['duration']
                )
                combined_score += duration_bonus
            
            if combined_score > best_score:
                best_match = result
                best_score = combined_score
        
        return best_match, best_score
    
    def _calculate_duration_bonus(self, spotify_duration_ms: int, youtube_duration: str) -> float:
        """Calculate bonus score based on duration similarity."""
        try:
            # Parse YouTube duration (format: "3:45" or "3:45:12")
            youtube_parts = youtube_duration.split(':')
            if len(youtube_parts) == 2:  # MM:SS
                youtube_seconds = int(youtube_parts[0]) * 60 + int(youtube_parts[1])
            elif len(youtube_parts) == 3:  # HH:MM:SS
                youtube_seconds = int(youtube_parts[0]) * 3600 + int(youtube_parts[1]) * 60 + int(youtube_parts[2])
            else:
                return 0
            
            spotify_seconds = spotify_duration_ms / 1000
            
            # Calculate difference percentage
            duration_diff = abs(spotify_seconds - youtube_seconds)
            duration_diff_percent = duration_diff / spotify_seconds
            
            # Give bonus if duration is within 10% difference
            if duration_diff_percent <= 0.1:
                return 0.05
            elif duration_diff_percent <= 0.2:
                return 0.02
            else:
                return 0
                
        except (ValueError, ZeroDivisionError):
            return 0
    
    def batch_match_tracks(self, spotify_tracks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Match multiple tracks in batch."""
        matched_tracks = []
        failed_matches = []
        
        logger.info(f"Starting batch matching for {len(spotify_tracks)} tracks")
        
        for i, track in enumerate(spotify_tracks, 1):
            logger.info(f"Matching track {i}/{len(spotify_tracks)}: {track['name']} by {track['primary_artist']}")
            
            match = self.find_best_match(track)
            if match:
                matched_tracks.append(match)
            else:
                failed_matches.append(track)
        
        logger.info(
            f"Batch matching completed: {len(matched_tracks)} successful, "
            f"{len(failed_matches)} failed"
        )
        
        if failed_matches:
            logger.warning("Failed to match the following tracks:")
            for track in failed_matches:
                logger.warning(f"  - {track['name']} by {track['primary_artist']}")
        
        return matched_tracks