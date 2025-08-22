# Usage Examples

## Command Line Interface Examples

### Basic Commands

#### Test Your Setup
```bash
# Test both Spotify and YouTube Music connections
python main.py test

# Expected output:
# 🎵 Spotify to YouTube Music Transfer Tool
# Testing Spotify connection...
# ✅ Spotify connection successful
# Testing YouTube Music connection...
# ✅ YouTube Music connection successful
# 🎉 All connections successful!
```

#### List Playlists
```bash
# List your Spotify playlists (default: 20)
python main.py list-spotify

# List with custom limit
python main.py list-spotify --limit 50

# List YouTube Music playlists
python main.py list-youtube --limit 25
```

#### Search for Tracks
```bash
# Search for a specific song
python main.py search "Bohemian Rhapsody Queen"

# Search with custom limit
python main.py search "The Beatles" --limit 15

# Search for exact matches
python main.py search "Hotel California Eagles" --limit 5
```

### Playlist Transfer Examples

#### Transfer to New Playlist
```bash
# Basic transfer (creates private playlist)
python main.py transfer 37i9dQZF1DXcBWIGoYBM5M --name "My Rock Playlist"

# Transfer with public visibility
python main.py transfer 37i9dQZF1DXcBWIGoYBM5M --name "My Public Playlist" --privacy PUBLIC

# Transfer with unlisted visibility
python main.py transfer 37i9dQZF1DXcBWIGoYBM5M --name "Shared Playlist" --privacy UNLISTED

# Transfer your liked songs to a new playlist
python main.py transfer liked_songs --name "My Spotify Likes"
```

#### Transfer to Liked Music
```bash
# Transfer any playlist to your YouTube Music liked songs
python main.py transfer-liked 37i9dQZF1DXcBWIGoYBM5M

# Transfer your Spotify liked songs to YouTube Music liked songs
python main.py transfer-liked liked_songs

# Transfer with custom matching settings
MATCH_THRESHOLD=0.7 python main.py transfer-liked 37i9dQZF1DXcBWIGoYBM5M
```

### Advanced Usage

#### Custom Configuration
```bash
# Set environment variables for one-time use
MATCH_THRESHOLD=0.6 MAX_SEARCH_RESULTS=10 python main.py transfer PLAYLIST_ID --name "Test"

# Enable debug logging
python main.py --log-level DEBUG transfer PLAYLIST_ID --name "Debug Transfer"

# Use custom retry attempts
RETRY_ATTEMPTS=5 python main.py transfer PLAYLIST_ID --name "Reliable Transfer"
```

#### Batch Operations
```bash
# Transfer multiple playlists (using shell scripting)
for playlist_id in "37i9dQZF1DXcBWIGoYBM5M" "37i9dQZF1DX0XUsuxWHRQd" "37i9dQZF1DXbTxeAdrVG2l"; do
    python main.py transfer "$playlist_id" --name "Transferred $(date +%Y%m%d)"
    sleep 30  # Wait between transfers to respect rate limits
done
```

## Python API Examples

### Basic Setup
```python
from src.spotify_youtube_transfer.config import Config
from src.spotify_youtube_transfer.playlist_transfer import PlaylistTransfer
from src.spotify_youtube_transfer.spotify_client import SpotifyClient
from src.spotify_youtube_transfer.youtube_music_client import YouTubeMusicClient

# Initialize configuration
config = Config()

# Create transfer instance
transfer = PlaylistTransfer(config)
```

### Simple Playlist Transfer
```python
def simple_transfer_example():
    """Basic playlist transfer example"""
    config = Config()
    transfer = PlaylistTransfer(config)
    
    # Transfer playlist
    result = transfer.transfer_playlist(
        spotify_playlist_id="37i9dQZF1DXcBWIGoYBM5M",
        youtube_playlist_name="My Transferred Playlist",
        privacy="PRIVATE"
    )
    
    print(f"Transfer completed!")
    print(f"Success: {result['success_count']}/{result['total_count']} tracks")
    print(f"Accuracy: {result['accuracy']:.1%}")
    
    return result

# Run the example
result = simple_transfer_example()
```

