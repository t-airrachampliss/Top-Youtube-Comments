import googleapiclient.discovery
import requests
import pandas as pd
import sqlalchemy as db
from pytube import Channel, YouTube


# class YoutubeComments():
# TODO: figure out what to do with this
app_key = ''


# Returns True if the user's input is NOT a Youtuber
def __is_not_youtuber(youtuber):
    try:
      # Check if the channel is online
      resp = requests.get(f'https://www.youtube.com/c/{youtuber}/videos')
      resp.raise_for_status()
      return False
    except requests.exceptions.HTTPError as err:
      return True  

# Prompts the user to enter the name of a youtuber (no spaces allowed yet)
def get_youtuber():
    print("This program provides a list of all the top comments from every video a Youtuber has made.")
    youtuber = input("Which YouTuber do you want to see a list of comments from?: ")
    try:
        while __is_not_youtuber(youtuber):
            print('Sorry, we cannot find the person you are looking for.')
            youtuber = input("Please re-enter the Youtuber: ")
    except True as e:
        pass
    return youtuber

# Returns the top (most-liked) comment and its author for a video
def __get_top_comment(video):
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = app_key

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part = "snippet",
        videoId = video,
        order = "relevance",
        textFormat = "plainText"
    )

    response = request.execute()
    # Grab the top comment and author from nested data
    top_comment = response['items'][0]['snippet']['topLevelComment']['snippet']['textDisplay']
    author = response['items'][0]['snippet']['topLevelComment']['snippet']['authorDisplayName']
    return (author, top_comment)

# Asks the user how many comments they want to see
# Returns a dictionary of video url links {link: video title}
def __get_urls(youtuber, num):
    # Creates a channel object to scrape the video for link and title
    c = Channel(f'https://www.youtube.com/c/{youtuber}/videos')

    all_urls = {}

    # If the channel doesn't have any videos, return None and trigger follow-up statement
    if len(c.video_urls) == 0:
      return "None"

    # Grab the title and link of every video from youtuber
    # Put {link: title} into all_urls
    for url in c.video_urls:
      yt = YouTube(url)
      yt.title
      all_urls[url] = yt.title
      # Stops adding urls after the number needed has been gathered
      if len(all_urls) == int(num):
        break

    return all_urls

# Prompts the user to select how many comments they want to see (5-40)
def __num_of_comments():
    print("You can choose to see between 5 and 40 comments.")
    num = input('How many comments would you like to see?: ')
    while not (int(num)) or int(num) < 5 or int(num) > 40:
      num = input('Please enter a number between 5 and 40: ')
    return num

# Retrives the video ID by deleting the first part of the link
def __fix_URL(full_url):
    new_url = full_url.split('=')
    return new_url[1]

# Returns all of the top comments from list of videos
# calls _get_urls() to get a list of video urls for channel
# calls _get_top_comment() on each video url to get the top comment
def get_all_comments(youtuber):
    # how many comments does the user want to see?
    num = num_of_comments()

    url_list = __get_urls(youtuber, num)

    # Checks if the youtuber has any videos; program quits if they don't
    if url_list == "None":
      print("That youtuber doesn't have any videos.")
    else:
      # Create a data frame to hold all of the comments data
      comments = pd.DataFrame(columns=["Video-Title", "Author", "Comment"])
      
      # Add the title, author of comment and comment text to comments
      for link in url_list.keys():
        comment = list(__get_top_comment(_fix_URL(link)))
        comments.loc[len(comments.index)] = [url_list.get(link), comment[0], comment[1]]    
    
      # Create and send sql table from the dataframe
      engine = db.create_engine('sqlite:///all_top_comments.db')
      comments.to_sql('all_top_comments', con=engine, if_exists='replace', index=False)
      
      # Return Database Query
      return engine.execute(f"SELECT * FROM all_top_comments;").fetchall()
