#!/usr/bin/env python3
"""
Example usage of the Spotify to YouTube Music Transfer Tool

This script demonstrates how to use the tool programmatically
for advanced automation and custom workflows.
"""

import os
from loguru import logger
from .config import Config
from .playlist_transfer import PlaylistTransfer
from .spotify_client import SpotifyClient
from .youtube_music_client import YouTubeMusicClient

def example_single_playlist_transfer():
    """Example: Transfer a single playlist."""
    print("\n=== Single Playlist Transfer Example ===")
    
    # Initialize the transfer system
    transfer = PlaylistTransfer()
    
    # Replace with your actual playlist ID
    playlist_id = "37i9dQZF1DXcBWIGoYBM5M"  # Example: Today's Top Hits
    
    try:
        # Transfer the playlist
        result = transfer.transfer_playlist(
            spotify_playlist_id=playlist_id,
            youtube_playlist_name="My Transferred Playlist",
            youtube_playlist_description="Transferred from Spotify using automation tool",
            privacy_status="PRIVATE"
        )
        
        if result['success']:
            print(f"✅ Successfully transferred: {result['spotify_playlist']['name']}")
            print(f"   Match rate: {result['match_rate']:.1%}")
            print(f"   YouTube Playlist ID: {result['youtube_playlist_id']}")
        else:
            print(f"❌ Transfer failed: {result['error']}")
            
    except Exception as e:
        logger.error(f"Transfer failed: {e}")

def example_batch_transfer_with_filters():
    """Example: Transfer multiple playlists with custom filters."""
    print("\n=== Batch Transfer with Filters Example ===")
    
    # Initialize clients
    spotify_client = SpotifyClient()
    transfer = PlaylistTransfer()
    
    try:
        # Get all user playlists
        playlists = spotify_client.get_user_playlists()
        
        # Custom filtering logic
        filtered_playlists = []
        for playlist in playlists:
            # Only transfer playlists with more than 10 tracks
            if playlist['track_count'] > 10:
                # Skip auto-generated playlists
                if not any(skip in playlist['name'].lower() for skip in 
                          ['discover weekly', 'release radar', 'daily mix']):
                    filtered_playlists.append(playlist)
        
        print(f"Found {len(filtered_playlists)} playlists to transfer")
        
        # Transfer filtered playlists
        playlist_ids = [p['id'] for p in filtered_playlists]
        results = transfer.transfer_multiple_playlists(playlist_ids, privacy_status="PRIVATE")
        
        # Print summary
        successful = sum(1 for r in results if r['success'])
        print(f"\n✅ Successfully transferred {successful}/{len(results)} playlists")
        
    except Exception as e:
        logger.error(f"Batch transfer failed: {e}")

def example_custom_matching():
    """Example: Custom track matching with different thresholds."""
    print("\n=== Custom Track Matching Example ===")
    
    # Initialize clients
    spotify_client = SpotifyClient()
    youtube_client = YouTubeMusicClient()
    
    try:
        # Get a sample playlist
        playlists = spotify_client.get_user_playlists()
        if not playlists:
            print("No playlists found")
            return
        
        sample_playlist = playlists[0]
        tracks = spotify_client.get_playlist_tracks(sample_playlist['id'])
        
        if not tracks:
            print("No tracks found in playlist")
            return
        
        # Take first 5 tracks for demonstration
        sample_tracks = tracks[:5]
        
        print(f"Testing matching for {len(sample_tracks)} tracks from '{sample_playlist['name']}'")
        
        # Test different matching thresholds
        from track_matcher import TrackMatcher
        
        thresholds = [0.6, 0.7, 0.8, 0.9]
        
        for threshold in thresholds:
            print(f"\n--- Testing with threshold {threshold} ---")
            
            # Create matcher with custom threshold
            matcher = TrackMatcher(youtube_client)
            matcher.match_threshold = threshold
            
            matches = 0
            for track in sample_tracks:
                match = matcher.find_best_match(track)
                if match:
                    matches += 1
                    print(f"✅ {track['name']} -> {match['title']} (score: {match['match_score']:.2f})")
                else:
                    print(f"❌ {track['name']} -> No match found")
            
            print(f"Match rate with threshold {threshold}: {matches}/{len(sample_tracks)} ({matches/len(sample_tracks):.1%})")
            
    except Exception as e:
        logger.error(f"Custom matching test failed: {e}")