### Transfer with Progress Tracking
```python
def transfer_with_progress():
    """Transfer with real-time progress tracking"""
    config = Config()
    transfer = PlaylistTransfer(config)
    
    # Define progress callback
    def progress_callback(current, total, track_name, success):
        status = "✅" if success else "❌"
        percentage = (current / total) * 100
        print(f"[{percentage:5.1f}%] {status} {track_name} ({current}/{total})")
    
    # Set progress callback
    transfer.set_progress_callback(progress_callback)
    
    # Transfer playlist
    result = transfer.transfer_playlist(
        spotify_playlist_id="37i9dQZF1DXcBWIGoYBM5M",
        youtube_playlist_name="Progress Tracked Playlist"
    )
    
    return result

# Run with progress tracking
result = transfer_with_progress()
```

### Transfer to Liked Music
```python
def transfer_to_liked_example():
    """Transfer playlist to YouTube Music liked songs"""
    config = Config()
    transfer = PlaylistTransfer(config)
    
    # Transfer to liked music
    result = transfer.transfer_to_liked_music("37i9dQZF1DXcBWIGoYBM5M")
    
    print(f"Added {result['success_count']} songs to liked music")
    print(f"Failed to add {result['failed_count']} songs")
    
    return result

# Run the example
result = transfer_to_liked_example()
```

### Custom Configuration Example
```python
def custom_config_example():
    """Example with custom configuration"""
    # Create config with custom settings
    config = Config()
    config.match_threshold = 0.7  # Lower threshold for more matches
    config.max_search_results = 10  # More search results
    config.retry_attempts = 5  # More retry attempts
    
    transfer = PlaylistTransfer(config)
    
    # Transfer with custom settings
    result = transfer.transfer_playlist(
        spotify_playlist_id="37i9dQZF1DXcBWIGoYBM5M",
        youtube_playlist_name="Custom Config Transfer"
    )
    
    return result

# Run with custom configuration
result = custom_config_example()
```

### Error Handling Example
```python
def robust_transfer_example():
    """Transfer with comprehensive error handling"""
    from src.spotify_youtube_transfer.exceptions import (
        AuthenticationError, APIError, ConfigurationError
    )
    
    try:
        config = Config()
        transfer = PlaylistTransfer(config)
        
        result = transfer.transfer_playlist(
            spotify_playlist_id="37i9dQZF1DXcBWIGoYBM5M",
            youtube_playlist_name="Robust Transfer"
        )
        
        print(f"✅ Transfer successful: {result['success_count']} tracks")
        return result
        
    except AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("Please check your API credentials")
        
    except APIError as e:
        print(f"❌ API error: {e}")
        print("This might be a temporary issue, try again later")
        
    except ConfigurationError as e:
        print(f"❌ Configuration error: {e}")
        print("Please check your .env file")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("Please report this issue on GitHub")
        
    return None

# Run with error handling
result = robust_transfer_example()
```

### Batch Transfer Example
```python
def batch_transfer_example():
    """Transfer multiple playlists in batch"""
    import time
    
    config = Config()
    transfer = PlaylistTransfer(config)
    
    # List of playlists to transfer
    playlists = [
        {"id": "37i9dQZF1DXcBWIGoYBM5M", "name": "Rock Classics"},
        {"id": "37i9dQZF1DX0XUsuxWHRQd", "name": "Pop Hits"},
        {"id": "37i9dQZF1DXbTxeAdrVG2l", "name": "Jazz Standards"}
    ]
    
    results = []
    
    for i, playlist in enumerate(playlists, 1):
        print(f"\n[{i}/{len(playlists)}] Transferring: {playlist['name']}")
        
        try:
            result = transfer.transfer_playlist(
                spotify_playlist_id=playlist["id"],
                youtube_playlist_name=playlist["name"]
            )
            
            results.append({
                "name": playlist["name"],
                "success": True,
                "result": result
            })
            
            print(f"✅ Completed: {result['success_count']}/{result['total_count']} tracks")
            
        except Exception as e:
            print(f"❌ Failed: {e}")
            results.append({
                "name": playlist["name"],
                "success": False,
                "error": str(e)
            })
        
        # Wait between transfers to respect rate limits
        if i < len(playlists):
            print("Waiting 30 seconds before next transfer...")
            time.sleep(30)
    
    # Summary
    successful = sum(1 for r in results if r["success"])
    print(f"\n📊 Batch transfer completed: {successful}/{len(playlists)} playlists")
    
    return results

# Run batch transfer
results = batch_transfer_example()
```

