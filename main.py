import requests
import site_headers
from bs4 import BeautifulSoup
import os

site_home = "https://soundcloudtool.com/"
post_url = "https://soundcloudtool.com/soundcloud-downloader-tool"


def main():
    session = requests.Session()
    
    #link = get_download_link(session)
    #download_from_link(session, link)

    song_links = open("songLinks.txt").readlines()
    for song_link in (song_links):
        song_link = song_link.replace("\n", "")
        link = get_download_link(song_link, session)
        download_from_link(song_link, session, link)

        print(f"{song_link} Downloaded")
    
def download_from_link(song_link, conn, link):
    response = conn.get(link, stream=True)

    if(response.status_code == 200):
        newstr = song_link[song_link.find("soundcloud.com/")+1:]
        filename = newstr[newstr.find("/")+1:] + ".mp3"
        filename = filename.replace("/", "_")
        filename = "songs/" + filename

        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

def get_download_link(song_link, conn):
    middle_token = get_middle_token(conn)

    post_json = {
        "csrfmiddlewaretoken": middle_token,
        "soundcloud": song_link
    }

    song_page = conn.post(post_url, data=post_json, headers=site_headers.post)
    print(song_page.status_code)

    soup = BeautifulSoup(song_page.text, "html.parser")
    linkElement = soup.find('a', {'id': 'trackLink'})

    return linkElement.get('href')


def get_middle_token(conn: requests.Session) -> str:
    a = conn.get(site_home, headers=site_headers.get)

    page = a.text
    soup = BeautifulSoup(page, "html.parser")
    input_field = soup.find('input', {'name': 'csrfmiddlewaretoken'})

    if(input_field):
        return input_field.get('value')
    else:
        print("Failed to get token")
        exit(1)

if __name__ == "__main__":
    main()