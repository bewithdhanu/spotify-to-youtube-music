# API Documentation

## Overview

The Spotify to YouTube Music Transfer Tool provides a comprehensive API for transferring playlists between Spotify and YouTube Music. The core functionality is organized into several modules within the `src/spotify_youtube_transfer` package.

## Core Modules

### Config (`src/spotify_youtube_transfer/config.py`)

Manages application configuration and environment variables.

#### Class: `Config`

```python
from src.spotify_youtube_transfer.config import Config

config = Config()
```

**Properties:**
- `spotify_client_id`: Spotify API client ID
- `spotify_client_secret`: Spotify API client secret
- `match_threshold`: Minimum similarity score for track matching (0.0-1.0)
- `max_search_results`: Maximum number of search results to consider
- `retry_attempts`: Number of retry attempts for failed operations

**Methods:**
- `validate()`: Validates configuration settings
- `get_spotify_credentials()`: Returns Spotify API credentials
- `get_matching_config()`: Returns track matching configuration

### Spotify Client (`src/spotify_youtube_transfer/spotify_client.py`)

Handles all Spotify API interactions.

#### Class: `SpotifyClient`

```python
from src.spotify_youtube_transfer.spotify_client import SpotifyClient

client = SpotifyClient(config)
```

**Methods:**
- `authenticate()`: Authenticates with Spotify API
- `get_user_playlists(limit=50)`: Retrieves user's playlists
- `get_playlist_tracks(playlist_id)`: Gets tracks from a specific playlist
- `get_liked_songs()`: Retrieves user's liked songs
- `search_track(query, limit=10)`: Searches for tracks
- `get_track_details(track_id)`: Gets detailed track information

**Example Usage:**
```python
from src.spotify_youtube_transfer.config import Config
from src.spotify_youtube_transfer.spotify_client import SpotifyClient

config = Config()
client = SpotifyClient(config)
client.authenticate()

# Get user playlists
playlists = client.get_user_playlists(limit=25)

# Get tracks from a playlist
tracks = client.get_playlist_tracks('playlist_id_here')
```

### YouTube Music Client (`src/spotify_youtube_transfer/youtube_music_client.py`)

Handles YouTube Music API interactions.

#### Class: `YouTubeMusicClient`

```python
from src.spotify_youtube_transfer.youtube_music_client import YouTubeMusicClient

client = YouTubeMusicClient(config)
```

**Methods:**
- `authenticate()`: Authenticates with YouTube Music
- `search_song(query, limit=5)`: Searches for songs
- `create_playlist(name, description="", privacy="PRIVATE")`: Creates a new playlist
- `add_song_to_playlist(playlist_id, video_id)`: Adds a song to playlist
- `add_to_liked_music(video_id)`: Adds a song to liked music
- `get_playlists()`: Retrieves user's playlists
- `get_liked_songs()`: Gets liked songs

**Privacy Options:**
- `PRIVATE`: Only visible to you
- `PUBLIC`: Visible to everyone
- `UNLISTED`: Accessible via link only

### Track Matcher (`src/spotify_youtube_transfer/track_matcher.py`)

Provides intelligent track matching between platforms.

#### Class: `TrackMatcher`

```python
from src.spotify_youtube_transfer.track_matcher import TrackMatcher

matcher = TrackMatcher(config)
```

**Methods:**
- `find_best_match(spotify_track, youtube_results)`: Finds the best YouTube Music match
- `calculate_similarity(track1, track2)`: Calculates similarity score
- `generate_search_queries(track)`: Generates multiple search queries
- `normalize_string(text)`: Normalizes text for comparison

**Matching Algorithm:**
1. **Query Generation**: Creates multiple search variations
2. **Fuzzy Matching**: Uses string similarity algorithms
3. **Multi-factor Scoring**: Considers title, artist, and duration
4. **Threshold Filtering**: Only accepts matches above threshold

### Playlist Transfer (`src/spotify_youtube_transfer/playlist_transfer.py`)

Orchestrates the complete transfer process.

#### Class: `PlaylistTransfer`

```python
from src.spotify_youtube_transfer.playlist_transfer import PlaylistTransfer

transfer = PlaylistTransfer(config)
```

**Methods:**
- `transfer_playlist(spotify_playlist_id, youtube_playlist_name, privacy="PRIVATE")`: Transfers to new playlist
- `transfer_to_liked_music(spotify_playlist_id)`: Transfers to liked music
- `get_transfer_report()`: Returns detailed transfer statistics
- `set_progress_callback(callback)`: Sets progress tracking callback

**Transfer Statistics:**
- Total tracks processed
- Successful matches
- Failed matches
- Match accuracy percentage
- Processing time

## Usage Examples

### Basic Playlist Transfer

```python
from src.spotify_youtube_transfer.config import Config
from src.spotify_youtube_transfer.playlist_transfer import PlaylistTransfer

# Initialize
config = Config()
transfer = PlaylistTransfer(config)

# Transfer playlist
result = transfer.transfer_playlist(
    spotify_playlist_id="37i9dQZF1DXcBWIGoYBM5M",
    youtube_playlist_name="My Transferred Playlist",
    privacy="PRIVATE"
)

print(f"Transfer completed: {result['success_count']}/{result['total_count']} tracks")
```

### Transfer to Liked Music

```python
# Transfer to YouTube Music liked songs
result = transfer.transfer_to_liked_music("37i9dQZF1DXcBWIGoYBM5M")
print(f"Added {result['success_count']} songs to liked music")
```

### Progress Tracking

```python
def progress_callback(current, total, track_name, success):
    status = "✓" if success else "✗"
    print(f"[{current}/{total}] {status} {track_name}")

transfer.set_progress_callback(progress_callback)
result = transfer.transfer_playlist(playlist_id, "My Playlist")
```

### Custom Configuration

```python
from src.spotify_youtube_transfer.config import Config

# Create config with custom settings
config = Config()
config.match_threshold = 0.7  # Lower threshold for more matches
config.max_search_results = 10  # More search results
config.retry_attempts = 5  # More retry attempts

transfer = PlaylistTransfer(config)
```

## Error Handling

All methods may raise the following exceptions:

- `AuthenticationError`: Authentication failed
- `APIError`: API request failed
- `ConfigurationError`: Invalid configuration
- `NetworkError`: Network connectivity issues
- `RateLimitError`: API rate limit exceeded

```python
from src.spotify_youtube_transfer.exceptions import AuthenticationError, APIError

try:
    result = transfer.transfer_playlist(playlist_id, "My Playlist")
except AuthenticationError:
    print("Authentication failed. Check your credentials.")
except APIError as e:
    print(f"API error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Rate Limiting

The tool includes built-in rate limiting to respect API limits:

- Spotify: 100 requests per minute
- YouTube Music: Adaptive rate limiting based on response times
- Automatic retry with exponential backoff

## Best Practices

1. **Authentication**: Always authenticate before making API calls
2. **Error Handling**: Implement proper error handling for production use
3. **Progress Tracking**: Use progress callbacks for long-running operations
4. **Configuration**: Validate configuration before starting transfers
5. **Rate Limits**: Be mindful of API rate limits for large transfers
6. **Logging**: Enable logging for debugging and monitoring

## Logging

Enable detailed logging for debugging:

```python
import logging
from loguru import logger

# Enable debug logging
logger.add("transfer.log", level="DEBUG")

# Or use Python's logging
logging.basicConfig(level=logging.DEBUG)
```