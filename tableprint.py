#!/usr/bin/env python3


# TablePrint module (self-made), copied here for convenience.
class TablePrint:
    # 2017-04-06: Allow stdout to be specified during init, so doesn't
    # need to be set all the time.
    def __init__(self, space_out=10, stdout=True):
        """
        Prints data in a visually friendly way.

        :param space_out: The number of spaces to be printed to separate each value
                          passed to the `tableprint` function. The length of each
                          value will be minused from this number, for even spacing.
        :param stdout: Should the output go to stdout? If true, the output will be printed.
                       If false, output will be returned to you (and will need to be captured).
        """
        self._space_out = int(space_out)
        self._stdout = stdout

    def tableprint(self, *data, is_header=False):
        """
        Create a table row.

        :param data: The data you want to be converted. An array can be passed if needed.
        :param is_header: Is the input a header? If set to True, and stdout is also True,
                          a line row separator will be printed after the headers are printed.
        :return: Nothing if stdout is true, the formatted table row if stdout is False.
        """

        # TODO: Make is_header more useful when stdout=False

        if type(data[0]) == list: data = data[0]
        res = ""
        for value in data:
            value = str(value)

            # Chop down value if too big.
            if len(value) >= self._space_out:
                value = value[ : self._space_out - 4]
                value += "..."

            res += value
            res += " " * (self._space_out - len(value))

        if self._stdout:
            print(res)
        else:
            return res

        # 2017-02-14: Removed 'headerprint' and integrated into 'tableprint'
        # through is_header kwarg.
        if is_header:
            print("-" * len(res))

        return