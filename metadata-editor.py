#!/usr/bin/python
# encoding: utf-8

import socket
from bs4 import BeautifulSoup
import sys
from selenium import webdriver
import time
import os
import os.path
from termcolor import colored
from tqdm import tqdm
import requests
import shutil


# [All Information Recover]
# l_file_path
# l_file_name
# l_file_artist_name
# l_file_track_name
# l_web_page
# l_track_link
# l_track_web_page
# l_track_number
# l_track_position
# l_tracks_name
# l_track_artist

# ERROR Code
# error 1 : get_internet_status
# error 2 : get_file_status
# error 3 : get_file_name
# error 4 : get_file_artist_name
# error 5 : get_file_track_name
# error 6 : get_web_page
# error 7 : get_track_link
# error 8 : get_track_link
# error 9 : get_track_web_page
# error 10 : get_track_number
# error 11 : get_tracks_name
# error 12 : get_track_position
# error 13 : get_track_name
# error 14 : get_album_artist
# error 15 : get_cover_link
# error 16 : get_album_genre
# error 17 : get_album_name
# error 18 : get_album_release_date
# error 19 : get_album_copyright
# error 20 : get_cover


def get_internet_status():
    try:
        socket.create_connection(("music.apple.com", 80))
        internet_status = colored("True", 'green')
        print("[debug] Internet connection: [{}]".format(internet_status))
    except OSError:
        internet_status = colored("False", 'red')
        print("[debug] Internet connection: [{}]".format(internet_status))
        error_text = colored("ERROR 1: internet connection is required.", 'red')
        print(error_text + "\n ")
        os.system('pause')
        sys.exit()


def get_file_status(file_path):
    if not os.path.exists(file_path):
        error_text = colored("ERROR 2: unable to find file.", 'red')
        tips_error = colored("Try to remove the quotes from the path.", 'yellow')
        print(error_text)
        print(tips_error + "\n ")
        os.system('pause')
        sys.exit()


def get_file_name(file_name):
    try:
        file_name = file_name.split("\\")
        file_name = "{}".format(file_name[-1])
        if ".mp3" in file_name:
            file_name = file_name.replace(".mp3", "")
        if file_name == "":
            sys.exit()
        if not "-" in file_name:
            sys.exit()
        return file_name
    except:
        error_text = colored("ERROR 3: the requested file cannot be found or is incompatible.", 'red')
        print(error_text + "\n ")
        os.system('pause')
        sys.exit()


def get_file_artist_name(file_name):
    try:
        file_artist_name = file_name.split('-')[0]
        file_artist_name = file_artist_name.strip()
        if file_artist_name == "":
            sys.exit()
        return file_artist_name
    except:
        error_text = colored("ERROR 4: the file name is incompatible. Respect the writing: artist - track name", 'red')
        print(error_text + "\n ")
        os.system('pause')
        sys.exit()


def get_file_track_name(file_name):
    try:
        file_track_name = file_name.split('-')[1]
        file_track_name = file_track_name.strip()
        if file_track_name == "":
            sys.exit()
        return file_track_name
    except:
        error_text = colored("ERROR 5 : the file name is incompatible. Respect the writing: artist - track name", 'red')
        print(error_text + "\n ")
        os.system('pause')
        sys.exit()


def get_web_page(file_artist_name, file_track_name):
    try:
        # [Browser settings]
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--verbose')
        # browser = webdriver.Chrome(executable_path=path_to_web_driver, options=chrome_options)
        browser = webdriver.Chrome(options=chrome_options)
        browser.get("https://music.apple.com/us/search?searchIn=am&term={} - {}".format(file_artist_name, file_track_name))

        # [Source code recovery]
        loading_finished = False
        while not loading_finished:
            source1 = browser.page_source
            time.sleep(2)
            if source1 == browser.page_source:
                loading_finished = True
        # browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # time.sleep(0.5)
        # for x in browser.find_elements_by_xpath("//*[@id=\"ember29\"]/div/nav/ul/li[1]/button"):
        #     webdriver.ActionChains(browser).move_to_element(x).click(x).perform()
        web_page = browser.page_source
        v_search_url = colored("{}".format(browser.current_url), 'blue')
        print("[debug] Search url: [{}]".format(v_search_url))
        browser.quit()
        if web_page == "":
            sys.exit()
        return web_page
    except:
        error_text = colored("ERROR 6 : a problem occurred while retrieving the web page.", 'red')
        tips_error = colored("Check that the chromedriver version corresponds to the google chrome version.", 'yellow')
        print(error_text)
        print(tips_error + "\n ")
        os.system('pause')
        sys.exit()


