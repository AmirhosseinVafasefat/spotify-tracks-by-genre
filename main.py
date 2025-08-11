from auth import SpotifyAuthManager
from db import create_tables
from cli import cli_help, cli_manager

def main():
    auth = SpotifyAuthManager()
    
    create_tables()
    
    cli_help()

    cli_manager(auth)
        
if __name__=="__main__":
    main()
