# Troubleshooting Guide

## Common Issues and Solutions

### Authentication Issues

#### "Configuration validation failed"

**Symptoms:**
- Error message when running any command
- Application fails to start

**Solutions:**
1. **Check your `.env` file:**
   ```bash
   # Ensure these variables are set correctly
   SPOTIFY_CLIENT_ID=your_actual_client_id
   SPOTIFY_CLIENT_SECRET=your_actual_client_secret
   ```

2. **Verify Spotify credentials:**
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Check that your app exists and credentials are correct
   - Ensure redirect URI is set to `http://localhost:8080/callback`

3. **Run the test command:**
   ```bash
   python main.py test
   ```

#### "YouTube Music OAuth authentication not configured"

**Symptoms:**
- YouTube Music authentication fails
- Missing `oauth.json` file
- Error: "YouTube Music OAuth authentication not configured"

**Solutions:**
1. **Set up OAuth2 authentication:**
   ```bash
   python -c "from ytmusicapi import setup_oauth; setup_oauth('oauth.json')"
   ```

2. **Ensure Google Cloud Console setup:**
   - Create project and enable YouTube Data API v3
   - Create OAuth2 credentials (TVs and Limited Input devices)
   - Add YOUTUBE_CLIENT_ID and YOUTUBE_CLIENT_SECRET to .env file

#### "Invalid OAuth2 credentials"

**Symptoms:**
- OAuth authentication fails
- "Invalid client" error

**Solutions:**
1. **Regenerate OAuth credentials:**
   - Delete existing `oauth.json`
   - Run `python setup_youtube_oauth.py` again

2. **Check OAuth2 setup:**
   - Ensure OAuth2 consent screen is configured
   - Add your email to test users if in testing mode
   - Verify redirect URIs include `http://localhost:8080/callback`

### Transfer Issues

#### "Low match rates" or "No matches found"

**Symptoms:**
- Very few songs are successfully transferred
- Many "No suitable match found" messages

**Solutions:**
1. **Lower the match threshold:**
   ```env
   # In your .env file
   MATCH_THRESHOLD=0.6  # Default is 0.8
   ```

2. **Increase search results:**
   ```env
   MAX_SEARCH_RESULTS=10  # Default is 5
   ```

3. **Check regional availability:**
   - Some tracks may not be available in your region
   - Try using a VPN to different regions

4. **Manual verification:**
   - Search for problematic tracks manually on YouTube Music
   - Check if they exist under different names/artists

#### "Rate limiting errors"

**Symptoms:**
- "Too Many Requests" errors
- Transfer stops or slows down significantly

**Solutions:**
1. **Wait and retry:**
   - Rate limits are temporary
   - Wait 15-30 minutes before retrying

2. **Transfer smaller batches:**
   - Split large playlists into smaller chunks
   - Transfer 50-100 songs at a time

3. **Increase retry attempts:**
   ```env
   RETRY_ATTEMPTS=5  # Default is 3
   ```

#### "Playlist creation failed"

**Symptoms:**
- Cannot create new playlists on YouTube Music
- Permission errors

**Solutions:**
1. **Check YouTube Music subscription:**
   - Ensure you have an active YouTube Music subscription
   - Free accounts have limited playlist creation

2. **Verify authentication scope:**
   - Re-authenticate with YouTube Music
   - Ensure all required permissions are granted

3. **Try different privacy settings:**
   ```bash
   python main.py transfer PLAYLIST_ID --privacy UNLISTED
   ```

### Performance Issues

#### "Transfer is very slow"

**Symptoms:**
- Transfer takes much longer than expected
- Frequent pauses between songs

**Solutions:**
1. **Check internet connection:**
   - Ensure stable, fast internet connection
   - Test with smaller playlists first

2. **Optimize configuration:**
   ```env
   MAX_SEARCH_RESULTS=3  # Reduce search results
   RETRY_ATTEMPTS=2      # Reduce retry attempts
   ```

3. **Use liked music transfer:**
   ```bash
   # Faster than creating new playlists
   python main.py transfer-liked PLAYLIST_ID
   ```

#### "High memory usage"

**Symptoms:**
- System becomes slow during transfer
- Out of memory errors

**Solutions:**
1. **Transfer smaller batches:**
   - Process playlists in chunks of 100-200 songs

2. **Close other applications:**
   - Free up system memory

3. **Use command-line only:**
   - Avoid running GUI applications during transfer

### File and Directory Issues

#### "Module not found" errors

**Symptoms:**
- Import errors when running the application
- "No module named 'src.spotify_youtube_transfer'" errors

