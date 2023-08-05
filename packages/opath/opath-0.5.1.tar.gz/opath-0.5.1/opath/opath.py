"""
Object encapsulation of directory/file trees
"""

import glob
import json
import os
from copy import deepcopy
from pathlib import Path

from . import utils
from .objchain import ObjChain, ChainList

#TODO: touch with hidden file that indicates a managed directory or file


class OPath(ObjChain):
    """ A generic path """

    def __init__(self, name, push_up=True, check_attr=True):
        """
<<<<<<< HEAD:magicdir/magic_dir.py
        Initializer for MagicPath
=======
        Initializer for OPath
>>>>>>> refactoring:opath/opath.py

        :param name: basename of the path
        :type name: str
        :param push_up: default of whether to 'push' access of this path to the root path node
        :type push_up: boolean
        :param check_attr: default to validate attributes. For example 'this is not valid' is not a valid
                            attribute since it contains spaces but 'this_is_a_valid_attribute' is a valid attribute.
        :type check_attr: boolean
        """
        super().__init__(push_up=push_up, check_attr=check_attr)
        self.name = name
        self._parent_dir = ''

    @property
    def dir(self):
        """ The parent directory of this location"""
        return str(self.root._parent_dir)

    @property
    def relpath(self):
        """ Relative path of this location """
        return Path(*self.ancestors(include_self=True).name)

    @property
    def path(self):
        """ Path of this location"""
        return Path(str(self.dir), *self.ancestors(include_self=True).name)

    @property
    def abspath(self):
        """ Absolute path of this location """
        return self.path.absolute()

    def set_dir(self, path):
        """ Set the parent directory """
        self.root._parent_dir = str(path)
        return path

    def remove_parent(self):
        """ Remove parent from this path """
        new_parent = self.abspath.parent
        self._parent_dir = new_parent
        return super().remove_parent()

    def __repr__(self):
        return "<{}(\"{}\")>".format(self.__class__.__name__, self.name, self.relpath)

    def print(self, print_files=False, indent=4, max_level=None, level=0, list_missing=True):
        print(self.show(print_files=print_files, indent=indent,
                        max_level=max_level, level=0, list_missing=True))

    def show(self, print_files=False, indent=4, max_level=None, level=0, list_missing=True):
        """
        Recursively print the file structure

        :param print_files: whether to print files
        :type print_files: boolean
        :param indent: number of spaces per indent
        :type indent: int
        :param max_level: max level depth to print
        :type max_level: int
        :param level: start at level
        :type level: int
        :param list_missing: whether to annotate files that do not exist
        :type list_missing: boolean
        :return: None
        :rtype: None
        """
        padding = '|   ' * level
        name = self.name
        if self.attr and name != self.attr:
            name += " (\"{}\")".format(self.attr)
        missing_tag = ''
        if list_missing and not self.exists():
            missing_tag = "*"
        s = "{padding}{missing}{name}".format(missing=missing_tag, padding=padding, name=name)
        s += '\n'
        level += 1
        for name, child in self._children.items():
            s += child.show(print_files, indent, max_level, level, list_missing)
        return s


class OFile(OPath):
    """ A file object """

    def write(self, data, mode='w', **kwargs):
        """ Write data to a file """
        return self.parent.write_file(self.name, mode, data, **kwargs)

    def read(self, mode='r', **kwargs):
        """ Read data from a file """
        return self.parent.read_file(self.name, mode, **kwargs)

    def open(self, mode='r', **kwargs):
        """ Opens a file for reading or writing """
        return self.parent.open_file(self.name, mode, **kwargs)

    def dump_json(self, data, mode='w', **json_kwargs):
        """Dump data as a json"""
        return self.parent.dump_json(self.name, mode, data, **json_kwargs)

    def load_json(self, mode='r', **json_kwargs):
        """Load data from json"""
        return self.parent.load_json(self.name, mode, **json_kwargs)

    def exists(self):
        """ Whether the file exists """
        return Path(self.abspath).is_file()

    def rm(self):
        """ Removes file if it exists. """
        if self.exists():
            os.remove(str(self.abspath))


