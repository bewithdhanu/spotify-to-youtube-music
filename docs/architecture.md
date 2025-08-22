# Project Architecture

## Overview

The Spotify to YouTube Music Transfer Tool follows a modular, object-oriented architecture designed for maintainability, extensibility, and separation of concerns. The project has been restructured to follow Python packaging best practices.

## Directory Structure

```
Spotify-to-Youtube/
├── main.py                     # CLI entry point
├── setup.py                    # Package setup and installation script
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── LICENSE                    # MIT license
├── README.md                  # Project documentation
│
├── src/                       # Source code package
│   └── spotify_youtube_transfer/
│       ├── __init__.py        # Package initialization
│       ├── config.py          # Configuration management
│       ├── spotify_client.py  # Spotify API client
│       ├── youtube_music_client.py # YouTube Music API client
│       ├── track_matcher.py   # Track matching algorithm
│       ├── playlist_transfer.py # Main transfer orchestration
│       └── example_usage.py   # Usage examples
│
├── docs/                      # Documentation
│   ├── api.md                # API documentation
│   ├── installation.md       # Installation guide
│   ├── troubleshooting.md     # Troubleshooting guide
│   ├── usage-examples.md      # Usage examples
│   └── architecture.md        # This file
│
└── Generated Files (runtime)
    ├── oauth.json             # YouTube Music OAuth2 token
    ├── .spotify_cache         # Spotify authentication cache
    ├── transfer_report_*.json # Transfer reports
    ├── spotify_to_youtube.log # Application logs
    └── .spotify_cache         # Spotify authentication cache
```

## Architecture Principles

### 1. Separation of Concerns
Each module has a single, well-defined responsibility:
- **Config**: Environment and configuration management
- **Clients**: API interactions (Spotify, YouTube Music)
- **Matcher**: Track matching logic
- **Transfer**: Orchestration and workflow management
- **CLI**: User interface and command handling

### 2. Dependency Injection
Configuration is injected into all components, making the system:
- Testable (easy to mock dependencies)
- Configurable (runtime behavior modification)
- Maintainable (loose coupling between components)

### 3. Error Handling
Robust error handling at multiple levels:
- Network errors with retry mechanisms
- API rate limiting with exponential backoff
- Authentication failures with clear user guidance
- Configuration validation with helpful error messages

### 4. Extensibility
Modular design allows for easy extension:
- New music services can be added by implementing client interfaces
- Different matching algorithms can be plugged in
- Additional transfer modes can be implemented

## Core Components

### Configuration Layer (`config.py`)

```python
class Config:
    """Centralized configuration management"""
    
    def __init__(self):
        self.load_environment()
        self.validate()
    
    def load_environment(self):
        """Load settings from environment variables"""
    
    def validate(self):
        """Validate configuration completeness and correctness"""
```

**Responsibilities:**
- Environment variable loading and parsing
- Configuration validation
- Default value management
- Type conversion and validation

**Design Decisions:**
- Uses environment variables for security (no hardcoded secrets)
- Validates configuration at startup to fail fast
- Provides sensible defaults for optional settings

### API Client Layer

#### Spotify Client (`spotify_client.py`)

```python
class SpotifyClient:
    """Spotify Web API client with authentication and rate limiting"""
    
    def __init__(self, config: Config):
        self.config = config
        self.sp = None
    
    def authenticate(self):
        """Handle OAuth2 authentication flow"""
    
    def get_user_playlists(self, limit: int = 50):
        """Retrieve user's playlists with pagination"""
    
    def get_playlist_tracks(self, playlist_id: str):
        """Get all tracks from a playlist with pagination"""
```

**Key Features:**
- OAuth2 authentication with token caching
- Automatic pagination handling
- Rate limiting compliance
- Comprehensive error handling
- Progress tracking for large operations

#### YouTube Music Client (`youtube_music_client.py`)

```python
class YouTubeMusicClient:
    """YouTube Music API client with multiple authentication methods"""
    
    def __init__(self, config: Config):
        self.config = config
        self.ytmusic = None
    
    def authenticate(self):
        """Handle OAuth2 or header-based authentication"""
    
    def search_song(self, query: str, limit: int = 5):
        """Search for songs with intelligent query processing"""
    
    def create_playlist(self, name: str, privacy: str = "PRIVATE"):
        """Create new playlist with privacy controls"""
```

**Key Features:**
- OAuth2 authentication for secure API access
- Intelligent search query generation
- Playlist privacy management
- Liked music integration
- Robust error handling for API inconsistencies

### Business Logic Layer

#### Track Matcher (`track_matcher.py`)

```python
class TrackMatcher:
    """Intelligent track matching between Spotify and YouTube Music"""
    
    def __init__(self, config: Config):
        self.config = config
    
    def find_best_match(self, spotify_track: dict, youtube_results: list):
        """Find the best YouTube Music match for a Spotify track"""
    
    def calculate_similarity(self, track1: dict, track2: dict) -> float:
        """Calculate similarity score between two tracks"""
```

**Matching Algorithm:**
1. **Query Generation**: Creates multiple search variations
   - Artist + Track name
   - Track name only
   - Cleaned versions (removing special characters)
   - Alternative artist names

2. **Fuzzy String Matching**: Uses multiple algorithms
   - Levenshtein distance
   - Token sort ratio
   - Token set ratio
   - Partial ratio matching

