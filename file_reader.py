import re

def extract_rappers() -> list:
    with open('html_rappers.txt', encoding="utf-8") as f:
        rappers = []
        for line in f:
            matches = re.search(r"<.*?>(.+?)<.*?href=\"artistprofile.cgi\?id=(.*?)\".*?>", line)
            if matches:
                rapper = {
                    "name": matches.group(1).strip(),
                    "spotify_id": matches.group(2).strip()
                }
                rappers.append(rapper)
    return rappers

def write_rappers_file(rappers_list: list) -> None:
    cleaned_list = []
    for rapper in rappers_list:
        entry = rapper["name"] + ", " + rapper["spotify_id"] 
        if entry not in cleaned_list:
            cleaned_list.append(entry)

    with open('rappers.txt', 'w', encoding="utf-8") as f:
        for rapper in cleaned_list:
            f.write(rapper + '\n')

def read_rappers() -> list:
    with open('rappers.txt') as f:
        rappers = []
        for line in f:
            name, spotify_id = line.split(", ")
            rappers.append({"name": name, "spotify_id":spotify_id.strip()})
    return rappers