class ODir(OPath):
    """ A directory object """

    # TODO: this doesn't take into account files not in descendents
    @property
    def files(self):
        """
        Recursively returns all files :class:`OFile` of this directory. Does not include parent directories.

        :return: list of OFiles
        :rtype: list
        """
        desc = self.descendents(include_self=True)
        return ChainList([d for d in desc if isinstance(d, OFile)])

    @property
    def dirs(self):
        """
        Recursively returns all directories :class:`ODir` of this directory. Does not include parent directories.

        :return: list of ODir
        :rtype: list
        """
        desc = self.descendents(include_self=True)
        return ChainList([d for d in desc if isinstance(d, ODir)])

    def list_dirs(self):
        """List immediate directories in this directory"""
        return ChainList([c for c in self.children if isinstance(c, ODir)])

    def list_files(self):
        """List immediate files in this directory"""
        return ChainList([c for c in self.children if isinstance(c, OFile)])

    @property
    def relpaths(self):
        """
        Returns all paths to all directories (includes parent_dir).

        :return: directory paths in this directory (inclusive)
        :rtype: list of PosixPath
        """
        return self.dirs.relpath

    @property
    def paths(self):
        """
        Returns all paths to all directories (includes parent_dir).

        :return: directory paths in this directory (inclusive)
        :rtype: list of PosixPath
        """
        return self.dirs.path

    @property
    def abspaths(self):
        """
        Returns all absolute paths to all directories (includes parent_dir).

        :return: directory absolute paths in this directory (inclusive)
        :rtype: list of PosixPath
        """
        return self.paths.absolute()

    def all_exists(self):
        """
        Whether all directories in the tree exist.

        :return: directory tree exists
        :rtype: boolean
        """
        return all(self.abspaths.is_dir())

    def mkdirs(self):
        """
         Creates all directories in the directory tree. Existing directories are ignored.

        :return: self
        :rtype: ODir
        """
        for p in self.abspaths:
            utils.makedirs(p, exist_ok=True)
        return self

    def rmdirs(self):
        """
         Recursively removes all files and directories of this directory (inclusive)

        :return: self
        :rtype: ODir
        """
        if self.abspath.is_dir():
            utils.rmtree(self.abspath)
        return self

    def cpdirs(self, new_parent):
        """
        Copies the directory tree to a new location. Returns the root of the newly copied tree.

        :param new_parent: path of new parent directory
        :type new_parent: basestring or PosixPath or Path object
        :return: copied directory
        :rtype: ODir
        """
        utils.copytree(self.abspath, Path(new_parent, self.name))
        copied_dirs = deepcopy(self)
        copied_dirs.remove_parent()
        copied_dirs.set_dir(new_parent)
        return copied_dirs

    def mvdirs(self, new_parent):
        """ Moves the directory. If this directory has a parent connection, the connection will be broken and this
        directory will become a root directory. The original root will be left in place but will no longer have
        access to the moved directories. """
        oldpath = self.abspath
        self.remove_parent()
        if self.exists():
            utils.copytree(oldpath, Path(new_parent, self.name))
        self.set_dir(new_parent)
        if self.exists():
            utils.rmtree(oldpath)
        return self

    def exists(self):
        """ Whether the directory exists """
        return self.abspath.is_dir()

    def ls(self):
        """ Lists the files that exist in directory """
        return utils.listdir(self.abspath)

    def glob(self, pattern):
        return glob.glob(str(Path(self.abspath, pattern)))

    # def collect(self):
    #     """ collects new directories that exist on the local machine and add to tree """

    def _get_if_exists(self, name, attr):
        if self.has(attr):
            c = self.get(attr)
            if hasattr(c, 'name') and c.name == name:
                return c

    def _validate_add(self, name, attr, expected_type, blacklisted_names):
        e = self._get_if_exists(name, attr)
        if e and issubclass(e.__class__, expected_type):
            return e
        if name in blacklisted_names:
            raise AttributeError(
                "{} name \"{}\" already exists for {}. Existing dirnames: {}".format(
                    expected_type.__name__, name, self, ', '.join(blacklisted_names)))

    # TODO: exist_ok kwarg
    def add(self, name, attr=None, push_up=None, check_attr=None):
        """
        Adds a new directory to the directory tree.

        :param name: name of the new directory
        :type name: basestring
        :param attr: attribute to use to access this directory. Defaults to name.
        :type attr: basestring
        :param push_up: whether to 'push' attribute to the root, where it can be accessed
        :type push_up: boolean
        :param check_attr: if True, will raise exception if attr is not a valid attribute. If None, value will
        default to defaults defined on initialization
        :type check_attr: boolean|None
        :return: new directory
        :rtype: ODir
        """
        if attr is None:
            attr = name
        existing = self._validate_add(name, attr, ODir, self.children.name)
        if existing:
            return existing
        return self._create_and_add_child(attr, with_attributes={"name": name}, push_up=push_up, check_attr=check_attr)

    def add_file(self, name, attr=None, push_up=None, check_attr=False):
        """
        Adds a new file to the directory tree.

        :param name: name of the new file
        :type name: basestring
        :param attr: attribute to use to access this directory. Defaults to name.
        :type attr: basestring
        :param push_up: whether to 'push' attribute to the root, where it can be accessed
        :type push_up: boolean
        :param check_attr: if True, will raise exception if attr is not a valid attribute. If None, value will
        default to defaults defined on initialization
        :type check_attr: boolean|None
        :return: new directory
        :rtype: ODir
        """
        if attr is None:
            attr = name
        existing = self._validate_add(name, attr, OFile, self.files.name)
        if existing:
            return existing
        file = OFile(name)
        self._add(attr, file, push_up=push_up, check_attr=check_attr)
        return file

    def write_file(self, filename, mode, data, **kwargs):
        """ Write  a file at this location """
        utils.makedirs(self.abspath)
        with self.open_file(str(Path(self.abspath, filename)), mode, **kwargs) as f:
            f.write(data)

    def read_file(self, filename, mode, **kwargs):
        """ Read a file at this location """
        with self.open_file(str(Path(self.abspath, filename)), mode, **kwargs) as f:
            return f.read()

    def open_file(self, filename, mode, **kwargs):
        """ Open a file at this location """
        utils.makedirs(self.abspath)
        return utils.fopen(str(Path(self.abspath, filename)), mode, **kwargs)

    def dump_json(self, filename, mode, data, *args, **json_kwargs):
        """Dump data to json"""
        utils.makedirs(self.abspath)
        with self.open_file(str(Path(self.abspath, filename)), mode) as f:
            json.dump(data, f, *args, **json_kwargs)

    def load_json(self, filename, mode, **kwargs):
        """Load data from a json"""
        with self.open_file(str(Path(self.abspath, filename)), mode, **kwargs) as f:
            return json.load(f)
