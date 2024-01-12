import logging
import os
import markdown
import re
from git import Repo  # Add the Git import
from config.getconfig import getConfig
from pagesController import createPage, attachFile

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

def publishFolder(folder, login, password, parentPageID=None):
    logging.info("Publishing folder: " + folder)
    for entry in os.scandir(folder):
        if entry.is_dir():
            # create page with the DISPLAY CHILDREN macro for the directories in the folder with MD files
            logging.info("Found directory: " + str(entry.path))
            currentPageID = createPage(title=str(entry.name),
                                       content="<ac:structured-macro ac:name=\"children\" ac:schema-version=\"2\" ac:macro-id=\"80b8c33e-cc87-4987-8f88-dd36ee991b15\"/>",  # name of the DISPLAY CHILDREN macro
                                       parentPageID=parentPageID,
                                       login=login,
                                       password=password)

            # publish files in the current folder
            publishFolder(folder=entry.path, login=login, password=password, parentPageID=currentPageID)

        elif entry.is_file():
            logging.info("Found file: " + str(entry.path))

            if str(entry.path).lower().endswith('.md'):  # check for correct file extension
                newFileContent = ""
                filesToUpload = []
                with open(entry.path, 'r', encoding="utf-8") as mdFile:
                    for line in mdFile:
                        # search for images in each line and ignore http/https image links
                        # Pattern: \A!\[.*]\(.*\)\Z
                        # example: ![test](/data_images/test_image.jpg)

                        result = re.findall("\A!\[.*]\((?!http)(.*)\)", line)

                        if bool(result):  # line contains an image
                            # extract filename from the full path
                            result = str(result).split('\'')[1]  # ['/data_images/test_image.jpg'] => /data_images/test_image.jpg
                            result = str(result).split('/')[-1]  # /data_images/test_image.jpg => test_image.jpg
                            logging.debug("Found file for attaching: " + result)
                            filesToUpload.append(result)
                            # replace line with confluence storage format <ac:image> <ri:attachment ri:filename="test_image.jpg" /></ac:image>
                            newFileContent += "<ac:image> <ri:attachment ri:filename=\"" + result + "\" /></ac:image>"
                        else:  # line without an image
                            newFileContent += line

                    # create new page
                    pageIDforFileAttaching = createPage(title=str(entry.name),
                                                        content=markdown.markdown(newFileContent, extensions=['markdown.extensions.tables', 'fenced_code']),
                                                        parentPageID=parentPageID,
                                                        login=login,
                                                        password=password)

                    # if do exist files to Upload as attachments
                    if bool(filesToUpload):
                        for file in filesToUpload:
                            imagePath = str(CONFIG["github_folder_with_image_files"]) + "/" + file  # full path of uploaded image file
                            if os.path.isfile(imagePath):  # check if the file exists
                                logging.info("Attaching file: " + imagePath + "  to the page: " + str(pageIDforFileAttaching))
                                with open(imagePath, 'rb') as attachedFile:
                                    attachFile(pageIdForFileAttaching=pageIDforFileAttaching,
                                               attachedFile=attachedFile,
                                               login=login,
                                               password=password)
                            else:
                                logging.error("File: " + str(imagePath) + "  not found. Nothing to attach")
            else:
                logging.info("File: " + str(entry.path) + "  is not an MD file. Publishing has rejected")

        elif entry.is_symlink():
            logging.info("Found symlink: " + str(entry.path))

        else:
            logging.info("Found an unknown type of entry (not a file, not a directory, not a symlink): " + str(entry.path))
