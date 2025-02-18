import spotipy, json, os, pyfiglet, datetime, warnings
from colorama import Fore, init
from spotipy.oauth2 import SpotifyOAuth
init(autoreset=True)
warnings.filterwarnings("ignore", category=DeprecationWarning)

def load_settings(file_name):
	settings={}
	try:
		with open(file_name, 'r') as f:
			settings = json.load(f)
	except FileNotFoundError:
		print(Fore.RED + f"ERR: missing file '{file_name}'")
		exit(1)
	except json.JSONDecodeError:
		print(Fore.RED + f"ERR: file '{file_name}' not valid")
		exit(1)
	return settings

def get_artists(sp):
	print(Fore.YELLOW + "Downloading Artists..")
	artists = []
	results = sp.current_user_followed_artists()
	while len(results)>0:
		for curr_artist in results['artists']['items']:
			artists.append({
				'name': curr_artist['name'],
				'url':  curr_artist['external_urls']['spotify']
			})
		if results['artists']['next'] is None:
			break
		results = sp.next(results['artists'])
		
	artists=sorted(artists, key=lambda x: x['name'])
	print(Fore.GREEN + f'Loaded {len(artists)} Artists..\n')
	return artists
	
def get_playlists(sp):
	print(Fore.YELLOW + "Downloading Playlsts..")
	playlists = []
	results = sp.current_user_playlists()
	while len(results)>0:
		for curr_playlist in results['items']:
			playlists.append({
				'name': curr_playlist['name'],
				'url': curr_playlist['external_urls']['spotify']
			})
		if results['next'] is None:
			break
		results = sp.next(results)

	playlists = sorted(playlists, key=lambda x: x['name'])
	print(Fore.GREEN + f'Loaded {len(playlists)} Playlists..\n')
	return playlists
	
def main():
	print(Fore.GREEN + pyfiglet.figlet_format("Spotickup",font='graffiti'))
		
	#VARS
	scope = 'user-follow-read playlist-read-private'
	curr_path = os.path.dirname(os.path.abspath(__file__))
	settings_path = os.path.join(curr_path,'settings.json')
	cache_path = os.path.join(curr_path,'.cache')
	
	# ERROR CHECK
	if not os.path.exists(settings_path):
		print(Fore.RED + f"ERR: wrong settings path '{settings_path}'")
		exit(1)
	settings = load_settings(settings_path)
	if not os.path.exists(settings['OUTPUT_DIR']):
		print(Fore.RED + f"ERR: wrong path '{settings['OUTPUT_DIR']}'")
	
	# AUTH
	print(Fore.YELLOW + "Logging in..")
	sp_oauth = SpotifyOAuth(client_id=settings.get('SPOTIPY_CLIENT_ID'), client_secret=settings.get('SPOTIPY_CLIENT_SECRET'), redirect_uri=settings.get('SPOTIPY_REDIRECT_URI'), scope=scope, cache_path=cache_path)
	token_info = sp_oauth.get_cached_token()
	if not token_info:
		token_info = sp_oauth.get_access_token()

	if token_info:
		sp = spotipy.Spotify(auth_manager=sp_oauth)
		sp.auth_manager.token_info = token_info  # load token in spotify manager
		if sp.auth_manager.is_token_expired(token_info): # verify token expiration
		    token_info = sp_oauth.refresh_access_token(token_info['refresh_token']) # token refresh
		    save_token(token_info) # save new token
		    sp = spotipy.Spotify(auth_manager=sp_oauth) # update new token in spotify manager
	else:
		print(Fore.RED + f"ERR: error loading token. Please log in to Spotify in the default browser.")
		exit(1)
	
	# GET ARTISTS
	artists = get_artists(sp)
	# GET PLAYLISTS
	playlists = get_playlists(sp)
	
	# SAVE ARTISTS LIST
	print(Fore.YELLOW + "Saving Backups..")
	timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
	filename_artists = f'artists_{timestamp}.json'
	output_artists = os.path.join(settings['OUTPUT_DIR'],filename_artists)
	with open(output_artists, 'w') as f:
		json.dump(artists, f, indent=4)
	print(f"{Fore.GREEN}Artists Saved in {Fore.RESET}{os.path.abspath(output_artists)}")
	
	# SAVE PLAYLISTS LIST
	filename_playlists = f'playlists_{timestamp}.json'
	output_playlists = os.path.join(settings['OUTPUT_DIR'],filename_playlists)
	with open(output_playlists, 'w') as f:
		json.dump(playlists, f, indent=4)
	print(f"{Fore.GREEN}Playlists Saved in {Fore.RESET}{os.path.abspath(output_playlists)}")

if __name__ == "__main__":
    main()
