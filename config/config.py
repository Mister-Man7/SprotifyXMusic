import re
import sys
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# Get it from my.telegram.org
API_ID = int(getenv("API_ID", ""))
API_HASH = getenv("API_HASH")

## Get it from @Botfather in Telegram.
BOT_TOKEN = getenv("BOT_TOKEN")

# Get it from https://openai.com
OPENAI_API_KEY = getenv("OPENAI_API_KEY", "")

# You can paste your cookies to https://batbin.me, save them, and get a link to paste here
COOKIE_LINK = getenv("COOKIE_LINK", None)

# Database to save your chats and stats... Get MongoDB:-  https://telegra.ph/How-To-get-Mongodb-URI-04-06
MONGO_DB_URI = getenv("MONGO_DB_URI", None)

# Clan mode for voice chats. If you want to enable this feature, set it to True.
CLEANMODE_DELETE_MINS = int(
    getenv("CLEANMODE_MINS", "5")
)  # Remember to give value in Seconds

# Custom max audio(music) duration for voice chat. set DURATION_LIMIT in variables with your own time(mins), Default to 60 mins.
DURATION_LIMIT_MIN = int(
    getenv("DURATION_LIMIT", "3200")
)  # Remember to give value in Minutes

# Enable / Disable external plugins
EXTRA_PLUGINS = getenv("EXTRA_PLUGINS", "True")

# Fill True if you want to load extra plugins from external repo
EXTRA_PLUGINS_REPO = getenv(
    "EXTRA_PLUGINS_REPO",
    "https://github.com/Mister-Man7/SprotifyXMusic-Plugin",
)

# Fill here the external plugins repo where plugins that you want to load
EXTRA_PLUGINS_FOLDER = getenv("EXTRA_PLUGINS_FOLDER", "plugins")
# Your folder name in your extra plugins repo where all plugins stored


# Duration Limit for downloading Songs in MP3 or MP4 format from bot
SONG_DOWNLOAD_DURATION = int(
    getenv("SONG_DOWNLOAD_DURATION_LIMIT", "900")
)  # Remember to give value in Minutes

# You'll need a Private Group ID for this.
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", ""))

# Your User ID.
OWNER_ID = list(
    map(int, getenv("OWNER_ID", "1854441420").split())
)  # Input type must be interger

# make your bots privacy from telegra.ph and put your url here

PRIVACY_LINK = getenv(
    "PRIVACY_LINK",
    "https://telegra.ph/Privacy-Policy-for-SprotifyXMusic-11-29",
)

# Get it from http://dashboard.heroku.com/account
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

# You have to Enter the app name which you gave to identify your  Music Bot in Heroku.
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")

# For customized or modified Repository
UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO", "https://github.com/Mister-Man7/SprotifyXMusic"
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")

# GIT TOKEN ( if your edited repo is private)
GIT_TOKEN = getenv("GIT_TOKEN", "")

# Only  Links formats are  accepted for this Var value.
SUPPORT_CHANNEL = getenv(
    "SUPPORT_CHANNEL", "https://t.me/SprotifyNewws"
)  # Example:- https://t.me/cinewinx
SUPPORT_GROUP = getenv(
    "SUPPORT_GROUP", "https://t.me/datarantinggi"
)  # Example:- https://t.me/cinewinxcoments

# Set it in True if you want to leave your assistant after a certain amount of time. [Set time via AUTO_LEAVE_ASSISTANT_TIME]
AUTO_LEAVING_ASSISTANT = getenv("AUTO_LEAVING_ASSISTANT", False)

# Time after which you're assistant account will leave chats automatically.
AUTO_LEAVE_ASSISTANT_TIME = int(
    getenv("ASSISTANT_LEAVE_TIME", 5800)
)  # Remember to give value in Seconds

# Set it true if you want your bot to be private only [You'll need to allow CHAT_ID via /authorize command then only your bot will play music in that chat.]
PRIVATE_BOT_MODE = getenv("PRIVATE_BOT_MODE", "False")

# Time sleep duration For Youtube Downloader
YOUTUBE_DOWNLOAD_EDIT_SLEEP = int(getenv("YOUTUBE_EDIT_SLEEP", "3"))

# Time sleep duration For Telegram Downloader
TELEGRAM_DOWNLOAD_EDIT_SLEEP = int(getenv("TELEGRAM_EDIT_SLEEP", "5"))

# Your Github Repo.. Will be shown on /start Command
GITHUB_REPO = getenv(
    "GITHUB_REPO", "https://github.com/Mister-Man7/SprotifyXMusic"
)

# Spotify Client.. Get it from https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "530a978df3084f8b916e3f512a8c8bb1")
SPOTIFY_CLIENT_SECRET = getenv(
    "SPOTIFY_CLIENT_SECRET", "8a82bc47253a43beac406e0618297132"
)