def get_track_link(web_page, file_name):
    try:
        # definition of values
        file_name = file_name.lower()

        # data for word search
        word_list = file_name.split()
        # number_word_list = len(word_list)

        # data for character search
        character_list = [c for c in file_name]
        # number_character_list = len(character_list)

        # track list data
        if "No results for" in web_page:
            print("ERROR 7 : no result found. Check the name of the title or the artist.")
            sys.exit()
        tracks_name = BeautifulSoup(web_page, "html.parser")
        tracks_name = tracks_name.findAll("div", attrs={"class": u"list-lockup typography-label song linkable search-swoosh ember-view"})
        track_list_data = []
        for x in tracks_name:
            track_list_data.append(str(x.get_text()).strip().split("\n")[0].lower())

        # word search script
        results_list = []
        for d in track_list_data:
            p = 0
            for w in word_list:
                if w in d:
                    p += 1
            results_list.append(p)
        if results_list == []:
            sys.exit()

        selected_track = max(results_list)
        track_position = results_list.index(selected_track)
        word_number_track_selected = len(track_list_data[track_position].split())

        if selected_track == word_number_track_selected:
            pass
        else:
            # character search script
            results_list.clear()
            for d in track_list_data:
                p = 0
                for w in character_list:
                    if w in d:
                        p += 1
                results_list.append(p)

            selected_track = max(results_list)
            track_position = results_list.index(selected_track)

        track_link = "{}".format(tracks_name[track_position]).split('actionUrl":"https://music.apple.com/')[1].split('"}')[0]
        track_link = "https://music.apple.com/{}".format(track_link)
        if "?i=" in track_link:
            track_link = track_link.split("?i=")[0]
        # if "/us/" in track_link:
        #     track_link = track_link.replace('/us/', '/fr/')
        return track_link
    except:
        error_text = colored("ERROR 8 : internet connection too slow. Try Again.", 'yellow')
        print(error_text + "\n ")
        os.system('pause')
        sys.exit()


def get_track_web_page(track_link):
    try:
        track_web_page = requests.get(track_link)
        track_web_page = BeautifulSoup(track_web_page.text, "html.parser")
        return track_web_page
    except:
        error_text = colored("ERROR 9 : an error has occurred.", 'red')
        print(error_text + "\n ")
        os.system('pause')
        sys.exit()


def get_track_number(track_web_page):
    try:
        track_number = track_web_page.findAll("div", attrs={"class": u"song-wrapper"})
        track_number = len(track_number)
        return track_number
    except:
        error_text = colored("ERROR 10 : an error has occurred.", 'red')
        print(error_text + "\n ")
        os.system('pause')
        sys.exit()


def get_tracks_name(track_web_page):
    try:
        search_result = track_web_page.findAll("div", attrs={"class": u"song-wrapper"})
        tracks_name = []
        for x in search_result:
            tracks_name.append(str(x.get_text()).strip().lower())
        return tracks_name
    except:
        error_text = colored("ERROR 11 : an error has occurred.", 'red')
        print(error_text + "\n ")
        os.system('pause')
        sys.exit()


def get_track_position(track_list_data, file_track_name):
    try:
        # definition of values
        file_name = file_track_name.lower()

        # data for word search
        word_list = file_name.split()

        # data for character search
        character_list = [c for c in file_name]

        # word search script
        results_list = []
        for d in track_list_data:
            p = 0
            for w in word_list:
                if w in d:
                    p += 1
            results_list.append(p)

        selected_track = max(results_list)
        track_position = results_list.index(selected_track)
        word_number_track_selected = len(track_list_data[track_position].split())

        if selected_track == word_number_track_selected:
            pass
        else:
            # character search script
            results_list.clear()
            for d in track_list_data:
                p = 0
                for w in character_list:
                    if w in d:
                        p += 1
                results_list.append(p)

            selected_track = max(results_list)
            track_position = results_list.index(selected_track)
        return track_position
    except:
        error_text = colored("ERROR 12 : an error has occurred.", 'red')
        print(error_text + "\n ")
        os.system('pause')
        sys.exit()


