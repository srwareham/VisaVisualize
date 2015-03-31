import os
import utilities.downloader
import utilities.archiver

"""
Utility for accessing non-python-code resources.
"""

PROJECT_ROOT_PATH = os.path.abspath(__file__ + "/../../")
DATA_FILES_DIRECTORY = os.path.join(PROJECT_ROOT_PATH, "data_files")


class Resource:
    """
    Object that represents the ability to fetch the desired resource

    Check if resource is present, if not download it and return it.
    Modification function is a python function that given the actual opened file, will return a file-like object
    that has been properly modified
    """
    def __init__(self, resource_name, source_url, modification_function=None):
        self.resource_name = resource_name
        self._source_url = source_url
        self._modification_function = modification_function

    def get_local_path(self):
        return os.path.join(DATA_FILES_DIRECTORY, self.resource_name)

    def is_locally_available(self):
        return os.path.isfile(self.get_local_path())

    def _download_me(self):
        """
        with open(self._get_local_path(), "wb") as file_out:
            with utilities.downloader.download_file(self._source_url) as download:
                for line in download.readlines():
                    file_out.write(line)
        """
        return utilities.downloader.simple_download(self._source_url)

    def download_if_necessary(self):
        if not self.is_locally_available():
            print "Downloading \"" + self.resource_name + "\" from: " + self._source_url
            with open(self.get_local_path(), "wb") as file_out:
                downloading = self._download_me()
                processing = downloading
                if self._modification_function is not None:
                    processing = self._modification_function(downloading)
                for line in processing.readlines():
                    file_out.write(line)

    """
    Return the local file, if not present download it. If needs to be modified, modify in place before saving locally
    and returning it.
    """
    def get_file(self):
        """
        Retrieve and return the resource if it is not present on the filesystem. Return if already present
        :return: An open file-like object
        """
        # Ensure the file is present on local filesystem
        # TODO: make sure this is locking and serialized
        self.download_if_necessary()
        try:
            return open(self.get_local_path(), "rb")
        # TODO: add actual exception handling
        except:
            print "CANNOT RETURN " + self.resource_name


resources_definitions = [
    Resource(
        "contributions.csv",
        "https://dl.dropboxusercontent.com/u/28056448/EverythingData/contributions.csv.tar.gz",
        modification_function=utilities.archiver.extract_file_from_tar
    ),
    Resource(
        "county_votes.csv",
        "https://dl.dropboxusercontent.com/u/28056448/EverythingData/county_votes.csv"
    ),
    Resource(
        "zip_code_database.csv",
        "https://dl.dropboxusercontent.com/u/28056448/EverythingData/zip_code_database.csv"
    )
]

_resources = {}
for resource in resources_definitions:
    _resources[resource.resource_name] = resource


def get_resource(resource_name):
    """
    Returns a resource where its state is "guaranteed" to be saved on the local filesystem
    :param resource_name:
    :return:
    """
    if resource_name in _resources:
        resource = _resources[resource_name]
        resource.download_if_necessary()
        return resource
    # TODO: add error handling even though this will never occur
    else:
        print "RESOURCE NOT DEFINED"


# ---------Examples------


def _example_download_plaintext():
    name = "OUR_README.txt"
    url = "https://raw.githubusercontent.com/srwareham/CampaignAdvisor/master/README.md"
    test_resource = Resource(name, url)
    file_in = test_resource.get_file()
    for line in file_in.readlines():
        print line


def _example_download_and_extract_tarball():
    name = "TEST_TARBALL_TO_PLAINTEXT.txt"
    url = "https://dl.dropboxusercontent.com/u/28056448/EverythingData/sources.txt.tar.gz"
    test_resource = Resource(name, url, modification_function=utilities.archiver.extract_file_from_tar)
    with test_resource.get_file() as file_in:
        for line in file_in:
            print line


def _example_of_untar_implementation():
    url = "https://dl.dropboxusercontent.com/u/28056448/EverythingData/sources.txt.tar.gz"
    download = utilities.downloader.simple_download(url)
    unarchived = utilities.archiver.extract_file_from_tar(download)
    for line in unarchived.readlines():
        print line