# Maximum number of video calls allowed on bot. You can later set it via /set_video_limit on telegram
VIDEO_STREAM_LIMIT = int(getenv("VIDEO_STREAM_LIMIT", "999"))

# Maximum Limit Allowed for users to save playlists on bot's server
SERVER_PLAYLIST_LIMIT = int(getenv("SERVER_PLAYLIST_LIMIT", "25"))

# MaximuM limit for fetching playlist's track from youtube, spotify, apple links.
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "25"))

# Telegram audio  and video file size limit

TG_AUDIO_FILESIZE_LIMIT = int(
    getenv("TG_AUDIO_FILESIZE_LIMIT", "4294967296")
)  # Remember to give value in bytes

TG_VIDEO_FILESIZE_LIMIT = int(
    getenv("TG_VIDEO_FILESIZE_LIMIT", "4294967296")
)  # Remember to give value in bytes

# Chceckout https://www.gbmb.org/mb-to-bytes  for converting mb to bytes


# If you want your bot to setup the commands automatically in the bot's menu set it to true.
# Refer to https://i.postimg.cc/Bbg3LQTG/image.png
SET_CMDS = getenv("SET_CMDS", "False")

# You'll need a Pyrogram String Session for these vars. Generate String from our session generator bot @WinxStringBot
STRING_SESSIONS = list(map(str.strip, getenv("STRING_SESSIONS", None).split(",")))

# TOKEN_DATA = getenv("TOKEN_DATA", None)


### DONT TOUCH or EDIT codes after this line
BANNED_USERS = filters.user()
YTDOWNLOADER = 1

LOG = 2
LOG_FILE_NAME = "sprotifylogs.txt"
TEMP_DB_FOLDER = "tempdb"
PREFIXES = ["/", "!", "%", ",", ".", "@", "#"]

adminlist = {}
lyrical = {}
chatstats = {}
userstats = {}
clean = {}

autoclean = []

# Images

START_IMG_URL = getenv(
    "START_IMG_URL",
    "https://graph.org/file/afe0bf9e6b4fede3afc0e.jpg",
    # This is the file id of the photo you can also put the url of photo
)

PING_IMG_URL = getenv(
    "PING_IMG_URL",
    "https://graph.org/file/8f6de108a54be6506b693.jpg",
)

PLAYLIST_IMG_URL = getenv(
    "PLAYLIST_IMG_URL",
    "https://graph.org/file/94074fd8f348807833802.jpg",
)

GLOBAL_IMG_URL = getenv(
    "GLOBAL_IMG_URL",
    "https://raw.githubusercontent.com/gabrielmaialva33/winx-music-bot/refs/heads/master/assets/global_stats_img.png",
)

STATS_IMG_URL = getenv(
    "STATS_IMG_URL",
    "https://raw.githubusercontent.com/gabrielmaialva33/winx-music-bot/refs/heads/master/assets/stats_img.png",
)

TELEGRAM_AUDIO_URL = getenv(
    "TELEGRAM_AUDIO_URL",
    "https://graph.org/file/f626eb194b025672eea28.jpg",
)

TELEGRAM_VIDEO_URL = getenv(
    "TELEGRAM_VIDEO_URL",
    "https://graph.org/file/f6e977e0046a5b8d17904.jpg",
)

STREAM_IMG_URL = getenv(
    "STREAM_IMG_URL",
    "https://graph.org/file/7247dcb0ae280ba3b8492.jpg",
)

SOUNCLOUD_IMG_URL = getenv(
    "SOUNCLOUD_IMG_URL",
    "https://graph.org/file/199a1bd803d3e8c8d0e43.jpg",
)

YOUTUBE_IMG_URL = getenv(
    "YOUTUBE_IMG_URL",
    "https://graph.org/file/d902a638d7bcb6653d36f.jpg",
)

SPOTIFY_ARTIST_IMG_URL = getenv(
    "SPOTIFY_ARTIST_IMG_URL",
    "https://graph.org/file/dc9eb455f86f845f400f8.jpg",
)

SPOTIFY_ALBUM_IMG_URL = getenv(
    "SPOTIFY_ALBUM_IMG_URL",
    "https://graph.org/file/aacfa8762c016077b7ee9.jpg",
)

SPOTIFY_PLAYLIST_IMG_URL = getenv(
    "SPOTIFY_PLAYLIST_IMG_URL",
    "https://graph.org/file/480dbdc265670e833d763.jpg",
)


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


def seconds_to_time(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes:02d}:{remaining_seconds:02d}"


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))
SONG_DOWNLOAD_DURATION_LIMIT = int(time_to_seconds(f"{SONG_DOWNLOAD_DURATION}:00"))

if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        print(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )
        sys.exit()