def get_track_name(track_web_page, track_position):
    try:
        search_result = track_web_page.findAll("div", attrs={"class": u"song-wrapper"})
        track_name = []
        track_name.append(str(search_result[track_position].get_text()).strip().split("\n")[0])
        track_name = track_name[0]
        return track_name
    except:
        error_text = colored("ERROR 13 : an error has occurred.", 'red')
        print(error_text + "\n ")
        os.system('pause')
        sys.exit()


def get_album_artist(track_web_page):
    try:
        search_result = track_web_page.find("a", attrs={"class": u"dt-link-to"})
        album_artist = search_result.get_text().strip()
        return album_artist
    except:
        error_text = colored("ERROR 14 : an error has occurred.", 'red')
        print(error_text + "\n ")
        os.system('pause')
        sys.exit()

def get_track_artist(track_web_page, track_position, album_artist):
    try:
        search_result = track_web_page.findAll("div", attrs={"class": u"song-wrapper"})
        track_artist = []
        track_artist.append(str(search_result[track_position].get_text()).strip().split("\n")[2])
        track_artist = track_artist[0]
        if track_artist == "":
            track_artist = album_artist
    except:
        track_artist = album_artist
    return track_artist


def get_cover_link(track_web_page):
    try:
        search_result = track_web_page.find("img", attrs={"class": u"media-artwork-v2__image"})
        cover_link = "{}".format(search_result).split(' srcset="https://')[1].split(' 2')[0]
        cover_link = "https://{}".format(cover_link)
        cover_link = cover_link.replace('270x270', '3000x3000')
        return cover_link
    except:
        error_text = colored("ERROR 15 : an error has occurred.", 'red')
        print(error_text + "\n ")
        os.system('pause')
        sys.exit()


def get_album_genre(track_web_page):
    try:
        search_result = track_web_page.find("h3", attrs={"class": u"product-meta typography-footnote-emphasized"})
        album_genre = search_result.get_text().split("·")[0].strip()
        return album_genre
    except:
        error_text = colored("ERROR 16 : an error has occurred.", 'red')
        print(error_text + "\n ")
        os.system('pause')
        sys.exit()


def get_album_name(track_web_page):
    try:
        search_result = track_web_page.find("h1", attrs={"class": u"product-name typography-title-emphasized clamp-4"})
        album_name = search_result.get_text().strip()
        return album_name
    except:
        error_text = colored("ERROR 17 : an error has occurred.", 'red')
        print(error_text + "\n ")
        os.system('pause')
        sys.exit()


def get_album_release_date(track_web_page):
    try:
        search_result = track_web_page.find("h3", attrs={"class": u"product-meta typography-footnote-emphasized"})
        album_release_date = search_result.get_text().split("·")[1].strip()
        return album_release_date
    except:
        error_text = colored("ERROR 18 : an error has occurred.", 'red')
        print(error_text + "\n ")
        os.system('pause')
        sys.exit()


def get_album_copyright(track_web_page):
    try:
        search_result = track_web_page.find("p", attrs={"class": u"song-copyright typography-footnote-emphasized"})
        album_copyright = search_result.get_text().strip()
        return album_copyright
    except:
        error_text = colored("ERROR 19 : an error has occurred.", 'red')
        print(error_text + "\n ")
        os.system('pause')
        sys.exit()


