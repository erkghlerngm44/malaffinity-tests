import sys
import io


class TablePrint:
    def __init__(self, fn=None, space_out=10):
        """
        Prints data in a visually-friendly way.

        :param fn: Path of file to write data to. Specify `None` to use stdout.
        :param space_out: The number of spaces to be printed to separate each value
                          passed to the `tableprint` function. The length of each
                          value will be minused from this number, for even spacing.
        """

        if fn:
            # Ask for the filename instead of the file object, so we're not
            # dealing with messy objects being referenced in multiple places,
            # leading to dodgy stuff happening.
            self._fp = open(fn, "w")
        else:
            # Default to stdout if no fp specified.
            self._fp = sys.stdout

        self._space_out = space_out

    def write_row(self, *data, is_header=False):
        """
        Create a table row.

        :param data: The data. An array can be passed if needed.
        :param is_header: Is the input a header? Print a series of "-"s after
                          the data to create a line row separator
        :return: Nothing.
        """

        # See if file has been closed. If so, we can't write to it.
        if self._fp.closed:
            # TODO: Check I'm doing this right
            raise IOError("fp has been closed. Please create another instance "
                          "of this class to perform table functions")

        # Array support.
        # Yes, `*[]` could be passed but this is more convenient.
        if isinstance(data[0], list): data = data[0]

        space_out = self._space_out
        result = ""

        for value in data:
            value = str(value)

            # Chop down if too big.
            # Avoid saving `len(value)` to a var because it might need chopping soon.
            if len(value) >= space_out:
                value = value[: space_out - 4]
                value += "..."

            value_len = len(value)

            result += value
            result += " " * (space_out - value_len)

        self._fp.write("{}\n".format(result))

        if is_header:
            sep = "-" * len(result)
            self._fp.write("{}\n".format(sep))

        return

    def close(self):
        """
        Close the file.
        Don't bother with this if fp is set to `sys.stdout`.

        Delete the instance of this class, or completely ignore it after
        you call this function. It's useless after this is run.

        :return: Nothing.
        """

        # Only actually close it if `self._fp` is a file object.
        # We don't want to close `sys.stdout` for obvious reasons.
        if isinstance(self._fp, io.IOBase):
            self._fp.close()

        return
