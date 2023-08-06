import pathspec
from os import walk, path
import os
import shutil
import yaml


def get_all_files_modified_after_time(dirs, specs, timestamp):
    """
    Gets all the files that are modified after the timestamp and do no match the spec
    :param dirs:
    :param specs:
    :param timestamp:
    :return:
    """
    files = get_included_files(dirs, specs)
    result = set([])
    for f in files:
        modtime = os.stat(f).st_mtime
        if modtime >= timestamp:
            result.add(f)
    return result


def get_included_files(dirs, specs):
    """
    Gets all the files that are included in the given dir
    :param dirs:
    :param specs:
    :return:
    """
    files = get_all_files_in_dirs(dirs)
    for spec in specs:
        spec = pathspec.PathSpec.from_lines(pathspec.GitIgnorePattern, spec.splitlines())

        exclude = set(spec.match_files(files))
        files = files - exclude
    return files


def get_all_files_in_dirs(dirs):
    """
    Gets all the files in the given dirs and subdirs in a set
    :param dirs:
    :return: a set with the files in the dirs and subdirs
    """
    f = []
    for d in dirs:
        for (dirpath, dirnames, filenames) in walk(d):
            f.extend([path.join(dirpath, file) for file in filenames])
    return set(f)


def copy_with_exclusion(dirs, dest, specs, timestamp=0):
    """
    Copies the files in the given directories that are not selected by the specs and are modified after the given timestamp
    :param dirs:
    :param dest:
    :param specs:
    :param timestamp:
    :return:
    """
    files_to_copy = [f for f in get_all_files_modified_after_time(dirs, specs, timestamp)]
    destinations = [dest + path.dirname(f)[1:] for f in files_to_copy]
    for (f, dest) in zip(files_to_copy, destinations):
        if not path.exists(dest):
            os.makedirs(dest, exist_ok=True)
        shutil.copy(f, dest)


def remove_if_exists(dir):
    """
    Removes a directory if it exists
    :param dir: directory to remove
    :return:
    """
    if path.exists(dir):
        shutil.rmtree(dir)


def yaml_file_to_dict(file_ref):
    """
    Loads the settings into a dictionary
    :param file_ref:
    :return:
    """
    settings = None
    with open(file_ref, "r") as f:
        settings = yaml.load(f)
    return settings
