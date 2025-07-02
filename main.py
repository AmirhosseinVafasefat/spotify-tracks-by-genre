from auth import get_token, get_auth_header
from db import create_tables
from dao import dao_get_all_artists,dao_get_all_albums, dao_get_all_tracks
from data_ingestion import parallel_extract_artists, extract_tracks_by_albums, parallel_extract_albums, extract_several_tracks_info
from cli import cli_help

from config import GENRE_QUERY, MAX_RESULTS, RESULTS_PER_PAGE

def main():
    create_tables()

    token: str = get_token()
    headers: str = get_auth_header(token)
    
    cli_help()

    while True:
        selection: str = input()
        match selection:
            case 'q':
                break
            case 'h' | 'help':
                cli_help()
            case '0':
                print("total artists:" + str(len(dao_get_all_artists())))
                print("total albums:" + str(len(dao_get_all_albums())))
                print("total tracks:" + str(len(dao_get_all_tracks())))
            case '1':
                print("Extracting artists.")
                parallel_extract_artists(headers, GENRE_QUERY, MAX_RESULTS, RESULTS_PER_PAGE)
            case '2':
                print("Extracting albums.")
                parallel_extract_albums(headers, MAX_RESULTS, RESULTS_PER_PAGE)
            case '3':
                print("Extracting tracks.")
                extract_tracks_by_albums(headers)
            case '4':
                print("Extracting tracks information.")
                extract_several_tracks_info(headers)
            case 'a':
                for track in dao_get_all_tracks():
                    print(track)
            case _:
                print("Invalid input. Please try again.")

if __name__=="__main__":
    main()
