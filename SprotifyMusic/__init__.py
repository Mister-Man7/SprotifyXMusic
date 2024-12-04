from SprotifyMusic.core.bot import SprotifyBot
from SprotifyMusic.core.dir import dirr
from SprotifyMusic.core.git import git
from SprotifyMusic.core.userbot import Userbot
from SprotifyMusic.misc import dbb, heroku, sudo
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
app = SprotifyBot()

# Assistant Client
userbot = Userbot()

from .platforms import PlaTForms

Platform = PlaTForms()

HELPABLE = {}