def get_cover(cover_link):
    try:
        if os.path.exists("cover.jpg"):
            os.remove("cover.jpg")
        r = requests.get(cover_link, stream=True)
        # Total size in bytes.
        total_size = int(r.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        t = tqdm(total=total_size, unit='iB', unit_scale=True)
        with open('cover.jpg', 'wb') as f:
            for data in r.iter_content(block_size):
                t.update(len(data))
                f.write(data)
        t.close()
        if total_size != 0 and t.n != total_size:
            sys.exit()
    except:
        error_text = colored("ERROR 20 : an error occurred while downloading.", 'red')
        print(error_text + "\n ")
        os.system('pause')
        sys.exit()


# [PROGRAM]
get_internet_status()
# l_file_path = "D:\Hugo GUILBERT\Wondershare UniConverter\Downloaded\Panda Eyes - Nostalgia 64.mp3"
print("[debug] Paste the file link or drag it into the window")
l_file_path = input("[debug] File path : ")
get_file_status(l_file_path)
print("[debug] File path: [{}]".format(l_file_path))

# file name recovery
l_file_name = get_file_name(l_file_path)
print("[debug] File name: [{}]".format(l_file_name))

# file artist name recovery
l_file_artist_name = get_file_artist_name(l_file_name)
print("[debug] File artist name: [{}]".format(l_file_artist_name))

# file track name recovery
l_file_track_name = get_file_track_name(l_file_name)
print("[debug] File track name: [{}]".format(l_file_track_name))

# web page recovery
l_web_page = get_web_page(l_file_artist_name, l_file_track_name)

# track link retrieval
l_track_link = get_track_link(l_web_page, l_file_track_name)
v_track_link = colored(l_track_link, 'blue')
print("[debug] Track link: [{}]".format(v_track_link))

# track page retrieval
l_track_web_page = get_track_web_page(l_track_link)

# track number retrieval
l_track_number = get_track_number(l_track_web_page)

# retrieving the track code
l_tracks_name = get_tracks_name(l_track_web_page)

# track position retrieval
l_track_position = get_track_position(l_tracks_name, l_file_track_name)

# track name retrieval
l_track_name = get_track_name(l_track_web_page, l_track_position)

# album artist retrieval
l_album_artist = get_album_artist(l_track_web_page)

# track artist retrieval
l_track_artist = get_track_artist(l_track_web_page, l_track_position, l_album_artist)

# cover link retrieval
l_cover_link = get_cover_link(l_track_web_page)

# album genre retrieval
l_album_genre = get_album_genre(l_track_web_page)

# album name retrieval
l_album_name = get_album_name(l_track_web_page)

# albume release date retrieval
l_album_release_date = get_album_release_date(l_track_web_page)

# albume copyright retrieval
l_album_copyright = get_album_copyright(l_track_web_page)


print("[info] Data extraction:")
v_cover_link = colored(l_cover_link, 'cyan')
v_text = colored("Cover link   :", 'yellow')
print("{} {}".format(v_text, v_cover_link))
v_text = colored("Name         :", 'yellow')
print("{} {}".format(v_text, l_track_name))
v_text = colored("Genre        :", 'yellow')
print("{} {}".format(v_text, l_album_genre))
v_text = colored("Album name   :", 'yellow')
print("{} {}".format(v_text, l_album_name))
v_text = colored("Track number :", 'yellow')
print("{} {}/{}".format(v_text, l_track_position + 1, l_track_number))
v_text = colored("Artist       :", 'yellow')
print("{} {}".format(v_text, l_track_artist))
v_text = colored("Album artist :", 'yellow')
print("{} {}".format(v_text, l_album_artist))
v_text = colored("Release date :", 'yellow')
print("{} {}".format(v_text, l_album_release_date))
v_text = colored("Copyright    :", 'yellow')
print("{} {}\n".format(v_text, l_album_copyright))

# cover download
print("Collecting cover")
print("  Downloading {}".format(v_cover_link))
get_cover(l_cover_link)
v_text = colored("Successfully downloaded", 'green')
print("{}".format(v_text))

# metadata editing
if not os.path.exists("Music\{}\{}".format(l_album_artist, l_album_name)):
    os.makedirs("Music\{}\{}".format(l_album_artist, l_album_name))
else:
    if os.path.exists("Music\{}\{}\cover.jpg".format(l_album_artist, l_album_name)):
        os.remove("Music\{}\{}\cover.jpg".format(l_album_artist, l_album_name))
    if os.path.exists("Music\{}\{}\{} - {}.mp3".format(l_album_artist, l_album_name, l_track_position + 1, l_track_name)):
        os.remove("Music\{}\{}\{} - {}.mp3".format(l_album_artist, l_album_name, l_track_position + 1, l_track_name))

os.system('ffmpeg -i "{}" -i "cover.jpg" -metadata comment="Cover (front)" -map 0:0 -map 1:0 -metadata title="{}" -metadata genre="{}" -metadata album="{}" -metadata track="{}/{}" -metadata artist="{}" -metadata album_artist="{}" -metadata date="{}" -metadata copyright="{}" -codec copy -id3v2_version 3 "Music\{}\{}\{} - {}.mp3"'.format(l_file_path, l_track_name, l_album_genre, l_album_name, l_track_position + 1, l_track_number, l_track_artist, l_album_artist, l_album_release_date, l_album_copyright, l_album_artist, l_album_name, l_track_position + 1, l_track_name))
shutil.move("cover.jpg", 'Music\{}\{}'.format(l_album_artist, l_album_name))
v_text = colored("[debug] metadata editing is successfully completed", 'green')
print(v_text + "\n")
os.system('pause')
sys.exit()
