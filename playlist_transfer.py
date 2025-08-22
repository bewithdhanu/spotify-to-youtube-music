from typing import List, Dict, Any, Optional
from loguru import logger
from tqdm import tqdm
import time
import json
from datetime import datetime

from spotify_client import SpotifyClient
from youtube_music_client import YouTubeMusicClient
from track_matcher import TrackMatcher
from config import Config

class PlaylistTransfer:
    """Main class for transferring playlists from Spotify to YouTube Music."""
    
    def __init__(self):
        """Initialize the playlist transfer system."""
        logger.info("Initializing Playlist Transfer System")
        
        # Initialize clients
        self.spotify_client = SpotifyClient()
        self.youtube_client = YouTubeMusicClient()
        self.track_matcher = TrackMatcher(self.youtube_client)
        
        # Transfer statistics
        self.stats = {
            'total_playlists': 0,
            'successful_transfers': 0,
            'failed_transfers': 0,
            'total_tracks': 0,
            'matched_tracks': 0,
            'failed_matches': 0,
            'transfer_start_time': None,
            'transfer_end_time': None
        }
    
    def transfer_playlist(self, spotify_playlist_id: str, 
                         youtube_playlist_name: Optional[str] = None,
                         youtube_playlist_description: Optional[str] = None,
                         privacy_status: str = 'PRIVATE') -> Dict[str, Any]:
        """Transfer a single playlist from Spotify to YouTube Music."""
        try:
            logger.info(f"Starting transfer of playlist: {spotify_playlist_id}")
            
            # Get Spotify playlist information
            playlist_info = self.spotify_client.get_playlist_info(spotify_playlist_id)
            if not playlist_info:
                raise Exception("Failed to get Spotify playlist information")
            
            logger.info(f"Transferring playlist: {playlist_info['name']} ({playlist_info['track_count']} tracks)")
            
            # Get all tracks from Spotify playlist
            spotify_tracks = self.spotify_client.get_playlist_tracks(spotify_playlist_id)
            if not spotify_tracks:
                logger.warning("No tracks found in Spotify playlist")
                return {
                    'success': True,
                    'spotify_playlist': playlist_info,
                    'youtube_playlist_id': None,
                    'matched_tracks': 0,
                    'total_tracks': 0,
                    'failed_matches': []
                }
            
            self.stats['total_tracks'] += len(spotify_tracks)
            
            # Create YouTube Music playlist first
            playlist_name = youtube_playlist_name or playlist_info['name']
            playlist_description = youtube_playlist_description or self._create_playlist_description(
                playlist_info, 0, 0  # Initial values, will be updated later
            )
            
            logger.info(f"Creating YouTube Music playlist: {playlist_name}")
            youtube_playlist_id = self.youtube_client.create_playlist(
                playlist_name, 
                playlist_description, 
                privacy_status
            )
            
            if not youtube_playlist_id:
                raise Exception("Failed to create YouTube Music playlist")
            
            logger.info(f"✅ Created YouTube Music playlist with ID: {youtube_playlist_id}")
            
            # Match and immediately add tracks to YouTube Music
            logger.info(f"Processing and adding tracks to YouTube Music... (0/{len(spotify_tracks)} processed)")
            matched_tracks = []
            failed_matches = []
            added_count = 0
            failed_additions = 0
            
            # Process tracks individually with immediate addition
            for i, track in enumerate(spotify_tracks, 1):
                # Use primary_artist, fallback to album name if artist is missing
                artist_display = track.get('primary_artist') or track.get('album', 'Unknown')
                logger.info(f"🔍 Processing track {i}/{len(spotify_tracks)}: {track.get('name', 'Unknown')} by {artist_display}")
                
                match = self.track_matcher.find_best_match(track)
                if match:
                    matched_tracks.append(match)
                    self.stats['matched_tracks'] += 1
                    logger.info(f"✅ Match found! Immediately adding to playlist...")
                    
                    # Immediately add to YouTube Music playlist
                    video_id = match.get('videoId')
                    if video_id:
                        success = self.youtube_client.add_songs_to_playlist(youtube_playlist_id, [video_id])
                        if success:
                            added_count += 1
                            logger.info(f"🎵 Successfully added to playlist! ({added_count} added, {failed_additions} failed additions, {len(failed_matches)} no matches)")
                        else:
                            failed_additions += 1
                            logger.error(f"❌ Failed to add to playlist ({added_count} added, {failed_additions} failed additions, {len(failed_matches)} no matches)")
                    else:
                        failed_additions += 1
                        logger.warning(f"⚠️  No video ID found for matched track ({added_count} added, {failed_additions} failed additions, {len(failed_matches)} no matches)")
                else:
                    failed_matches.append(track)
                    self.stats['failed_matches'] += 1
                    logger.warning(f"❌ No match found ({added_count} added, {failed_additions} failed additions, {len(failed_matches)} no matches)")
                
                # Small delay to avoid rate limiting
                time.sleep(0.3)
            
            logger.info(f"Processing completed: {len(matched_tracks)}/{len(spotify_tracks)} tracks matched, {added_count} successfully added to playlist")
            
            # Update playlist description with final statistics
            final_description = self._create_playlist_description(
                playlist_info, len(matched_tracks), len(failed_matches)
            )
            # Note: Playlist already created earlier, description will be updated if needed
            
            # Tracks have already been added immediately during matching process
            logger.info(f"Final summary: {added_count} tracks successfully added to YouTube Music playlist")
            
            # Generate transfer report
            transfer_result = {
                'success': True,
                'spotify_playlist': playlist_info,
                'youtube_playlist_id': youtube_playlist_id,
                'youtube_playlist_name': playlist_name,
                'matched_tracks': len(matched_tracks),
                'added_tracks': added_count,
                'total_tracks': len(spotify_tracks),
                'failed_matches': failed_matches,
                'failed_additions': failed_additions,
                'match_rate': len(matched_tracks) / len(spotify_tracks) if spotify_tracks else 0,
                'addition_rate': added_count / len(matched_tracks) if matched_tracks else 0
            }
            
            logger.info(
                f"Playlist transfer completed successfully! "
                f"Match rate: {transfer_result['match_rate']:.1%} "
                f"({len(matched_tracks)}/{len(spotify_tracks)} tracks)"
            )
            
            self.stats['successful_transfers'] += 1
            return transfer_result
            
        except Exception as e:
            logger.error(f"Failed to transfer playlist {spotify_playlist_id}: {e}")
            self.stats['failed_transfers'] += 1
            return {
                'success': False,
                'error': str(e),
                'spotify_playlist_id': spotify_playlist_id
            }
    
    def transfer_multiple_playlists(self, playlist_ids: List[str], 
                                   privacy_status: str = 'PRIVATE') -> List[Dict[str, Any]]:
        """Transfer multiple playlists from Spotify to YouTube Music."""
        logger.info(f"Starting transfer of {len(playlist_ids)} playlists")
        
        self.stats['total_playlists'] = len(playlist_ids)
        self.stats['transfer_start_time'] = datetime.now()
        
        results = []
        
        for i, playlist_id in enumerate(playlist_ids, 1):
            logger.info(f"\n=== Transferring playlist {i}/{len(playlist_ids)} ===")
            
            result = self.transfer_playlist(playlist_id, privacy_status=privacy_status)
            results.append(result)
            
            # Add delay between playlists to avoid rate limiting
            if i < len(playlist_ids):
                logger.info("Waiting before next playlist...")
                time.sleep(2)
        
        self.stats['transfer_end_time'] = datetime.now()
        
        # Generate summary report
        self._generate_transfer_summary(results)
        
        return results
    
    def transfer_user_playlists(self, exclude_patterns: Optional[List[str]] = None,
                               privacy_status: str = 'PRIVATE') -> List[Dict[str, Any]]:
        """Transfer all user playlists from Spotify to YouTube Music."""
        logger.info("Getting user playlists from Spotify...")
        
        # Get all user playlists
        playlists = self.spotify_client.get_user_playlists()
        
        if not playlists:
            logger.warning("No playlists found")
            return []
        
        # Filter playlists if exclude patterns are provided
        if exclude_patterns:
            filtered_playlists = []
            for playlist in playlists:
                should_exclude = False
                for pattern in exclude_patterns:
                    if pattern.lower() in playlist['name'].lower():
                        should_exclude = True
                        break
                
                if not should_exclude:
                    filtered_playlists.append(playlist)
                else:
                    logger.info(f"Excluding playlist: {playlist['name']}")
            
            playlists = filtered_playlists
        
        logger.info(f"Found {len(playlists)} playlists to transfer")
        
        # Display playlists for confirmation
        print("\nPlaylists to transfer:")
        for i, playlist in enumerate(playlists, 1):
            print(f"{i:2d}. {playlist['name']} ({playlist['track_count']} tracks)")
        
        # Extract playlist IDs
        playlist_ids = [playlist['id'] for playlist in playlists]
        
        # Transfer all playlists
        return self.transfer_multiple_playlists(playlist_ids, privacy_status)
    
    def _create_playlist_description(self, playlist_info: Dict[str, Any], 
                                   matched_tracks: int, failed_matches: int) -> str:
        """Create a description for the YouTube Music playlist."""
        description_parts = []
        
        # Original description
        if playlist_info.get('description'):
            description_parts.append(playlist_info['description'])
        
        # Transfer information
        description_parts.append(
            f"\n\nTransferred from Spotify playlist '{playlist_info['name']}' "
            f"by {playlist_info['owner']}"
        )
        
        # Match statistics
        total_tracks = matched_tracks + failed_matches
        match_rate = (matched_tracks / total_tracks * 100) if total_tracks > 0 else 0
        
        description_parts.append(
            f"Transfer completed: {matched_tracks}/{total_tracks} tracks matched ({match_rate:.1f}%)"
        )
        
        # Transfer date
        description_parts.append(f"Transferred on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return '\n'.join(description_parts)
    
    def _generate_transfer_summary(self, results: List[Dict[str, Any]]) -> None:
        """Generate and log a summary of the transfer process."""
        logger.info("\n" + "=" * 60)
        logger.info("TRANSFER SUMMARY")
        logger.info("=" * 60)
        
        # Time statistics
        if self.stats['transfer_start_time'] and self.stats['transfer_end_time']:
            duration = self.stats['transfer_end_time'] - self.stats['transfer_start_time']
            logger.info(f"Transfer duration: {duration}")
        
        # Playlist statistics
        logger.info(f"Total playlists processed: {self.stats['total_playlists']}")
        logger.info(f"Successful transfers: {self.stats['successful_transfers']}")
        logger.info(f"Failed transfers: {self.stats['failed_transfers']}")
        
        # Track statistics
        logger.info(f"Total tracks processed: {self.stats['total_tracks']}")
        logger.info(f"Successfully matched: {self.stats['matched_tracks']}")
        logger.info(f"Failed to match: {self.stats['failed_matches']}")
        
        if self.stats['total_tracks'] > 0:
            overall_match_rate = self.stats['matched_tracks'] / self.stats['total_tracks']
            logger.info(f"Overall match rate: {overall_match_rate:.1%}")
        
        # Detailed results
        logger.info("\nDetailed Results:")
        for i, result in enumerate(results, 1):
            if result['success']:
                playlist_name = result['spotify_playlist']['name']
                match_rate = result['match_rate']
                logger.info(
                    f"{i:2d}. ✓ {playlist_name} - {match_rate:.1%} match rate "
                    f"({result['matched_tracks']}/{result['total_tracks']} tracks)"
                )
            else:
                logger.error(f"{i:2d}. ✗ Failed: {result.get('error', 'Unknown error')}")
        
        # Save detailed report to file
        self._save_transfer_report(results)
        
        logger.info("=" * 60)
    
    def _save_transfer_report(self, results: List[Dict[str, Any]]) -> None:
        """Save detailed transfer report to JSON file."""
        try:
            report = {
                'transfer_date': datetime.now().isoformat(),
                'statistics': self.stats,
                'results': results
            }
            
            filename = f"transfer_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"Detailed transfer report saved to: {filename}")
            
        except Exception as e:
            logger.error(f"Failed to save transfer report: {e}")
    
    def get_transfer_statistics(self) -> Dict[str, Any]:
        """Get current transfer statistics."""
        return self.stats.copy()
    
    def transfer_to_liked_music(self, spotify_playlist_id: str) -> Dict[str, Any]:
        """Transfer a Spotify playlist to YouTube Music's liked songs."""
        try:
            logger.info(f"Starting transfer to liked music: {spotify_playlist_id}")
            
            # Get Spotify playlist information
            playlist_info = self.spotify_client.get_playlist_info(spotify_playlist_id)
            if not playlist_info:
                raise Exception("Failed to get Spotify playlist information")
            
            logger.info(f"Transferring to liked music: {playlist_info['name']} ({playlist_info['track_count']} tracks)")
            
            # Get all tracks from Spotify playlist
            spotify_tracks = self.spotify_client.get_playlist_tracks(spotify_playlist_id)
            if not spotify_tracks:
                logger.warning("No tracks found in Spotify playlist")
                return {
                    'success': True,
                    'spotify_playlist': playlist_info,
                    'liked_tracks': 0,
                    'total_tracks': 0,
                    'failed_matches': [],
                    'failed_likes': 0,
                    'match_rate': 0.0,
                    'like_rate': 0.0
                }
            
            self.stats['total_tracks'] += len(spotify_tracks)
            
            # Match and immediately like tracks on YouTube Music
            logger.info(f"Processing and liking tracks on YouTube Music... (0/{len(spotify_tracks)} processed)")
            matched_tracks = []
            failed_matches = []
            liked_count = 0
            failed_likes = 0
            
            # Process tracks individually with immediate liking
            for i, track in enumerate(spotify_tracks, 1):
                # Use primary_artist, fallback to album name if artist is missing
                artist_display = track.get('primary_artist') or track.get('album', 'Unknown')
                logger.info(f"🔍 Processing track {i}/{len(spotify_tracks)}: {track.get('name', 'Unknown')} by {artist_display}")
                
                match = self.track_matcher.find_best_match(track)
                if match:
                    matched_tracks.append(match)
                    self.stats['matched_tracks'] += 1
                    logger.info(f"✅ Match found! Immediately liking song...")
                    
                    # Immediately like the song on YouTube Music
                    video_id = match.get('videoId')
                    if video_id:
                        success = self.youtube_client.like_song(video_id)
                        if success:
                            liked_count += 1
                            logger.info(f"❤️  Successfully liked song! ({liked_count} liked, {failed_likes} failed likes, {len(failed_matches)} no matches)")
                        else:
                            failed_likes += 1
                            logger.error(f"❌ Failed to like song ({liked_count} liked, {failed_likes} failed likes, {len(failed_matches)} no matches)")
                    else:
                        failed_likes += 1
                        logger.warning(f"⚠️  No video ID found for matched track ({liked_count} liked, {failed_likes} failed likes, {len(failed_matches)} no matches)")
                else:
                    failed_matches.append(track)
                    self.stats['failed_matches'] += 1
                    logger.warning(f"⚠️  No match found ({liked_count} liked, {failed_likes} failed likes, {len(failed_matches)} no matches)")
                
                # Small delay to avoid rate limiting
                time.sleep(0.3)
            
            # Calculate rates
            match_rate = (len(matched_tracks) / len(spotify_tracks)) * 100 if spotify_tracks else 0
            like_rate = (liked_count / len(matched_tracks)) * 100 if matched_tracks else 0
            
            logger.info(f"✅ Transfer to liked music completed!")
            logger.info(f"📊 Final Summary:")
            logger.info(f"   • Total tracks: {len(spotify_tracks)}")
            logger.info(f"   • Matched: {len(matched_tracks)} ({match_rate:.1f}%)")
            logger.info(f"   • Liked: {liked_count} ({like_rate:.1f}%)")
            logger.info(f"   • Failed likes: {failed_likes}")
            logger.info(f"   • No matches: {len(failed_matches)}")
            
            return {
                'success': True,
                'spotify_playlist': playlist_info,
                'liked_tracks': liked_count,
                'total_tracks': len(spotify_tracks),
                'matched_tracks': matched_tracks,
                'failed_matches': failed_matches,
                'failed_likes': failed_likes,
                'match_rate': match_rate,
                'like_rate': like_rate
            }
            
        except Exception as e:
            logger.error(f"Failed to transfer to liked music: {e}")
            return {
                'success': False,
                'error': str(e),
                'spotify_playlist': playlist_info if 'playlist_info' in locals() else None,
                'liked_tracks': 0,
                'total_tracks': 0,
                'failed_matches': [],
                'failed_likes': 0,
                'match_rate': 0.0,
                'like_rate': 0.0
            }