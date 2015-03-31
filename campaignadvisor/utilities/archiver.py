__author__ = 'srwareham'
__all__ = ['extract_file_from_tar', 'extract_file_from_tar']

"""
Utility for managing archives

"""

from zipfile import ZipFile
import tarfile


def extract_file_from_zip(f, desired_file=None):
    """
    Extracts desired file from zip file.

    If no desired file is specified, the first file in the archive will be returned.

    :param f: File-like object referencing a zip file
    :param desired_file: (optional) The name of the file to be extracted
    :return: A file-like object of the desired file
    """

    zip_file = ZipFile(f)
    if desired_file is None:
        desired_file = zip_file.filelist[0]
    return zip_file.open(desired_file)


def _get_first_file(tar_file):
    for member in tar_file.getmembers():
        if member.isfile():
            return member
    return None


def extract_file_from_tar(f, desired_file=None):
    """
    Extracts desired file from a (compressed) tar archive.

    Supports extracting from uncompressed tars as well as those compressed with gzip or bzip2

    If no file is specified, the first file in the tar will be extracted.
    Symlinks, directories, etc. will be ignored.

    If no file is found, tarfile.ReadError is raised

    :param f: The file-like object referencing a tar file
    :param desired_file: (optional) The name of the file to be extracted
    :return: A file-like object of the desired file
    """
    tar_file = tarfile.open(fileobj=f, mode="r:*")
    if desired_file is None:
        tar_info = _get_first_file(tar_file)
    else:
        tar_info = tar_file.getmember(desired_file)
    if tar_info is None:
        raise tarfile.ReadError
    return tar_file.extractfile(tar_info)
