import logging
from git import Repo
from config.getconfig import getConfig
from pagesController import createPage

CONFIG = getConfig()

def get_latest_release():
    try:
        repo = Repo(search_parent_directories=True)
        latest_release = repo.tags[-1].name
        return latest_release
    except Exception as e:
        logging.error(f"Error fetching latest Git release: {e}")
        return None

def publishGitRelease(login, password, parentPageID=None):
    latest_release = get_latest_release()

    if latest_release:
        release_info = f"Latest Git Release: {latest_release}"

        # Create or update Confluence page with Git release information
        createPage(title="Git Release Page",
                   content=release_info,
                   parentPageID=parentPageID,
                   login=login,
                   password=password)

        logging.info("Git release information published to Confluence.")
    else:
        logging.error("Failed to fetch Git release information. Check logs for details.")
