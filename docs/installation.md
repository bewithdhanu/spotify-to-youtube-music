# Installation Guide

## System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Memory**: 512 MB RAM
- **Storage**: 100 MB free space
- **Internet**: Stable broadband connection

### Recommended Requirements
- **Python**: 3.9 or higher
- **Memory**: 1 GB RAM
- **Storage**: 500 MB free space (for logs and cache)

### Prerequisites
- Active Spotify account
- YouTube Music subscription (required for playlist creation)
- Spotify Developer Account (free)
- Google Cloud Account (free tier sufficient)

## Installation Methods

### Method 1: Git Clone (Recommended)

1. **Install Git** (if not already installed):
   - **Windows**: Download from [git-scm.com](https://git-scm.com/)
   - **macOS**: `brew install git` or install Xcode Command Line Tools
   - **Linux**: `sudo apt install git` (Ubuntu/Debian) or `sudo yum install git` (CentOS/RHEL)

2. **Clone the repository**:
   ```bash
   git clone https://github.com/bewithdhanu/spotify-to-youtube-music.git
   cd spotify-to-youtube-music
   ```

3. **Verify the project structure**:
   ```bash
   ls -la
   # Should show: main.py, setup.py, src/, docs/, requirements.txt, etc.
   ```

### Method 2: Download ZIP

1. **Download the ZIP file**:
   - Go to the [GitHub repository](https://github.com/bewithdhanu/spotify-to-youtube-music)
   - Click "Code" → "Download ZIP"

2. **Extract and navigate**:
   ```bash
   unzip spotify-to-youtube-music-main.zip
   cd spotify-to-youtube-music-main
   ```

## Python Environment Setup

### Step 1: Verify Python Installation

```bash
# Check Python version
python --version
# or
python3 --version

# Should show Python 3.8 or higher
```

**If Python is not installed:**
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **macOS**: `brew install python3` or download from python.org
- **Linux**: `sudo apt install python3 python3-pip` (Ubuntu/Debian)

### Step 2: Create Virtual Environment

**Why use a virtual environment?**
- Isolates project dependencies
- Prevents conflicts with other Python projects
- Makes dependency management easier

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# Verify activation (should show (venv) in prompt)
which python
```

### Step 3: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

**Common dependency issues:**

- **If `pip install` fails on Windows:**
  ```bash
  # Install Microsoft C++ Build Tools
  # Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
  ```

- **If `pip install` fails on macOS:**
  ```bash
  # Install Xcode Command Line Tools
  xcode-select --install
  ```

- **If `pip install` fails on Linux:**
  ```bash
  # Install build essentials
  sudo apt install build-essential python3-dev
  ```

## Configuration Setup

### Step 1: Environment Variables

1. **Copy the example environment file**:
   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` file**:
   ```bash
   # Use your preferred text editor
   nano .env
   # or
   code .env
   # or
   vim .env
   ```

3. **Basic configuration**:
   ```env
   # Spotify API Configuration (Required)
   SPOTIFY_CLIENT_ID=your_spotify_client_id_here
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
   
   # Track Matching Configuration (Optional)
   MATCH_THRESHOLD=0.8
   MAX_SEARCH_RESULTS=5
   RETRY_ATTEMPTS=3
   
   # Logging Configuration (Optional)
   LOG_LEVEL=INFO
   LOG_FILE=spotify_to_youtube.log
   ```

### Step 2: Spotify API Setup

1. **Go to Spotify Developer Dashboard**:
   - Visit [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
   - Log in with your Spotify account

2. **Create a new app**:
   - Click "Create App"
   - Fill in the details:
     - **App Name**: "Spotify to YouTube Music Transfer"
     - **App Description**: "Personal playlist transfer tool"
     - **Website**: Leave blank or use your GitHub repo URL
     - **Redirect URI**: `http://localhost:8080/callback`
   - Accept terms and create

3. **Get your credentials**:
   - Click on your newly created app
   - Click "Settings"
   - Copy the **Client ID** and **Client Secret**
   - Paste them into your `.env` file

4. **Configure redirect URI**:
   - In app settings, click "Edit Settings"
   - Under "Redirect URIs", add: `http://localhost:8080/callback`
   - Click "Save"

### Step 3: YouTube Music Setup

#### Option A: OAuth2 Setup (Recommended)

1. **Run the automated setup**:
   ```bash
   python setup_youtube_oauth.py
   ```

2. **Follow the guided process**:
   - The script will open your browser
   - You'll be guided through Google Cloud Console setup
   - OAuth2 credentials will be created automatically

3. **Manual OAuth2 setup** (if automated setup fails):
   
   a. **Go to Google Cloud Console**:
      - Visit [console.cloud.google.com](https://console.cloud.google.com/)
      - Create a new project or select existing one
   
   b. **Enable YouTube Data API v3**:
      - Go to "APIs & Services" → "Library"
      - Search for "YouTube Data API v3"
      - Click and enable it
   
   c. **Create OAuth2 credentials**:
      - Go to "APIs & Services" → "Credentials"
      - Click "Create Credentials" → "OAuth client ID"
      - Choose "Desktop application"
      - Name it "Spotify to YouTube Music Transfer"
      - Download the JSON file
   
   d. **Configure OAuth consent screen**:
      - Go to "APIs & Services" → "OAuth consent screen"
      - Choose "External" user type
      - Fill in required fields:
        - **App name**: "Spotify to YouTube Music Transfer"
        - **User support email**: Your email
        - **Developer contact**: Your email
      - Add your email to test users
   
   e. **Save credentials**:
      - Rename downloaded file to `oauth.json`
      - Place it in the project root directory

#### Troubleshooting OAuth2 Setup

If you encounter issues with OAuth2:

1. **Verify Google Cloud Console setup:**
   - Ensure YouTube Data API v3 is enabled
   - Check OAuth2 credentials are for "TVs and Limited Input devices"
   - Confirm redirect URI is set correctly

2. **Check environment variables:**
   ```bash
   grep YOUTUBE .env
   ```

3. **Regenerate OAuth token if needed:**
   ```bash
   rm oauth.json
   python -c "from ytmusicapi import setup_oauth; setup_oauth('oauth.json')"
   ```

## Verification

### Test Your Installation

1. **Run the connection test**:
   ```bash
   python main.py test
   ```

2. **Expected output**:
   ```
   🎵 Spotify to YouTube Music Transfer Tool
   
   Testing Spotify connection...
   ✅ Spotify connection successful
   
   Testing YouTube Music connection...
   ✅ YouTube Music connection successful
   
   🎉 All connections successful! You're ready to transfer playlists.
   ```

3. **If tests fail**:
   - Check the [Troubleshooting Guide](troubleshooting.md)
   - Verify your `.env` file configuration
   - Ensure all authentication files are in place

### Test Basic Functionality

1. **List your Spotify playlists**:
   ```bash
   python main.py list-spotify --limit 5
   ```

2. **List your YouTube Music playlists**:
   ```bash
   python main.py list-youtube --limit 5
   ```

3. **Test search functionality**:
   ```bash
   python main.py search "Bohemian Rhapsody" --limit 3
   ```

## Post-Installation Setup

### Optional: Configure Logging

1. **Enable file logging**:
   ```env
   # In your .env file
   LOG_LEVEL=DEBUG
   LOG_FILE=transfer.log
   ```

2. **Create logs directory**:
   ```bash
   mkdir logs
   ```

### Optional: Shell Aliases

Add convenient aliases to your shell configuration:

```bash
# Add to ~/.bashrc, ~/.zshrc, or equivalent
alias syt='cd /path/to/spotify-to-youtube-music && source venv/bin/activate'
alias syt-test='python main.py test'
alias syt-transfer='python main.py transfer'
```

### Optional: Desktop Shortcut

**Windows:**
1. Create a batch file `spotify-youtube-transfer.bat`:
   ```batch
   @echo off
   cd /d "C:\path\to\spotify-to-youtube-music"
   call venv\Scripts\activate
   python main.py %*
   pause
   ```

**macOS:**
1. Create an Automator application or shell script

**Linux:**
1. Create a desktop entry in `~/.local/share/applications/`

## Updating the Tool

### Git Update

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Test the update
python main.py test
```

### Manual Update

1. Download the latest release
2. Backup your `.env` file and authentication files
3. Replace project files
4. Restore your configuration files
5. Update dependencies

## Uninstallation

### Complete Removal

1. **Deactivate virtual environment**:
   ```bash
   deactivate
   ```

2. **Remove project directory**:
   ```bash
   rm -rf /path/to/spotify-to-youtube-music
   ```

3. **Revoke API access** (optional):
   - **Spotify**: Go to [Spotify Account Overview](https://www.spotify.com/account/privacy/) → "Privacy Settings" → "Apps"
   - **Google**: Go to [Google Account](https://myaccount.google.com/permissions) → "Third-party apps & services"

### Partial Removal (Keep Configuration)

1. **Backup configuration**:
   ```bash
   cp .env ~/spotify-youtube-backup.env
   cp oauth.json ~/spotify-youtube-oauth-backup.json
   ```

2. **Remove project files**:
   ```bash
   rm -rf src/ docs/ *.py requirements.txt
   ```

## Troubleshooting Installation

### Common Issues

**"Python not found"**
- Install Python 3.8+ from python.org
- Add Python to your system PATH

**"pip not found"**
- Reinstall Python with pip included
- Or install pip separately: `python -m ensurepip --upgrade`

**"Permission denied"**
- Use virtual environment (recommended)
- Or install with `--user` flag: `pip install --user -r requirements.txt`

**"Module not found after installation"**
- Ensure virtual environment is activated
- Verify you're in the correct directory
- Check Python path: `python -c "import sys; print(sys.path)"`

**"SSL certificate errors"**
- Update certificates: `pip install --upgrade certifi`
- Or use trusted hosts: `pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt`

For more detailed troubleshooting, see the [Troubleshooting Guide](troubleshooting.md).

## Next Steps

After successful installation:

1. **Read the [API Documentation](api.md)** for advanced usage
2. **Check the [Troubleshooting Guide](troubleshooting.md)** for common issues
3. **Start with a small test playlist** (5-10 songs)
4. **Explore different transfer options** (new playlist vs. liked music)
5. **Configure settings** to match your preferences

Happy playlist transferring! 🎵➡️🎬