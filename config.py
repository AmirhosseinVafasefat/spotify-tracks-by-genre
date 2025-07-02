GENRE_QUERY = "Iranian Rap" #query for music genre 

MAX_RESULTS = 1000 #1000 is the maximum amount the spotify api allows
RESULTS_PER_PAGE = 50 #50 is the maximum amount the spotify api allows

MAX_RETIRES = 3 #number of retiries for each api request 
RETRY_BACKOFF = 3 #seconds to wait for retrying

DB_NAME = "Iranian_Rap.db" #databasename

LOG_FILE = "logs.log" #log file name
LOG_DEBUG = True #True if debugging

N_JOBS = 1 #number of cores used for sending requests (caution: more cores may result in overwhelming the api server)

N_SEVERAL_ALBUMS = 20 #maximum is 20

N_SEVERAL_TRACKS = 50 #maximum is 50

