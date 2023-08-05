import pickle

from .helper import to_str, to_parts
from pystrct import StructFile


class Inverted():
    """Inverted file for string indexing."""

    def __init__(self, filename, n=601):
        """Set properties.

        Keyword arguments:
            filepath -- path to inverted file
            n -- indexes' list length (default 601)
        """
        try:
            # If file exists, open and load
            dict_file = open(filename + '.dict', 'rb')  # open file
            self.__dict = pickle.load(dict_file)        # load content
            dict_file.close()                           # close file
        except FileNotFoundError:
            # Create new dict, otherwise
            self.__dict = dict()

            # And save in file
            dict_file = open(filename + '.dict', 'wb')  # open file
            pickle.dump(self.__dict, dict_file)         # save content
            dict_file.close()                           # close file

        self.__n = n
        self.__filename = filename
        self.__file = StructFile(filename + '.inv', str(self.__n) + 'i')

    @property
    def n_keys(self):
        return self.__n - 1

    def insert(self, key, value):
        """Insert a value for a key.

        Keyword arguments:
            key -- key in dict
            value -- key's value
        """
        i = self.__dict.setdefault(key, self.__file.length)

        # Check if list does not exist
        if i == self.__file.length:
            values = [value]
            values += [-1] * self.n_keys

            self.__file.append(values)
        else:
            vals, pos = self.__get(i)

            # Get elements from last list
            j = len(vals) // self.n_keys
            j = j * self.n_keys

            values = vals[j:]

            # If there is no element...
            if len(values) == 0:
                # It means that values are full
                i = self.__file.length              # get file length
                values = vals[-self.n_keys:]        # get last list
                values.append(i)                    # save file index as last element
                self.__save(pos[-1], values)        # save last list
                values = [value]                    # create a new list to save value
                self.__save(i, values)              # save value on last index
            # There is element and it's not full
            else:
                values.append(value)                # append value
                values = values.sort()              # sort values
                self.__save(pos[-1], values)        # save on list position

    def __get(self, i):
        """Get values from ith element in file.

        Return a tuple as (<values>, <file positions>).

        Keyword argument:
            i -- ith element
        """
        values = self.__file.get(i)                         # get values from file
        values = list(filter(lambda x: x > -1, values))     # clear values
        all_values = list()                                 # empty list to save all values
        positions = [i]                                     # list of positions

        while len(values) == self.__n:
            all_values += values[:-1]                           # save values
            positions.append(values[-1])                        # save position

            i = positions[-1]                                   # get last position
            values = self.__file.get(i)                         # get values from file
            values = list(filter(lambda x: x > -1, values))     # clear values

        all_values += values                                    # save last values

        # Return values and positions
        return all_values, positions

    def get(self, key):
        """Get list of values from key.

        Keyword argument:
            key -- dict's key
        """
        # If key is string, it can be a partial string
        if type(key) is str:
            # Clear string to match key
            key = to_parts(key)
        elif type(key) is not list:
            # Just force key to be a list
            key = [key]

        # To save values
        values = list()

        # For each key found...
        for k in key:
            try:
                i = self.__dict[k]          # get file position
                vals, _ = self.__get(i)     # get values

                if type(values) is list:
                    values = set(vals)
                else:
                    values = values.intersection(vals)  # concat values
            except KeyError:
                return list()                           # key dos not exist

        # Return values
        return list(values)

    def update(self, old, new):
        """Update a key label.

        Keyword arguments:
            old -- old key
            new -- new key
        """
        i = self.__dict[old]
        self.__dict[new] = i

        del self.__dict[old]

    def delete(self, key, value):
        """Delete all values from a key.

        Keyword arguments:
            key -- key to be deleted
        """
        n_keys = self.n_keys
        i = self.__dict[key]            # get position in file

        vals, pos = self.__get(i)

        try:
            j = vals.index(value)         # get value index
            del vals[j]                   # delete value

            for i in range(len(pos) - 1):
                p = pos[i]
                l = i * self.n_keys
                values = vals[l:l + self.n_keys]
                values.append(pos[i + 1])
                self.__save(p, values)

            # Get elements from last list
            j = len(vals) // self.n_keys
            j = j * self.n_keys

            values = vals[j:]
            self.__save(pos[-1], values)
        except ValueError:
            pass

    def __save(self, i, values):
        """Prepare data and save on-disk.

        Keyword arguments:
            i -- position in file
            values -- list of values to be saved
        """
        values += [-1] * (self.__n - len(values))   # fill with -1
        self.__file.write(i, values)                # save on-disk

    def __repr__(self):
        """Class representation string."""
        return "{}({}, {})".format(self.__class__.__name__,
                                   self.__filename,
                                   self.__n)

    def __str__(self):
        """Return a str(dict) of self.dict."""
        return str(self.__dict)

    def __del__(self):
        file = open(self.__filename + '.dict', 'wb')  # open file
        pickle.dump(self.__dict, file)                # save content
        file.close()                                  # close file


