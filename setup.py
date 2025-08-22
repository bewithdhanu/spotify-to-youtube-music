#!/usr/bin/env python3
"""
Setup script for Spotify to YouTube Music Playlist Transfer Tool

This script helps users set up the environment and dependencies.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    else:
        print(f"✅ Python version: {sys.version.split()[0]}")

def check_pip():
    """Check if pip is available."""
    try:
        subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                      check=True, capture_output=True)
        print("✅ pip is available")
        return True
    except subprocess.CalledProcessError:
        print("❌ pip is not available")
        return False

def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_env_file():
    """Set up environment file."""
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        try:
            shutil.copy(env_example, env_file)
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env file with your API credentials")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("❌ .env.example file not found")
        return False

def check_git():
    """Check if git is available (optional)."""
    try:
        subprocess.run(['git', '--version'], check=True, capture_output=True)
        print("✅ Git is available")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Git is not available (optional)")
        return False

def print_next_steps():
    """Print next steps for the user."""
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETED!")
    print("="*60)
    print("\nNext steps:")
    print("\n1. 🔑 Set up Spotify API credentials:")
    print("   - Go to https://developer.spotify.com/dashboard")
    print("   - Create a new app")
    print("   - Copy Client ID and Client Secret")
    print("   - Edit .env file with your credentials")
    
    print("\n2. 🎬 Set up YouTube Music authentication:")
    print("   python main.py setup-youtube")
    
    print("\n3. 🧪 Test your setup:")
    print("   python main.py test-connection")
    
    print("\n4. 📋 List your Spotify playlists:")
    print("   python main.py list-playlists")
    
    print("\n5. 🚀 Transfer a playlist:")
    print("   python main.py transfer-playlist <playlist_id>")
    
    print("\n6. 📚 Get help:")
    print("   python main.py --help")
    
    print("\n" + "="*60)
    print("For detailed instructions, see README.md")
    print("="*60)

def main():
    """Main setup function."""
    print("🎵 Spotify to YouTube Music Transfer Tool Setup")
    print("="*50)
    
    # Check system requirements
    print("\n🔍 Checking system requirements...")
    check_python_version()
    
    if not check_pip():
        print("Please install pip and try again.")
        sys.exit(1)
    
    check_git()
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed during dependency installation.")
        sys.exit(1)
    
    # Set up environment file
    print("\n⚙️  Setting up configuration...")
    if not setup_env_file():
        print("\n❌ Setup failed during environment configuration.")
        sys.exit(1)
    
    # Print next steps
    print_next_steps()

if __name__ == '__main__':
    main()