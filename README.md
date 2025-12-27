# Spotify Tracks by Genre

Spotify Tracks by Genre is a Python application that extracts and analyzes track information
for a specified music genre using the **Spotify Web API**. This tool is ideal for
data exploration, music analysis, and building genre-specific datasets for visualization
or machine learning tasks.

## Overview

Many music analytics projects require datasets of tracks labeled by genre.
This repository provides a way to **query Spotify’s API** for track metadata within
a specific genre and save that information for analysis or further processing.

The extracted data can be used for tasks such as:

- Genre distribution analysis  
- Audio feature comparison across genres  
- Data preparation for machine learning  
- Music recommendation research

## Features

- Fetches track metadata from Spotify based on genre
- Stores track information in structured output formats (CSV/JSON/other)
- Supports customizable filters and genre selection
- Useful for exploratory data analysis, visualization, and modeling

## Installation

### Prerequisites

1. **Python 3.8+**
2. A Spotify Developer account and application credentials
   - You will need a **Client ID** and **Client Secret** from:
     https://developer.spotify.com/dashboard

### Setup

1. Clone the repository:

```bash
git clone https://github.com/AmirhosseinVafasefat/spotify-tracks-by-genre.git
cd spotify-tracks-by-genre
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create a `.env file` (based on `.env.example`) with your Spotify credentials:

SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret

## Usage

### Configuration

Update the parameters in `settings.py`, including the target genre
and output configuration.

### Running the Program

Execute the following command from the project root:

```bash
python main.py
```
