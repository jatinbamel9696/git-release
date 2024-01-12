import argparse
import logging
from config.getconfig import getConfig
from pagesController import searchPages, deletePages
from pagesPublisher import publishGitRelease, publishFolder

logging.basicConfig(level=logging.INFO)

# Parse arguments with LOGIN and PASSWORD for Confluence
parser = argparse.ArgumentParser()
parser.add_argument('--login', help='Login with "" is mandatory', required=True)
parser.add_argument('--password', help='Password with "" is mandatory', required=True)
args = parser.parse_args()
inputArguments = vars(args)

CONFIG = getConfig()

logging.debug(CONFIG)

# Search for existing pages with the specified search pattern
pages = searchPages(login=inputArguments['login'], password=inputArguments['password'])

# Delete existing pages to ensure a clean slate
deletePages(pagesIDList=pages, login=inputArguments['login'], password=inputArguments['password'])

# Publish Git release information to Confluence
publishGitRelease(login=inputArguments['login'], password=inputArguments['password'])

# Publish pages from the specified folder
publishFolder(folder=str(CONFIG["github_folder_with_md_files"]),
              login=inputArguments['login'],
              password=inputArguments['password'])
