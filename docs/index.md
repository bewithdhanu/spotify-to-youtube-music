# Spotify to YouTube Music Transfer

<div align="center">
  <h2>🎵 Transfer your Spotify playlists to YouTube Music with ease 🎬</h2>
  <p><strong>A powerful, user-friendly tool for seamless playlist migration</strong></p>
</div>

---

## ✨ Features

- **🔄 Complete Playlist Transfer** - Move entire playlists from Spotify to YouTube Music
- **❤️ Liked Songs Support** - Transfer songs to your YouTube Music liked songs
- **🎯 Smart Matching** - Advanced algorithm for accurate song matching
- **📊 Real-time Progress** - Live updates during transfer process
- **🔐 Secure Authentication** - OAuth2 for both Spotify and YouTube Music
- **📝 Detailed Reports** - Comprehensive transfer reports with match statistics
- **🛠️ Python API** - Programmatic access for developers
- **🖥️ Cross-platform** - Works on Windows, macOS, and Linux

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/bewithdhanu/spotify-to-youtube-music.git
cd spotify-to-youtube-music

# Run automated setup
python setup.py
```

### Basic Usage

```bash
# Test your setup
python main.py test

# Transfer a playlist
python main.py transfer "My Awesome Playlist" --to-new-playlist "My YouTube Playlist"

# Transfer to liked songs
python main.py transfer "My Awesome Playlist" --to-liked
```

## 📚 Documentation

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Getting Started**

    ---

    New to the tool? Start here for installation and basic usage.

    [:octicons-arrow-right-24: Installation Guide](installation.md)

-   :material-code-braces:{ .lg .middle } **Usage Examples**

    ---

    Learn through practical examples and real-world scenarios.

    [:octicons-arrow-right-24: Usage Examples](usage-examples.md)

-   :material-api:{ .lg .middle } **API Reference**

    ---

    Complete API documentation for developers and advanced users.

    [:octicons-arrow-right-24: API Documentation](api.md)

-   :material-help-circle:{ .lg .middle } **Troubleshooting**

    ---

    Solutions for common issues and frequently asked questions.

    [:octicons-arrow-right-24: Troubleshooting Guide](troubleshooting.md)

</div>

## 🎯 Use Cases

### For Music Lovers
- **Platform Migration** - Switch from Spotify to YouTube Music without losing your playlists
- **Backup Playlists** - Keep copies of your favorite playlists on multiple platforms
- **Discover New Music** - Use YouTube Music's recommendation engine with your existing taste

### For Developers
- **Automation** - Integrate playlist transfers into your applications
- **Batch Processing** - Transfer multiple playlists programmatically
- **Custom Workflows** - Build custom music management tools

### For Content Creators
- **Multi-platform Presence** - Maintain playlists across different music services
- **Audience Engagement** - Share playlists on the platform your audience prefers
- **Content Backup** - Ensure your curated playlists are never lost

## 🔧 Key Components

### Smart Track Matching
Our advanced matching algorithm considers:
- Song title and artist name similarity
- Album information when available
- Duration matching for accuracy
- Fuzzy matching for slight variations

### Secure Authentication
- **Spotify**: OAuth2 with PKCE for secure API access
- **YouTube Music**: OAuth2 with Google Cloud integration
- **No Passwords**: Never stores or requires your login credentials

### Comprehensive Reporting
- **Match Statistics**: Success rates and detailed breakdowns
- **Failed Matches**: List of songs that couldn't be found
- **Transfer Logs**: Complete audit trail of all operations
- **Export Options**: JSON reports for further analysis

## 📊 Performance

- **Fast Processing**: Concurrent API requests for optimal speed
- **Rate Limiting**: Respects API limits to avoid throttling
- **Memory Efficient**: Processes large playlists without excessive memory usage
- **Resumable**: Can continue interrupted transfers

## 🤝 Contributing

We welcome contributions! Here's how you can help:

- **🐛 Report Bugs**: Found an issue? [Create an issue](https://github.com/bewithdhanu/spotify-to-youtube-music/issues)
- **💡 Suggest Features**: Have an idea? [Start a discussion](https://github.com/bewithdhanu/spotify-to-youtube-music/discussions)
- **📝 Improve Docs**: Help make our documentation better
- **🔧 Submit Code**: Fork, improve, and submit pull requests

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/bewithdhanu/spotify-to-youtube-music/blob/main/LICENSE) file for details.

## 🙏 Acknowledgments

- **[Spotipy](https://spotipy.readthedocs.io/)** - Spotify Web API wrapper
- **[YTMusicAPI](https://ytmusicapi.readthedocs.io/)** - YouTube Music API wrapper
- **[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)** - Documentation theme

---

<div align="center">
  <p><strong>Ready to transfer your playlists?</strong></p>
  <p><a href="installation/">Get Started →</a></p>
</div>