3. **Multi-factor Scoring**:
   - Title similarity (40% weight)
   - Artist similarity (35% weight)
   - Duration similarity (25% weight)

4. **Threshold Filtering**: Configurable minimum similarity score

#### Playlist Transfer (`playlist_transfer.py`)

```python
class PlaylistTransfer:
    """Orchestrates the complete transfer process"""
    
    def __init__(self, config: Config):
        self.config = config
        self.spotify_client = SpotifyClient(config)
        self.youtube_client = YouTubeMusicClient(config)
        self.track_matcher = TrackMatcher(config)
    
    def transfer_playlist(self, spotify_playlist_id: str, youtube_playlist_name: str):
        """Transfer a Spotify playlist to YouTube Music"""
    
    def transfer_to_liked_music(self, spotify_playlist_id: str):
        """Transfer tracks to YouTube Music liked songs"""
```

**Transfer Workflow:**
1. **Authentication**: Verify connections to both services
2. **Playlist Retrieval**: Fetch Spotify playlist metadata and tracks
3. **Track Processing**: Process each track individually
   - Search YouTube Music for matches
   - Apply matching algorithm
   - Add successful matches to target playlist/liked music
   - Log failures for manual review
4. **Progress Reporting**: Real-time progress updates
5. **Report Generation**: Detailed transfer statistics

### Presentation Layer

#### Command Line Interface (`main.py`)

```python
def main():
    """Main CLI entry point with command routing"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Route to appropriate handler
    if args.command == 'test':
        test_connections()
    elif args.command == 'transfer':
        transfer_playlist(args)
    # ... other commands
```

**CLI Features:**
- Intuitive command structure
- Comprehensive help system
- Progress bars and status indicators
- Colored output for better UX
- Error handling with user-friendly messages

## Data Flow

### Authentication Flow
```
1. Config loads environment variables
2. Spotify Client authenticates via OAuth2
3. YouTube Music Client authenticates using OAuth2
4. Connections tested and verified
```

### Transfer Flow
```
1. User initiates transfer via CLI
2. PlaylistTransfer orchestrates the process:
   a. Fetch Spotify playlist tracks
   b. For each track:
      - Search YouTube Music
      - Find best match using TrackMatcher
      - Add to YouTube Music playlist/liked music
      - Update progress
   c. Generate transfer report
3. Display results to user
```

### Error Handling Flow
```
1. Error occurs at any level
2. Component-specific error handling:
   - Network errors: Retry with exponential backoff
   - Rate limits: Wait and retry
   - Authentication: Re-authenticate if possible
   - API errors: Log and continue with next item
3. User-friendly error messages displayed
4. Detailed errors logged for debugging
```

## Design Patterns

### 1. Dependency Injection
- Configuration injected into all components
- Enables easy testing and mocking
- Supports runtime configuration changes

### 2. Strategy Pattern
- Multiple authentication strategies for YouTube Music
- Different matching algorithms can be plugged in
- Extensible for new music services

### 3. Observer Pattern
- Progress callbacks for real-time updates
- Event-driven architecture for UI updates
- Decoupled progress reporting

### 4. Factory Pattern
- Client creation based on configuration
- Authentication method selection
- Report generator selection

## Performance Considerations

### 1. Rate Limiting
- Built-in rate limiting for all API calls
- Exponential backoff for retry attempts
- Configurable delays between requests

### 2. Memory Management
- Streaming processing for large playlists
- Minimal data caching
- Garbage collection friendly design

### 3. Network Optimization
- Connection pooling for HTTP requests
- Batch operations where possible
- Intelligent retry mechanisms

### 4. Caching
- Spotify token caching
- Search result caching (optional)
- Configuration caching

## Security Considerations

### 1. Credential Management
- Environment variables for sensitive data
- No hardcoded secrets
- Secure token storage

### 2. API Security
- OAuth2 for authentication
- HTTPS for all communications
- Token refresh handling

### 3. Data Privacy
- No persistent storage of user data
- Local processing only
- Minimal data collection

## Testing Strategy

### 1. Unit Tests
- Individual component testing
- Mock external dependencies
- Configuration validation testing

### 2. Integration Tests
- API client testing with real services
- End-to-end transfer testing
- Authentication flow testing

### 3. Performance Tests
- Large playlist handling
- Rate limiting compliance
- Memory usage monitoring

## Future Enhancements

### 1. Additional Music Services
- Apple Music integration
- Amazon Music support
- Deezer compatibility

### 2. Advanced Features
- Bidirectional sync
- Scheduled transfers
- Playlist comparison tools

### 3. User Interface
- Web-based GUI
- Desktop application
- Mobile app

### 4. Performance Improvements
- Parallel processing
- Advanced caching
- Database integration for large-scale operations

## Deployment Considerations

### 1. Packaging
- Standard Python package structure
- pip-installable package
- Docker containerization support

### 2. Configuration Management
- Environment-specific configurations
- Configuration validation
- Default value management

### 3. Monitoring and Logging
- Structured logging
- Performance metrics
- Error tracking

### 4. Documentation
- Comprehensive API documentation
- User guides and tutorials
- Troubleshooting guides

This architecture provides a solid foundation for the Spotify to YouTube Music Transfer Tool, balancing simplicity with extensibility, and ensuring maintainability as the project grows.