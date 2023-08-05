from struct import Struct


class StructFile():
    """Represent a set of structs from a binary file.

    Propeties:
        size -- file's size
        tell -- current index
        length -- number of structs in file
    """

    def __init__(self, filepath, fmt):
        """Open file in binary mode and set properties.

        Keyword arguments:
            filepath -- absolute/relative path of the file to be read
            fmt -- format of file's struct
        """
        self.__filepath = filepath
        self.__strct = Struct(fmt)           # file's data structure

        # Open file
        try:
            file = open(filepath, 'rb+')
        except FileNotFoundError:
            file = open(filepath, 'wb+')
        finally:
            self.__file = file
            self.__file.seek(0)                  # begin of file

    @property
    def size(self):
        """Calculate and return the file size in bytes."""
        old = self.__file.tell()        # old position

        self.__file.seek(0, 2)          # end of file
        n_bytes = self.__file.tell()    # file size in bytes

        self.__file.seek(old)           # back to old position

        return n_bytes                  # return size

    @property
    def tell(self):
        """Return dataset current index."""
        return self.__file.tell() // self.__strct.size

    @property
    def length(self):
        """Return the number of structs in file."""
        return self.size // self.__strct.size

    def next(self, n=1):
        """Get the next n data from file*.

        Keyword argument:
            n -- number of structs to be retrieved (default 1)
                 Must be greater than 0.

        Return:
            A data in the format of obj_fmt, if n = 1. A list of
            structs, otherwise.

        *This method changes file.tell value.
        """
        # Get the next n elements
        return self.get(self.tell, n)

    def prev(self, n=1):
        """Get the previous n data from file.

        Keyword argument:
            n -- number of structs to be retrieved (default 1)
                 Must be greater than 0.

        Return:
            A data in the format of obj_fmt, if n = 1. A list of
            structs, otherwise.
        """
        # Current position - #data
        i = abs(self.tell - n)

        # Get the next n data starting from i
        return self.get(i, n)

    def get(self, i, n=1):
        """Get the n data starting from the ith.

        Keyword argument:
            i -- position in file
            n -- number of structs to be retrieved (default 1)
                 Must be greater than 0.

        Return:
            A data in the format of obj_fmt, if n = 1. A list of
            structs, otherwise.

        *This method changes file.tell value.
        """
        # If there is nothing to get...
        if self.size == 0:
            return None

        if n < 1:
            return []

        # Current byte position - (n * data_size)
        offset = i * self.__strct.size

        # Set file pointer to -(#data)
        self.__file.seek(offset)

        # Unpack raw data to struct
        data = map(lambda x: self.unpack(x), self.raw(n))
        data = map(lambda x: x if len(x) > 1 else x[0], data)
        data = list(data)

        # If n is 1, return a single unpacked data.
        # Otherwise, return a list of unpacked data
        return data[0] if n == 1 else data

    def last(self):
        """Get the last object in file."""
        # End of file
        self.__file.seek(0, 2)

        # Get the last struct
        data = self.get(self.length - 1)

        return data

    def raw(self, n=1):
        """Get the data from file*.

        Keyword argument:
            n -- number of data to be retrieved (default 1).
                 Must be greater than 0.

        Return:
            A list of raw data.

        *This method changes file.tell value.
        """
        size = self.__strct.size  # struct size
        dataset = list()          # list of raw data

        try:
            # For n times...
            for _ in range(n):
                data = self.__file.read(size)  # get raw data from file
                dataset.append(data)           # save raw data in the list
        finally:
            return dataset

    def unpack(self, raw_data):
        """Unpack data and return a formated object.

        Keyword argument:
            raw_data -- data to be unpacked
        """
        # Unpack
        data = self.__strct.unpack(raw_data)

        return data

    def pack(self, value):
        """Pack the data according to format and return a binary string.

        Keyword arguments:
            value -- value to be packed
        """
        return self.__strct.pack(*value)

    def append(self, value):
        """Write the value into the file.

        Keyword arguments:
            value -- value to be writen (tuple)
        """
        # Pack value
        data = self.pack(value)

        # End of file
        self.__file.seek(0, 2)

        # Write packed value
        self.__file.write(data)

    def write(self, i, value):
        """Write value in ith position in file.

        Keyword arguments:
            i -- position in file
            value -- value to be packed (tuple)
        """
        # Current byte position - (n * data_size)
        offset = i * self.__strct.size

        # Set file pointer to -(#data)
        self.__file.seek(offset)

        # Pack value
        data = self.pack(value)

        # Write packed value
        self.__file.write(data)

    def truncate(self, n):
        """Erase data to [size] bytes.

        Keyword arguments:
            size -- how much data should be removed in bytes.
                    When (default None), the file is erased until the end.
        """
        # Current byte position - (n * data_size)
        size = self.size - n * self.__strct.size

        # Erase [size] bytes from file.tell()
        self.__file.truncate(size)

    def __repr__(self):
        """Class representation string."""
        return "{}({}, {})".format(self.__class__.__name__,
                                   self.__filepath,
                                   self.__strct.format)

    def __str__(self):
        """Return a str(list) of data."""
        old = self.__file.tell()            # save old position
        dataset = self.get(0, self.length)  # get all

        self.__file.seek(old)    # back to old position
        return str(dataset)      # return the list's string representation

    def __del__(self):
        """Close file right before object is deleted."""
        self.__file.close()
