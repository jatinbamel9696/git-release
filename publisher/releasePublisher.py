import logging
from github import Github
from config.getconfig import getConfig
from pagesController import createPage

CONFIG = getConfig()

def get_github_release_info(token, repo_owner, repo_name, release_tag):
    try:
        g = Github(token)
        repo = g.get_repo(f"{repo_owner}/{repo_name}")
        release = repo.get_release(release_tag)
        
        release_info = f"Release Tag: {release.tag_name}\n" \
                       f"Release Name: {release.title}\n" \
                       f"Release Notes:\n{release.body}"

        return release_info
    except Exception as e:
        logging.error(f"Error fetching GitHub release information: {e}")
        return None

def publishGitHubReleaseToConfluence(login, password, repo_owner, repo_name, release_tag, parentPageID=None):
    github_token = CONFIG.get("github_token")
    
    if not github_token:
        logging.error("GitHub token not provided. Please add it to your config.yaml.")
        return

    release_info = get_github_release_info(github_token, repo_owner, repo_name, release_tag)

    if release_info:
        createPage(title=f"GitHub Release: {release_tag}",
                   content=release_info,
                   parentPageID=parentPageID,
                   login=login,
                   password=password)

        logging.info("GitHub release information published to Confluence.")
    else:
        logging.error("Failed to fetch GitHub release information. Check logs for details.")
