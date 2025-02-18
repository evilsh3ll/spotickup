# Spotickup

Spotickup is a Python script that backs up your followed artists and playlists from Spotify. It uses the [Spotipy](https://spotipy.readthedocs.io/) library to interact with the Spotify API.

## Installation

    ```bash
    git clone https://github.com/evilsh3ll/spotickup.git
    cd spotickup
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

## Configuration

1.  Obtain your Spotify API credentials:

    *   Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
    *   Create a new app.
    *   Note down your `Client ID` and `Client Secret`.
    *   Set the `Redirect URI` to `http://localhost:8888/callback`

2.  Edit `settings.json` with your credentials and desired output directory:

    ```json
    {
      "SPOTIPY_CLIENT_ID": "YOUR_CLIENT_ID",
      "SPOTIPY_CLIENT_SECRET": "YOUR_CLIENT_SECRET",
      "SPOTIPY_REDIRECT_URI": "http://localhost:8888/callback",
      "OUTPUT_DIR": "/path/to/your/output/directory"
    }
    ```

## Usage

1.  Login to spotify web

2.  Run the script:

    ```bash
    python spotickup.py
    ```
3.  The script will then download your followed artists and playlists and save them as JSON files in the specified output directory. The filenames will include a timestamp to keep track of backups.

## Screenshots
![image](https://i.postimg.cc/LXSVx7DV/image.png)
