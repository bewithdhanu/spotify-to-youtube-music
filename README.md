# Spotify to YouTube Music Transfer Tool

🎵 A comprehensive Python tool to transfer your Spotify playlists to YouTube Music with intelligent track matching and real-time progress tracking.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](CONTRIBUTING.md)

## ✨ Features

- **🎯 Intelligent Track Matching**: Advanced fuzzy matching algorithm to find the best YouTube Music equivalents
- **❤️ Liked Music Transfer**: Transfer playlists directly to your YouTube Music liked songs
- **📊 Real-time Progress**: Live progress tracking with success/failure counters
- **🔄 Individual Processing**: Process and add songs one by one with immediate feedback
- **📋 Detailed Reporting**: Comprehensive transfer reports with match statistics
- **⚙️ Flexible Configuration**: Customizable matching thresholds and transfer settings
- **🖥️ CLI Interface**: Easy-to-use command-line interface with progress tracking
- **🛡️ Error Handling**: Robust error handling with retry mechanisms
- **🔒 Privacy Control**: Set playlist privacy (Private, Public, Unlisted)

## Prerequisites

- Python 3.8 or higher
- Spotify Developer Account
- YouTube Music subscription (for playlist creation)

## Installation

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bewithdhanu/spotify-to-youtube-music.git
   cd spotify-to-youtube-music
   ```

2. **Run the setup script:**
   ```bash
   python setup.py
   ```
   This will automatically:
   - Check Python version compatibility
   - Create a virtual environment
   - Install all dependencies
   - Set up configuration files

3. **Configure API credentials:**
   Edit the generated `.env` file with your API credentials:
   ```
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   SPOTIFY_REDIRECT_URI=http://localhost:8080/callback
   YOUTUBE_CLIENT_ID=your_youtube_client_id
   YOUTUBE_CLIENT_SECRET=your_youtube_client_secret
   ```

### Manual Installation

For detailed installation instructions, including manual setup and troubleshooting, see our comprehensive [Installation Guide](docs/installation.md).

## Setup

### 1. Spotify API Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Copy the **Client ID** and **Client Secret**
4. Add `http://localhost:8080/callback` to Redirect URIs
5. Update your `.env` file:
   ```
   SPOTIFY_CLIENT_ID=your_client_id_here
   SPOTIFY_CLIENT_SECRET=your_client_secret_here
   ```

### 2. YouTube Music Setup

**YouTube Music uses OAuth2 authentication for secure API access:**

1. **Run the OAuth setup script**:
   ```bash
   python setup_youtube_oauth.py
   ```

2. **Follow the guided setup**:
   - The script will help you create OAuth2 credentials in Google Cloud Console
   - It will guide you through enabling the YouTube Data API v3
   - You'll authorize the application through your browser
   - An `oauth.json` file will be created automatically

3. **Benefits of OAuth2**:
   - More reliable and stable authentication
   - No need to manually copy browser headers
   - Automatic token refresh
   - Better security

### 3. Test Your Setup

```bash
python main.py test-connection
```

## 🚀 Usage

### Quick Commands

**Test connections:**
```bash
python main.py test
```

**List your playlists:**
```bash
# List Spotify playlists
python main.py list-spotify --limit 25

# List YouTube Music playlists
python main.py list-youtube --limit 25
```

**Transfer to new playlist:**
```bash
# Transfer a playlist to a new YouTube Music playlist
python main.py transfer SPOTIFY_PLAYLIST_ID --name "My Playlist"

# With privacy settings
python main.py transfer SPOTIFY_PLAYLIST_ID --name "My Playlist" --privacy PUBLIC

# Transfer your liked songs
python main.py transfer liked_songs --name "My Liked Songs"
```

**Transfer to liked music:**
```bash
# Transfer any playlist directly to your YouTube Music liked songs
python main.py transfer-liked SPOTIFY_PLAYLIST_ID

# Transfer your Spotify liked songs to YouTube Music liked songs
python main.py transfer-liked liked_songs
```

**Search and compare tracks:**
```bash
# Search for tracks on both platforms
python main.py search "Bohemian Rhapsody" --limit 10
```

### Comprehensive Usage Guide

For detailed usage examples, advanced features, and Python API integration, see our [Usage Examples Documentation](docs/usage-examples.md).

### Python API

You can also use the tool programmatically:

```python
from src.spotify_youtube_transfer import Config, PlaylistTransfer

# Initialize with configuration
config = Config()
transfer = PlaylistTransfer(config)

# Transfer a playlist
result = transfer.transfer_playlist(
    spotify_playlist_name="My Playlist",
    youtube_playlist_name="My YouTube Playlist"
)
```

For complete API documentation, see [API Documentation](docs/api.md).

## 📚 Documentation

This project includes comprehensive documentation to help you get the most out of the tool:

### 📖 User Documentation
- **[Installation Guide](docs/installation.md)** - Complete setup instructions for all platforms
- **[Usage Examples](docs/usage-examples.md)** - Practical examples and real-world scenarios
- **[Troubleshooting](docs/troubleshooting.md)** - Solutions for common issues and FAQ

### 🔧 Developer Documentation
- **[API Documentation](docs/api.md)** - Complete Python API reference
- **[Architecture](docs/architecture.md)** - Technical design and project structure

### 🚀 Quick Links
- **New to the tool?** Start with the [Installation Guide](docs/installation.md)
- **Need examples?** Check [Usage Examples](docs/usage-examples.md)
- **Having issues?** Visit [Troubleshooting](docs/troubleshooting.md)
- **Want to integrate?** See [API Documentation](docs/api.md)

