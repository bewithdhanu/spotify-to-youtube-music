#!/usr/bin/env python3
"""
Spotify to YouTube Music Integration Tool

Core functionality for connecting to both platforms, managing playlists,
searching songs, and transferring content between services.
"""

import sys
from typing import List, Dict, Any, Optional
from loguru import logger

from src.spotify_youtube_transfer.config import Config
from src.spotify_youtube_transfer.spotify_client import SpotifyClient
from src.spotify_youtube_transfer.youtube_music_client import YouTubeMusicClient
from src.spotify_youtube_transfer.playlist_transfer import PlaylistTransfer

# Configure logging
logger.remove()
logger.add(sys.stderr, level="INFO", format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}")

class SpotifyYouTubeMusicTool:
    """Main class for Spotify to YouTube Music integration."""
    
    def __init__(self):
        self.config = Config()
        self.spotify_client = None
        self.youtube_client = None
        self.transfer_tool = None
    
    def connect_spotify(self) -> bool:
        """Connect to Spotify API."""
        try:
            self.spotify_client = SpotifyClient()
            logger.info("✅ Successfully connected to Spotify")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to connect to Spotify: {e}")
            return False
    
    def connect_youtube_music(self) -> bool:
        """Connect to YouTube Music API."""
        try:
            self.youtube_client = YouTubeMusicClient()
            logger.info("✅ Successfully connected to YouTube Music")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to connect to YouTube Music: {e}")
            return False
    
    def test_connections(self) -> Dict[str, bool]:
        """Test connections to both platforms."""
        logger.info("🔍 Testing platform connections...")
        
        results = {
            'spotify': self.connect_spotify(),
            'youtube_music': self.connect_youtube_music()
        }
        
        if all(results.values()):
            logger.info("✅ All connections successful!")
            # Initialize transfer tool if both connections work
            self.transfer_tool = PlaylistTransfer()
        else:
            logger.warning("⚠️ Some connections failed")
        
        return results
    
    def list_spotify_playlists(self, limit: int = 50) -> List[Dict[str, Any]]:
        """List user's Spotify playlists."""
        if not self.spotify_client:
            if not self.connect_spotify():
                return []
        
        try:
            playlists = self.spotify_client.get_user_playlists(limit=limit)
            logger.info(f"📋 Found {len(playlists)} Spotify playlists")
            
            for playlist in playlists:
                print(f"🎵 {playlist['name']} - {playlist['track_count']} tracks (ID: {playlist['id']})")
            
            return playlists
        except Exception as e:
            logger.error(f"❌ Failed to list Spotify playlists: {e}")
            return []
    
    def list_youtube_music_playlists(self, limit: int = 25) -> List[Dict[str, Any]]:
        """List user's YouTube Music playlists."""
        if not self.youtube_client:
            if not self.connect_youtube_music():
                return []
        
        try:
            playlists = self.youtube_client.get_library_playlists(limit=limit)
            logger.info(f"📋 Found {len(playlists)} YouTube Music playlists")
            
            for playlist in playlists:
                print(f"🎵 {playlist['title']} - {playlist['actual_count']} songs (ID: {playlist['playlistId']})")
            
            return playlists
        except Exception as e:
            logger.error(f"❌ Failed to list YouTube Music playlists: {e}")
            return []
    
    def search_spotify_song(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for songs on Spotify."""
        if not self.spotify_client:
            if not self.connect_spotify():
                return []
        
        try:
            results = self.spotify_client.search_track(query, limit=limit)
            logger.info(f"🔍 Found {len(results)} Spotify results for '{query}'")
            
            for i, track in enumerate(results, 1):
                artists = ', '.join(track['artists'])
                print(f"{i}. {track['name']} by {artists} ({track['album']})")
            
            return results
        except Exception as e:
            logger.error(f"❌ Failed to search Spotify: {e}")
            return []
    
    def search_youtube_music_song(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for songs on YouTube Music."""
        if not self.youtube_client:
            if not self.connect_youtube_music():
                return []
        
        try:
            results = self.youtube_client.search_song(query, limit=limit)
            logger.info(f"🔍 Found {len(results)} YouTube Music results for '{query}'")
            
            for i, track in enumerate(results, 1):
                artists = ', '.join(track['artists'])
                print(f"{i}. {track['title']} by {artists} ({track['album']})")
            
            return results
        except Exception as e:
            logger.error(f"❌ Failed to search YouTube Music: {e}")
            return []
    
    def initiate_transfer(self, spotify_playlist_id: str, 
                         youtube_playlist_name: Optional[str] = None,
                         privacy: str = 'PRIVATE') -> bool:
        """Initiate transfer of a Spotify playlist to YouTube Music."""
        if not self.transfer_tool:
            logger.error("❌ Transfer tool not initialized. Run test_connections() first.")
            return False
        
        try:
            logger.info(f"🚀 Starting transfer of playlist {spotify_playlist_id}")
            
            result = self.transfer_tool.transfer_playlist(
                spotify_playlist_id=spotify_playlist_id,
                youtube_playlist_name=youtube_playlist_name,
                privacy_status=privacy
            )
            
            if result['success']:
                logger.info(f"✅ Transfer completed successfully!")
                logger.info(f"📋 YouTube Music playlist: {result['youtube_playlist_name']}")
                logger.info(f"📊 Matched: {result['matched_tracks']}/{result['total_tracks']} tracks ({result['match_rate']:.1%})")
                logger.info(f"📊 Added to playlist: {result['added_tracks']}/{result['matched_tracks']} tracks ({result['addition_rate']:.1%})")
                return True
            else:
                logger.error(f"❌ Transfer failed: {result.get('error', 'Unknown error')}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Transfer failed with exception: {e}")
            return False
    
    def initiate_transfer_to_liked_music(self, spotify_playlist_id: str) -> bool:
        """Initiate transfer of a Spotify playlist to YouTube Music's liked songs."""
        if not self.transfer_tool:
            logger.error("❌ Transfer tool not initialized. Run test_connections() first.")
            return False
        
        try:
            logger.info(f"🚀 Starting transfer to liked music: {spotify_playlist_id}")
            
            result = self.transfer_tool.transfer_to_liked_music(
                spotify_playlist_id=spotify_playlist_id
            )
            
            if result['success']:
                logger.info(f"✅ Transfer to liked music completed successfully!")
                logger.info(f"📋 Spotify playlist: {result['spotify_playlist']['name']}")
                logger.info(f"📊 Matched: {result['total_tracks'] - len(result['failed_matches'])}/{result['total_tracks']} tracks ({result['match_rate']:.1f}%)")
                logger.info(f"❤️  Liked: {result['liked_tracks']}/{result['total_tracks'] - len(result['failed_matches'])} tracks ({result['like_rate']:.1f}%)")
                return True
            else:
                logger.error(f"❌ Transfer to liked music failed: {result.get('error', 'Unknown error')}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Transfer to liked music failed with exception: {e}")
            return False


def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="🎵 Spotify to YouTube Music Integration Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python main.py test                           # Test connections
  python main.py list-spotify                   # List Spotify playlists
  python main.py list-youtube                   # List YouTube Music playlists
  python main.py search "Bohemian Rhapsody"      # Search for a song
  python main.py transfer PLAYLIST_ID           # Transfer a playlist
  python main.py demo                           # Run full demo
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Test connections to both platforms')
    
    # List commands
    list_spotify_parser = subparsers.add_parser('list-spotify', help='List Spotify playlists')
    list_spotify_parser.add_argument('--limit', type=int, default=50, help='Number of playlists to show')
    
    list_youtube_parser = subparsers.add_parser('list-youtube', help='List YouTube Music playlists')
    list_youtube_parser.add_argument('--limit', type=int, default=25, help='Number of playlists to show')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for songs on both platforms')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--limit', type=int, default=10, help='Number of results to show')
    
    # Transfer command
    transfer_parser = subparsers.add_parser('transfer', help='Transfer a Spotify playlist to YouTube Music')
    transfer_parser.add_argument('playlist_id', help='Spotify playlist ID')
    transfer_parser.add_argument('--name', help='Custom name for YouTube Music playlist')
    transfer_parser.add_argument('--privacy', choices=['PRIVATE', 'PUBLIC', 'UNLISTED'], 
                               default='PRIVATE', help='Privacy setting for YouTube Music playlist')
    
    # Transfer to liked music command
    transfer_liked_parser = subparsers.add_parser('transfer-liked', help='Transfer a Spotify playlist to YouTube Music liked songs')
    transfer_liked_parser.add_argument('playlist_id', help='Spotify playlist ID')
    
    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Run full demonstration of all features')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    tool = SpotifyYouTubeMusicTool()
    
    if args.command == 'test':
        print("🔍 Testing platform connections...")
        connections = tool.test_connections()
        if all(connections.values()):
            print("✅ All connections successful!")
        else:
            print("❌ Some connections failed. Check your configuration.")
            
    elif args.command == 'list-spotify':
        print(f"📋 Listing Spotify playlists (limit: {args.limit})...")
        tool.list_spotify_playlists(limit=args.limit)
        
    elif args.command == 'list-youtube':
        print(f"📋 Listing YouTube Music playlists (limit: {args.limit})...")
        tool.list_youtube_music_playlists(limit=args.limit)
        
    elif args.command == 'search':
        print(f"🔍 Searching for '{args.query}' on both platforms...")
        print("\nSpotify Results:")
        tool.search_spotify_song(args.query, limit=args.limit)
        print("\nYouTube Music Results:")
        tool.search_youtube_music_song(args.query, limit=args.limit)
        
    elif args.command == 'transfer':
        print(f"🚀 Transferring playlist {args.playlist_id}...")
        
        # First test connections to initialize transfer tool
        print("🔍 Testing platform connections...")
        connections = tool.test_connections()
        if not all(connections.values()):
            print("❌ Connection test failed. Please check your configuration.")
            return
        
        success = tool.initiate_transfer(
            spotify_playlist_id=args.playlist_id,
            youtube_playlist_name=args.name,
            privacy=args.privacy
        )
        if success:
            print("✅ Transfer completed successfully!")
        else:
            print("❌ Transfer failed. Check logs for details.")
            
    elif args.command == 'transfer-liked':
        print(f"❤️  Transferring playlist {args.playlist_id} to liked music...")
        
        # First test connections to initialize transfer tool
        print("🔍 Testing platform connections...")
        connections = tool.test_connections()
        if not all(connections.values()):
            print("❌ Connection test failed. Please check your configuration.")
            return
        
        success = tool.initiate_transfer_to_liked_music(
            spotify_playlist_id=args.playlist_id
        )
        if success:
            print("✅ Transfer to liked music completed successfully!")
        else:
            print("❌ Transfer to liked music failed. Check logs for details.")
            
    elif args.command == 'demo':
        print("🎵 Spotify to YouTube Music Integration Tool")
        print("=" * 50)
        
        # Test connections
        print("\n1. Testing connections...")
        connections = tool.test_connections()
        
        if not all(connections.values()):
            print("❌ Connection test failed. Please check your configuration.")
            return
        
        # List playlists from both platforms
        print("\n2. Spotify Playlists:")
        tool.list_spotify_playlists(limit=5)
        
        print("\n3. YouTube Music Playlists:")
        tool.list_youtube_music_playlists(limit=5)
        
        # Example search
        print("\n4. Example Search - 'Bohemian Rhapsody':")
        print("\nSpotify Results:")
        tool.search_spotify_song("Bohemian Rhapsody", limit=3)
        
        print("\nYouTube Music Results:")
        tool.search_youtube_music_song("Bohemian Rhapsody", limit=3)
        
        print("\n✅ All core functions tested successfully!")
        print("\n💡 To transfer a playlist, use:")
        print("   python main.py transfer SPOTIFY_PLAYLIST_ID --name 'New Playlist Name'")
        print("\n💡 To transfer to your liked music, use:")
        print("   python main.py transfer-liked SPOTIFY_PLAYLIST_ID")


if __name__ == "__main__":
    main()