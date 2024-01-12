import json
import logging
import requests
from urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPBasicAuth
from config.getconfig import getConfig

CONFIG = getConfig()

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def searchPages(login, password):
    # make call using Confluence query language
    url = f"{CONFIG['confluence_url']}search?cql=parent={CONFIG['counfluence_parent_page_id']}+and+text~{{\"{CONFIG['confluence_search_pattern']}\"}}+and+type=page+and+space=\"{CONFIG['confluence_space']}\"&limit=1000"

    logging.debug("Calling URL: " + url)

    response = requests.get(
        url=url,
        auth=HTTPBasicAuth(login, password),
        verify=False
    )

    logging.debug(response.status_code)
    
    try:
        results = json.loads(response.text)
        logging.debug(json.dumps(results, indent=4, sort_keys=True))
    except json.decoder.JSONDecodeError as e:
        logging.warning(f"Error decoding JSON response: {e}")
        results = {}

    # extract page's IDs from response JSON
    foundPages = []

    if "results" in results:
        for result in results['results']:
            foundPages.append(result['content']['id'])  # add found page id
            logging.info("Found page: " + result['content']['id'] + " with title: " + result['content']['title'])

    logging.debug("Found pages in space " + str(CONFIG["confluence_space"]) + " and parent page: " +
                  str(CONFIG["counfluence_parent_page_id"]) + " and search text: " +
                  str(CONFIG["confluence_search_pattern"]) + ": " + str(foundPages))

    return foundPages