All documentation is kept up-to-date and includes tested examples with expected outputs.

### Demo Mode

```bash
# Run a full demonstration of all features
python main.py demo
```

## ⚙️ Configuration

Edit your `.env` file to customize the behavior:

```env
# Spotify API Configuration
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here

# Track Matching Configuration
MATCH_THRESHOLD=0.8          # Minimum similarity score (0.0-1.0)
MAX_SEARCH_RESULTS=5         # Number of search results to consider
RETRY_ATTEMPTS=3             # Number of retry attempts for failed operations
```

## How It Works

### Track Matching Algorithm

1. **Query Generation**: Creates multiple search queries using different combinations of artist and track names
2. **Fuzzy Matching**: Uses advanced string similarity algorithms to compare tracks
3. **Multi-factor Scoring**: Considers track title, artist name, and duration similarity
4. **Threshold Filtering**: Only accepts matches above the configured similarity threshold

### Transfer Process

1. **Authentication**: Connects to both Spotify and YouTube Music APIs
2. **Playlist Retrieval**: Fetches playlist metadata and track information from Spotify
3. **Track Matching**: Finds YouTube Music equivalents for each track
4. **Playlist Creation**: Creates a new playlist on YouTube Music
5. **Track Addition**: Adds matched tracks to the new playlist
6. **Reporting**: Generates detailed transfer reports

## Troubleshooting

### Common Issues

**"Configuration validation failed"**
- Ensure your `.env` file has valid Spotify credentials
- Run `python main.py setup-youtube` to set up YouTube Music authentication

**"YouTube Music headers file not found"**
- Run `python main.py setup-youtube` to generate the authentication file
- Ensure you're logged into YouTube Music in your browser

**"Low match rates"**
- Lower the `MATCH_THRESHOLD` in your `.env` file
- Some tracks may not be available on YouTube Music
- Regional availability differences can affect matching

**"Rate limiting errors"**
- The tool includes built-in rate limiting
- Increase delays between requests if needed
- Try transferring smaller batches

### Debug Mode

Enable debug logging for detailed information:

```bash
python main.py --log-level DEBUG transfer-playlist YOUR_PLAYLIST_ID
```

## 📁 Project Structure

```
spotify-youtube-transfer/
├── main.py                           # Main CLI application entry point
├── setup.py                          # Automated setup and installation
├── requirements.txt                  # Python dependencies
├── .env.example                      # Environment variables template
├── .gitignore                        # Git ignore rules
├── LICENSE                           # MIT License
├── README.md                         # This file
├── docs/                             # 📚 Comprehensive documentation
│   ├── README.md                     # Documentation index
│   ├── installation.md               # Detailed installation guide
│   ├── usage-examples.md             # Usage examples and tutorials
│   ├── api.md                        # API documentation
│   ├── troubleshooting.md            # Troubleshooting and FAQ
│   └── architecture.md               # Technical architecture
└── src/                              # 🐍 Python source code
    └── spotify_youtube_transfer/     # Main package
        ├── __init__.py               # Package initialization
        ├── config.py                 # Configuration management
        ├── spotify_client.py         # Spotify API client
        ├── youtube_music_client.py   # YouTube Music client
        ├── track_matcher.py          # Track matching algorithm
        ├── playlist_transfer.py      # Playlist transfer logic
        └── example_usage.py          # Usage examples
```

### Key Directories

- **`src/spotify_youtube_transfer/`** - Core Python package with all functionality
- **`docs/`** - Comprehensive documentation for users and developers
- **Root directory** - Entry points, configuration, and project metadata

### Documentation Structure

Our documentation is organized for different user types:
- **New users**: Start with `docs/installation.md`
- **Regular users**: See `docs/usage-examples.md`
- **Developers**: Check `docs/api.md` and `docs/architecture.md`
- **Troubleshooting**: Visit `docs/troubleshooting.md`

## Generated Files

- `oauth.json`: YouTube Music OAuth2 authentication token
- `transfer_report_*.json`: Detailed transfer reports
- `spotify_to_youtube.log`: Application logs (if enabled)
- `.spotify_cache`: Spotify authentication cache

## Limitations

- **YouTube Music Availability**: Not all Spotify tracks are available on YouTube Music
- **Regional Differences**: Track availability varies by region
- **Matching Accuracy**: Algorithm-based matching may not be 100% accurate
- **Rate Limits**: APIs have rate limits that may slow down large transfers
- **Authentication**: YouTube Music authentication requires manual browser setup

## Privacy and Security

- **Local Processing**: All processing happens locally on your machine
- **No Data Storage**: The tool doesn't store your music data
- **Secure Authentication**: Uses official OAuth flows for both services
- **Credential Protection**: API credentials are stored locally in environment files

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute

- 🐛 **Report Bugs**: Found a bug? [Open an issue](../../issues/new)
- 💡 **Suggest Features**: Have an idea? [Create a feature request](../../issues/new)
- 📝 **Improve Documentation**: Help make our docs better
- 🔧 **Submit Code**: Fix bugs or add new features

### Development Setup

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/spotify-to-youtube-music.git
   cd spotify-to-youtube-music
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Pull Request Process

1. **Test your changes** thoroughly
2. **Update documentation** if needed
3. **Follow the existing code style**
4. **Write clear commit messages**
5. **Submit a pull request** with a detailed description

### Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for personal use only. Ensure you comply with Spotify and YouTube Music terms of service. The developers are not responsible for any violations of service terms or copyright issues.

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Enable debug logging to get more information
3. Check the generated log files
4. Create an issue with detailed error information

---

**Happy playlist transferring! 🎵➡️🎬**