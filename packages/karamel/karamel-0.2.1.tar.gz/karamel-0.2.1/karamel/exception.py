class KaramelException(Exception):
    pass

packages_file_not_found_message = \
'''Cannot find the file {}'.format(packages_file_url).
Check if the url or the path is valid and the file exist.
If the package file is online also check your connection to Internet.'''

class PackagesFileNotFound(KaramelException):
    def __init__(self, packages_file):
        message = packages_file_not_found_message.format(packages_file)
        super().__init__(message)