### Individual Client Usage

#### Spotify Client Example
```python
def spotify_client_example():
    """Direct Spotify client usage"""
    from src.spotify_youtube_transfer.config import Config
    from src.spotify_youtube_transfer.spotify_client import SpotifyClient
    
    config = Config()
    spotify = SpotifyClient(config)
    spotify.authenticate()
    
    # Get user playlists
    playlists = spotify.get_user_playlists(limit=10)
    print(f"Found {len(playlists)} playlists:")
    
    for playlist in playlists:
        print(f"- {playlist['name']} ({playlist['track_count']} tracks)")
    
    # Get tracks from a specific playlist
    if playlists:
        playlist_id = playlists[0]['id']
        tracks = spotify.get_playlist_tracks(playlist_id)
        
        print(f"\nTracks in '{playlists[0]['name']}':")
        for track in tracks[:5]:  # Show first 5 tracks
            print(f"- {track['name']} by {track['artist']}")
    
    return playlists

# Run Spotify client example
playlists = spotify_client_example()
```

#### YouTube Music Client Example
```python
def youtube_client_example():
    """Direct YouTube Music client usage"""
    from src.spotify_youtube_transfer.config import Config
    from src.spotify_youtube_transfer.youtube_music_client import YouTubeMusicClient
    
    config = Config()
    youtube = YouTubeMusicClient(config)
    youtube.authenticate()
    
    # Search for a song
    results = youtube.search_song("Bohemian Rhapsody Queen", limit=5)
    print(f"Search results for 'Bohemian Rhapsody Queen':")
    
    for result in results:
        print(f"- {result['title']} by {result['artist']} ({result['duration']})")
    
    # Create a new playlist
    playlist_id = youtube.create_playlist(
        name="API Test Playlist",
        description="Created via API",
        privacy="PRIVATE"
    )
    
    print(f"\nCreated playlist with ID: {playlist_id}")
    
    # Add a song to the playlist
    if results:
        video_id = results[0]['videoId']
        youtube.add_song_to_playlist(playlist_id, video_id)
        print(f"Added '{results[0]['title']}' to playlist")
    
    return playlist_id

# Run YouTube Music client example
playlist_id = youtube_client_example()
```

### Track Matching Example
```python
def track_matching_example():
    """Demonstrate track matching algorithm"""
    from src.spotify_youtube_transfer.config import Config
    from src.spotify_youtube_transfer.track_matcher import TrackMatcher
    from src.spotify_youtube_transfer.youtube_music_client import YouTubeMusicClient
    
    config = Config()
    matcher = TrackMatcher(config)
    youtube = YouTubeMusicClient(config)
    youtube.authenticate()
    
    # Example Spotify track
    spotify_track = {
        'name': 'Bohemian Rhapsody',
        'artist': 'Queen',
        'duration_ms': 355000
    }
    
    # Search YouTube Music
    search_query = f"{spotify_track['name']} {spotify_track['artist']}"
    youtube_results = youtube.search_song(search_query, limit=10)
    
    # Find best match
    best_match = matcher.find_best_match(spotify_track, youtube_results)
    
    if best_match:
        print(f"✅ Found match:")
        print(f"   Spotify: {spotify_track['name']} by {spotify_track['artist']}")
        print(f"   YouTube: {best_match['title']} by {best_match['artist']}")
        print(f"   Similarity: {best_match['similarity']:.2%}")
    else:
        print(f"❌ No suitable match found")
    
    return best_match

# Run track matching example
match = track_matching_example()
```

## Real-World Scenarios