**Solutions:**
1. **Ensure correct directory structure:**
   ```
   Spotify-to-Youtube/
   ├── main.py
   ├── setup.py
   ├── src/
   │   └── spotify_youtube_transfer/
   │       ├── __init__.py
   │       ├── config.py
   │       ├── spotify_client.py
   │       ├── youtube_music_client.py
   │       ├── track_matcher.py
   │       └── playlist_transfer.py
   └── docs/
   ```

2. **Run from project root:**
   ```bash
   cd /path/to/Spotify-to-Youtube
   python main.py
   ```

3. **Check Python path:**
   ```bash
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

#### "Permission denied" errors

**Symptoms:**
- Cannot create or write files
- Authentication files cannot be saved

**Solutions:**
1. **Check file permissions:**
   ```bash
   chmod 755 .
   chmod 644 *.py
   ```

2. **Run with appropriate permissions:**
   - Ensure you have write permissions in the project directory

3. **Check disk space:**
   - Ensure sufficient disk space for log files and cache

## Debug Mode

### Enable Debug Logging

```bash
# Enable detailed logging
python main.py --log-level DEBUG transfer PLAYLIST_ID
```

### Log File Analysis

Check the generated log files:
- `spotify_to_youtube.log`: Main application log
- `transfer_report_*.json`: Detailed transfer reports

### Common Log Messages

**"Spotify authentication successful"**
- ✅ Spotify connection is working

**"YouTube Music authentication failed"**
- ❌ Check YouTube Music setup

**"Track match found with similarity: 0.85"**
- ✅ Good match found

**"No suitable match found for track"**
- ⚠️ Track not available or poor matching

**"Rate limit exceeded, waiting..."**
- ⚠️ Normal behavior, will retry automatically

## Getting Help

### Before Reporting Issues

1. **Check this troubleshooting guide**
2. **Enable debug logging** and check log files
3. **Test with a small playlist** (5-10 songs)
4. **Verify your setup** with `python main.py test`
5. **Check for updates** to the tool

### Reporting Bugs

When reporting issues, please include:

1. **System information:**
   - Operating system and version
   - Python version (`python --version`)
   - Tool version

2. **Error details:**
   - Complete error message
   - Steps to reproduce
   - Debug log output (if applicable)

3. **Configuration:**
   - Anonymized `.env` file content
   - Command used
   - Playlist size and type

### Support Channels

- **GitHub Issues**: [Create an issue](https://github.com/bewithdhanu/spotify-to-youtube-music/issues/new)
- **Documentation**: Check the `docs/` folder
- **Community**: GitHub Discussions

## Frequently Asked Questions (FAQ)

### General Questions

**Q: Is this tool free to use?**
A: Yes, the tool is open source and free. However, you need active subscriptions to Spotify and YouTube Music.

**Q: Does this tool store my music data?**
A: No, all processing happens locally. The tool only transfers playlist metadata and song references.

**Q: Can I transfer from YouTube Music to Spotify?**
A: Currently, the tool only supports Spotify to YouTube Music transfers.

**Q: How accurate is the track matching?**
A: Accuracy varies but typically ranges from 80-95% depending on music library overlap and regional availability.

### Technical Questions

**Q: Why do I need both Spotify and YouTube Music accounts?**
A: The tool needs to access both services to read from Spotify and write to YouTube Music.

**Q: Can I run multiple transfers simultaneously?**
A: Not recommended due to API rate limits. Run transfers sequentially.

**Q: How long does a transfer take?**
A: Approximately 1-2 seconds per song, so a 100-song playlist takes 2-3 minutes.

**Q: Can I pause and resume transfers?**
A: Currently not supported. Transfers must complete in one session.

### Privacy and Security

**Q: Is my data secure?**
A: Yes, the tool uses official OAuth flows and processes everything locally.

**Q: What permissions does the tool need?**
A: Read access to Spotify playlists and write access to YouTube Music playlists.

**Q: Can I revoke access later?**
A: Yes, you can revoke access through Spotify and Google account settings.

### Limitations

**Q: Why aren't all my songs transferred?**
A: Some songs may not be available on YouTube Music due to licensing or regional restrictions.

**Q: Can I transfer podcasts or audiobooks?**
A: No, the tool is designed specifically for music tracks.

**Q: Is there a limit to playlist size?**
A: No hard limit, but very large playlists (1000+ songs) may take considerable time.

**Q: Can I transfer collaborative playlists?**
A: Yes, if you have access to read the playlist on Spotify.