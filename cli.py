from dao import dao_get_all_artists, dao_get_all_albums, dao_get_all_tracks
from data_ingestion import parallel_extract_artists, extract_tracks_by_albums, parallel_extract_albums, extract_several_tracks_info, parallel_extract_artist_by_id
from file_reader import extract_rappers, write_rappers_file, read_rappers

from config import QUERY, MAX_RESULTS, RESULTS_PER_PAGE

def cli_help() -> None:
    print('''
        Enter:
        0 - to see total entries in database
        1 - to extract artists from the genre query
        2 - to extract artists from a .txt file
        3 - to extract albums of the artists in the data base
        4 - to extract tracks from the albums in the database
        5 - to extract popularity, album title and album spotify id of the tracks in the database
        
        h, help - for help
        q - to quit''')

def cli_manager(auth):
    while True:
        selection: str = input()

        match selection:
                case 'q':
                    return None
                case 'h' | 'help':
                    cli_help()
                case '0':
                    print(f"total artists: {len(dao_get_all_artists())}")
                    print(f"total albums: {len(dao_get_all_albums())}")
                    print(f"total tracks: {len(dao_get_all_tracks())}")
                case '1':
                    parallel_extract_artists(auth, QUERY, MAX_RESULTS, RESULTS_PER_PAGE)
                case '2':
                    rappers_list = extract_rappers()
                    write_rappers_file(rappers_list)
                case '3':
                    rappers_list = read_rappers()
                    parallel_extract_artist_by_id(auth, rappers_list)
                case '4':
                    parallel_extract_albums(auth, MAX_RESULTS, RESULTS_PER_PAGE)
                case '5':
                    extract_tracks_by_albums(auth)
                case '6':
                    extract_several_tracks_info(auth)
                case 'all':
                    for artist in dao_get_all_artists():
                        print(artist.name)
                case 'check':
                    for rapper in dao_get_all_artists():
                        if rapper.name not in read_rappers():
                            print(rapper.name, rapper.spotify_id)
                case _:
                    print("Invalid input. Please try again.")