### Scenario 1: Migrating Your Entire Music Library
```python
def migrate_entire_library():
    """Migrate all playlists from Spotify to YouTube Music"""
    import time
    from datetime import datetime
    
    config = Config()
    transfer = PlaylistTransfer(config)
    spotify = SpotifyClient(config)
    spotify.authenticate()
    
    # Get all user playlists
    all_playlists = spotify.get_user_playlists(limit=50)
    
    print(f"Found {len(all_playlists)} playlists to migrate")
    
    migration_log = []
    
    for i, playlist in enumerate(all_playlists, 1):
        print(f"\n[{i}/{len(all_playlists)}] Migrating: {playlist['name']}")
        
        try:
            result = transfer.transfer_playlist(
                spotify_playlist_id=playlist['id'],
                youtube_playlist_name=f"{playlist['name']} (Migrated {datetime.now().strftime('%Y-%m-%d')})"
            )
            
            migration_log.append({
                "playlist": playlist['name'],
                "status": "success",
                "tracks_transferred": result['success_count'],
                "total_tracks": result['total_count'],
                "accuracy": result['accuracy']
            })
            
            print(f"✅ Success: {result['success_count']}/{result['total_count']} tracks")
            
        except Exception as e:
            print(f"❌ Failed: {e}")
            migration_log.append({
                "playlist": playlist['name'],
                "status": "failed",
                "error": str(e)
            })
        
        # Rate limiting
        time.sleep(60)  # Wait 1 minute between playlists
    
    # Generate migration report
    successful = sum(1 for log in migration_log if log["status"] == "success")
    total_tracks = sum(log.get("tracks_transferred", 0) for log in migration_log)
    
    print(f"\n📊 Migration Summary:")
    print(f"   Playlists: {successful}/{len(all_playlists)} successful")
    print(f"   Total tracks transferred: {total_tracks}")
    
    return migration_log

# Run full migration (use with caution!)
# migration_log = migrate_entire_library()
```

### Scenario 2: Weekly Playlist Sync
```python
def weekly_playlist_sync():
    """Sync specific playlists weekly"""
    import json
    from datetime import datetime
    
    # Configuration for weekly sync
    SYNC_PLAYLISTS = [
        {"spotify_id": "37i9dQZF1DXcBWIGoYBM5M", "youtube_name": "Weekly Rock"},
        {"spotify_id": "37i9dQZF1DX0XUsuxWHRQd", "youtube_name": "Weekly Pop"}
    ]
    
    config = Config()
    transfer = PlaylistTransfer(config)
    
    sync_results = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for playlist_config in SYNC_PLAYLISTS:
        print(f"Syncing: {playlist_config['youtube_name']}")
        
        try:
            result = transfer.transfer_playlist(
                spotify_playlist_id=playlist_config["spotify_id"],
                youtube_playlist_name=f"{playlist_config['youtube_name']} - {datetime.now().strftime('%Y-%m-%d')}"
            )
            
            sync_results.append({
                "timestamp": timestamp,
                "playlist": playlist_config["youtube_name"],
                "status": "success",
                "result": result
            })
            
        except Exception as e:
            sync_results.append({
                "timestamp": timestamp,
                "playlist": playlist_config["youtube_name"],
                "status": "failed",
                "error": str(e)
            })
    
    # Save sync log
    with open(f"sync_log_{datetime.now().strftime('%Y%m%d')}.json", "w") as f:
        json.dump(sync_results, f, indent=2)
    
    return sync_results

# Run weekly sync
# sync_results = weekly_playlist_sync()
```

### Scenario 3: Discover Weekly to Liked Music
```python
def discover_weekly_to_liked():
    """Transfer Discover Weekly to YouTube Music liked songs"""
    config = Config()
    transfer = PlaylistTransfer(config)
    spotify = SpotifyClient(config)
    spotify.authenticate()
    
    # Find Discover Weekly playlist
    playlists = spotify.get_user_playlists(limit=50)
    discover_weekly = None
    
    for playlist in playlists:
        if "Discover Weekly" in playlist['name']:
            discover_weekly = playlist
            break
    
    if not discover_weekly:
        print("❌ Discover Weekly playlist not found")
        return None
    
    print(f"Found Discover Weekly: {discover_weekly['name']}")
    
    # Transfer to liked music
    result = transfer.transfer_to_liked_music(discover_weekly['id'])
    
    print(f"✅ Added {result['success_count']} new discoveries to liked music")
    
    return result

# Run Discover Weekly transfer
# result = discover_weekly_to_liked()
```

These examples demonstrate various ways to use the Spotify to YouTube Music Transfer Tool, from simple command-line operations to complex Python integrations. Choose the approach that best fits your needs and technical comfort level.