def example_search_comparison():
    """Example: Compare search results between platforms."""
    print("\n=== Search Comparison Example ===")
    
    # Initialize clients
    spotify_client = SpotifyClient()
    youtube_client = YouTubeMusicClient()
    
    # Test queries
    test_queries = [
        "Bohemian Rhapsody Queen",
        "Billie Jean Michael Jackson",
        "Hotel California Eagles",
        "Imagine Dragons Radioactive",
        "Taylor Swift Shake It Off"
    ]
    
    try:
        for query in test_queries:
            print(f"\n--- Searching for: {query} ---")
            
            # Search Spotify
            spotify_results = spotify_client.search_track(query, limit=3)
            print("Spotify results:")
            for i, track in enumerate(spotify_results, 1):
                print(f"  {i}. {track['name']} by {track['primary_artist']}")
            
            # Search YouTube Music
            youtube_results = youtube_client.search_song(query, limit=3)
            print("YouTube Music results:")
            for i, track in enumerate(youtube_results, 1):
                print(f"  {i}. {track['title']} by {track['primary_artist']}")
                
    except Exception as e:
        logger.error(f"Search comparison failed: {e}")

def example_playlist_analysis():
    """Example: Analyze playlist characteristics before transfer."""
    print("\n=== Playlist Analysis Example ===")
    
    # Initialize client
    spotify_client = SpotifyClient()
    
    try:
        # Get all playlists
        playlists = spotify_client.get_user_playlists()
        
        if not playlists:
            print("No playlists found")
            return
        
        print(f"Analyzing {len(playlists)} playlists...")
        
        # Analyze playlist characteristics
        total_tracks = sum(p['track_count'] for p in playlists)
        avg_tracks = total_tracks / len(playlists) if playlists else 0
        
        # Find largest and smallest playlists
        largest = max(playlists, key=lambda p: p['track_count'])
        smallest = min(playlists, key=lambda p: p['track_count'])
        
        print(f"\nPlaylist Statistics:")
        print(f"  Total playlists: {len(playlists)}")
        print(f"  Total tracks: {total_tracks}")
        print(f"  Average tracks per playlist: {avg_tracks:.1f}")
        print(f"  Largest playlist: '{largest['name']}' ({largest['track_count']} tracks)")
        print(f"  Smallest playlist: '{smallest['name']}' ({smallest['track_count']} tracks)")
        
        # Categorize playlists by size
        small = sum(1 for p in playlists if p['track_count'] < 20)
        medium = sum(1 for p in playlists if 20 <= p['track_count'] < 100)
        large = sum(1 for p in playlists if p['track_count'] >= 100)
        
        print(f"\nPlaylist Size Distribution:")
        print(f"  Small (<20 tracks): {small}")
        print(f"  Medium (20-99 tracks): {medium}")
        print(f"  Large (100+ tracks): {large}")
        
        # Estimate transfer time (rough calculation)
        # Assuming ~2 seconds per track for matching and transfer
        estimated_time = total_tracks * 2 / 60  # minutes
        print(f"\nEstimated transfer time: {estimated_time:.1f} minutes")
        
    except Exception as e:
        logger.error(f"Playlist analysis failed: {e}")

def main():
    """Run all examples."""
    print("🎵 Spotify to YouTube Music Transfer Tool - Usage Examples")
    print("=" * 60)
    
    # Check if configuration is valid
    validation = Config.validate_config()
    if not validation['valid']:
        print("❌ Configuration is not valid. Please run setup first.")
        print("Errors:")
        for error in validation['errors']:
            print(f"  - {error}")
        return
    
    print("✅ Configuration is valid")
    
    # Run examples (comment out the ones you don't want to run)
    try:
        # example_single_playlist_transfer()  # Uncomment to test
        # example_batch_transfer_with_filters()  # Uncomment to test
        # example_custom_matching()  # Uncomment to test
        example_search_comparison()
        example_playlist_analysis()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Examples interrupted by user")
    except Exception as e:
        logger.error(f"Examples failed: {e}")
    
    print("\n" + "=" * 60)
    print("Examples completed! Check the code for more details.")
    print("=" * 60)

if __name__ == '__main__':
    main()