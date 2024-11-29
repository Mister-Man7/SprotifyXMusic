from SprotifyXMusic.core.bot import WinxBot
from SprotifyXMusic.core.dir import dirr
from SprotifyXMusic.core.git import git
from SprotifyXMusic.core.userbot import Userbot
from SprotifyXMusic.misc import dbb, heroku, sudo
from .core.cookies import save_cookies

from .logging import LOGGER

# Directories
dirr()

# Check Git Updates
git()

# Save cookies in txt
# save_cookies()

# Initialize Memory DB
dbb()

# Heroku APP
heroku()

# Load Sudo Users from DB
sudo()
# Bot Client
app = WinxBot()

# Assistant Client
userbot = Userbot()

from .platforms import PlaTForms

Platform = PlaTForms()

HELPABLE = {}
