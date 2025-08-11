QUERY = "genre:'persian hip hop'" #query for searching artists

MAX_RESULTS = 1000 #1000 is the maximum amount the spotify api allows
RESULTS_PER_PAGE = 50 #50 is the maximum amount the spotify api allows

MAX_RETRIES = 3 #number of retiries for each api request 
RETRY_BACKOFF = 3 #seconds to wait for retrying

DB_NAME = "Iranian_Rap.db" #databasename

LOG_FILE = "logs.log" #log file name
LOG_DEBUG = True #True if debugging

N_JOBS = -1 #number of cores used for sending requests (caution: more cores may result in overwhelming the api server which can be seen in the log file)

N_SEVERAL_ALBUMS = 20 #batching a number of albums for the api (maximum is 20)

N_SEVERAL_TRACKS = 50 #batching a number of tracks for the api(maximum is 50)

N_SEVERAL_ARTISTS = 50 #batching a number of artists for the api(maximum is 50)
