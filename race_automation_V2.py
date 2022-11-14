import requests
import requests_html
import os
import time
from datetime import date

def main():
    tracks = get_tracks()
    today = date.today()
    start = time.time()
    total_races = 0
    for (track, track_link, day) in tracks:
        
        if day != today.isoformat():
            continue
        races = get_races(track_link, day)

        for race in list(races):
            get_csv(track, race, day)
            total_races += 1
    end = time.time()
    print("Took",int((end-start)),"seconds to export",total_races,"races")
    return

def get_races(track, date):
    try:
        base_path = "https://www.thedogs.com.au"
        track_path = base_path + track
        session = requests_html.HTMLSession()
        r = session.get(track_path)
        #r.html.render(sleep=5, timeout=8)
        for item in r.html.xpath("/html/body/div[1]/div[1]/div[1]/div"):
            return(item.links)
    except:
        return None

def get_csv(track, race_url, date):

    try:
        #extract race name
        contents = race_url.split("/")
        track = contents[2]
        race = contents[5]
        
        #Creats a path for the csv that exists in a Sheets/"date" folder
        path = os.path.realpath(__file__)
        main, script = os.path.split(path)
        sheet_path = os.path.join(main,'Sheets')
        date_path = os.path.join(sheet_path, date, track)
        if not os.path.exists(date_path):
            os.makedirs(date_path)
        #this is the link to the csv
        url = "https://www.thedogs.com.au" + race_url + "/export-expert-form?sort_by=&amp;sort_dir=&amp;starts="

        #Load file into memory
        response = requests.get(url)

        filename  = track + "_" + race + '.csv'

        #Write file to directory
        with open(os.path.join(date_path, filename), 'wb') as temp_file:
            temp_file.write(response.content)
    except:
        return
        
def get_tracks():
    base_path = "https://www.thedogs.com.au/racing/racecards"
    session = requests_html.HTMLSession()
    r = session.get(base_path)

    for item in r.html.xpath("/html/body/div[1]/div/div[1]/div[2]"):
        track_links = list(item.links)
    tracks = []
    for i, link in enumerate(track_links):
        if link[1] != "r":
            continue
        else:
            contents = link.split("/")
            date = contents[-1]
            track = contents[2]
            tracks.append((track, link, date))
    return tracks

if __name__ == "__main__":
    main()
