from googleapiclient.errors import HttpError
import json 
import re
import base64
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
import html2text
import tkinter as tk
from tkinterweb import HtmlFrame # import the HtmlFrame widget

from Mail import Mail
from Mailbox import Mailbox
from Security import Security
from datetime import datetime