if SUPPORT_GROUP:
    if not re.match("(?:http|https)://", SUPPORT_GROUP):
        print(
            "[ERROR] - Your SUPPORT_GROUP url is wrong. Please ensure that it starts with https://"
        )
        sys.exit()

if UPSTREAM_REPO:
    if not re.match("(?:http|https)://", UPSTREAM_REPO):
        print(
            "[ERROR] - Your UPSTREAM_REPO url is wrong. Please ensure that it starts with https://"
        )
        sys.exit()

if GITHUB_REPO:
    if not re.match("(?:http|https)://", GITHUB_REPO):
        print(
            "[ERROR] - Your GITHUB_REPO url is wrong. Please ensure that it starts with https://"
        )
        sys.exit()

if PING_IMG_URL:
    if (
        PING_IMG_URL
        != "https://raw.githubusercontent.com/gabrielmaialva33/winx-music-bot/refs/heads/master/assets/ping_img.png"
    ):
        if not re.match("(?:http|https)://", PING_IMG_URL):
            print(
                "[ERROR] - Your PING_IMG_URL url is wrong. Please ensure that it starts with https://"
            )
            sys.exit()

if PLAYLIST_IMG_URL:
    if (
        PLAYLIST_IMG_URL
        != "https://raw.githubusercontent.com/gabrielmaialva33/winx-music-bot/refs/heads/master/assets/playlist_img.png"
    ):
        if not re.match("(?:http|https)://", PLAYLIST_IMG_URL):
            print(
                "[ERROR] - Your PLAYLIST_IMG_URL url is wrong. Please ensure that it starts with https://"
            )
            sys.exit()

if GLOBAL_IMG_URL:
    if (
        GLOBAL_IMG_URL
        != "https://raw.githubusercontent.com/gabrielmaialva33/winx-music-bot/refs/heads/master/assets/global_stats_img.png"
    ):
        if not re.match("(?:http|https)://", GLOBAL_IMG_URL):
            print(
                "[ERROR] - Your GLOBAL_IMG_URL url is wrong. Please ensure that it starts with https://"
            )
            sys.exit()

if STATS_IMG_URL:
    if (
        STATS_IMG_URL
        != "https://raw.githubusercontent.com/gabrielmaialva33/winx-music-bot/refs/heads/master/assets/stats_img.png"
    ):
        if not re.match("(?:http|https)://", STATS_IMG_URL):
            print(
                "[ERROR] - Your STATS_IMG_URL url is wrong. Please ensure that it starts with https://"
            )
            sys.exit()

if TELEGRAM_AUDIO_URL:
    if (
        TELEGRAM_AUDIO_URL
        != "https://raw.githubusercontent.com/gabrielmaialva33/winx-music-bot/refs/heads/master/assets/telegram_audio_img.png"
    ):
        if not re.match("(?:http|https)://", TELEGRAM_AUDIO_URL):
            print(
                "[ERROR] - Your TELEGRAM_AUDIO_URL url is wrong. Please ensure that it starts with https://"
            )
            sys.exit()

if STREAM_IMG_URL:
    if (
        STREAM_IMG_URL
        != "https://raw.githubusercontent.com/gabrielmaialva33/winx-music-bot/refs/heads/master/assets/stream_img.png"
    ):
        if not re.match("(?:http|https)://", STREAM_IMG_URL):
            print(
                "[ERROR] - Your STREAM_IMG_URL url is wrong. Please ensure that it starts with https://"
            )
            sys.exit()

if SOUNCLOUD_IMG_URL:
    if (
        SOUNCLOUD_IMG_URL
        != "https://raw.githubusercontent.com/gabrielmaialva33/winx-music-bot/refs/heads/master/assets/soundcloud_img.png"
    ):
        if not re.match("(?:http|https)://", SOUNCLOUD_IMG_URL):
            print(
                "[ERROR] - Your SOUNCLOUD_IMG_URL url is wrong. Please ensure that it starts with https://"
            )
            sys.exit()

if YOUTUBE_IMG_URL:
    if (
        YOUTUBE_IMG_URL
        != "https://raw.githubusercontent.com/gabrielmaialva33/winx-music-bot/refs/heads/master/assets/youtube_img.png"
    ):
        if not re.match("(?:http|https)://", YOUTUBE_IMG_URL):
            print(
                "[ERROR] - Your YOUTUBE_IMG_URL url is wrong. Please ensure that it starts with https://"
            )
            sys.exit()

if TELEGRAM_VIDEO_URL:
    if (
        TELEGRAM_VIDEO_URL
        != "https://raw.githubusercontent.com/gabrielmaialva33/winx-music-bot/refs/heads/master/assets/telegram_video_img.png"
    ):
        if not re.match("(?:http|https)://", TELEGRAM_VIDEO_URL):
            print(
                "[ERROR] - Your TELEGRAM_VIDEO_URL url is wrong. Please ensure that it starts with https://"
            )
            sys.exit()
