# Safety-Bot - Formula 1 Discord Bot

## Overview
A Python-powered Discord bot that brings live Formula 1 data to Discord servers using the official OpenF1 API. The bot provides real-time race updates, schedules, driver standings, team information, and race results.

## Project Status
**Current State:** Fully configured and running on Replit
**Last Updated:** October 27, 2025

## Features
- 🏎️ **Driver Information** - Lists all F1 drivers organized by team
- 📅 **Race Calendar** - Complete 2025 F1 season schedule with race status
- 🏆 **Driver Standings** - Live driver standings (when available from API)
- 🏭 **Team Standings** - Constructor standings and team rosters
- ⏭️ **Next Race** - Countdown and details for upcoming race
- 🏁 **Race Results** - Results from the most recent race
- ❓ **Help Command** - Interactive help menu

## Technology Stack
- **Language:** Python 3.11
- **Framework:** discord.py 2.6.4
- **API:** OpenF1 API (https://api.openf1.org/v1)
- **Dependencies:**
  - discord.py >= 2.3.0
  - python-dotenv >= 1.0.0
  - aiohttp >= 3.9.0

## Project Architecture

### Main Components
- **bot.py** - Main bot file containing all commands and functionality
  - Bot initialization and Discord client setup
  - Command tree with slash commands
  - API integration with OpenF1
  - Embedded message formatting for Discord

### Data Sources
- **Live Data:** OpenF1 API for real-time session data and race results
- **Static Data:** Hardcoded 2025 calendar and driver roster (fallback when API data unavailable)

### Command Structure
All commands are accessed via the `/f1` slash command with the following options:
- `pilotes` - Show all drivers
- `calendrier` - Show race calendar
- `classement` - Show driver standings
- `equipes` - Show team standings
- `prochaine` - Show next race
- `resultats` - Show last race results
- `help` - Show help menu

## Environment Configuration
- **DISCORD_TOKEN** - Discord bot authentication token (stored in Replit Secrets)

## Running the Bot
The bot runs automatically via the configured workflow:
- Command: `python bot.py`
- Output: Console logs showing connection status and command syncing

## Recent Changes
- **October 27, 2025:** Initial Replit setup
  - Installed Python 3.11 and dependencies
  - Configured Discord token via Replit Secrets
  - Set up workflow for automatic bot execution
  - Updated .gitignore for Python project
  - Bot successfully connected to Discord

## Notes
- The bot uses French language for command names and messages
- Includes comprehensive F1 2025 season data
- Gracefully falls back to static data when API is unavailable
- PyNaCl warning can be ignored (voice features not needed)
