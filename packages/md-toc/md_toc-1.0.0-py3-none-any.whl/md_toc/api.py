#
# api.py
#
# Copyright (C) 2017-2018 frnmst (Franco Masotti) <franco.masotti@live.com>
#                                            <franco.masotti@student.unife.it>
#
# This file is part of md-toc.
#
# md-toc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# md-toc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with md-toc.  If not, see <http://www.gnu.org/licenses/>.
#
"""The main file."""

import fpyutils
import re
import curses.ascii


def write_string_on_file_between_markers(filename, string, marker):
    r"""Write the table of contents.

    :parameter filename: the file that needs to be read or modified.
    :parameter string: the string that will be written on the file.
    :parameter marker: a marker that will identify the start
         and the end of the string.
    :type filename: str
    :type string: str
    :type marker: str
    :returns: None
    :rtype: None
    :raises: one of the fpyutils exceptions or one of the built-in exceptions.

    :Example:

    ::

        >>> import md_toc
        >>> f = open('foo.md')
        >>> print(f.read(),end='')
        ## Hi

        [](TOC)

        hey

        ### How are you?           !!!

        fine, thanks

        # Bye
        >>> md_toc.write_string_on_file_between_markers('fake_md.md','Hallo \
        how are you?\nVery well thanks...\n\nGoodbye\n\n\nFarewell\n', \
        '[](TOC)')
        >>> print(f.read(),end='')
        ## Hi

        [](TOC)

        Hallo how are you?
        Very well thanks...

        Goodbye


        Farewell

        [](TOC)

        hey

        ### How are you?           !!!

        fine, thanks

        # Bye
    """
    assert isinstance(string, str)
    assert isinstance(marker, str)

    final_string = marker + '\n\n' + string.rstrip() + '\n\n' + marker + '\n'
    marker_line_positions = fpyutils.get_line_matches(
        filename, marker, 2, loose_matching=True)

    if 1 in marker_line_positions:
        if 2 in marker_line_positions:
            fpyutils.remove_line_interval(filename, marker_line_positions[1],
                                          marker_line_positions[2], filename)
        else:
            fpyutils.remove_line_interval(filename, marker_line_positions[1],
                                          marker_line_positions[1], filename)
        # See fpyutils for the reason of the -1 here.
        fpyutils.insert_string_at_line(filename, final_string,
                                       marker_line_positions[1] - 1, filename)


def build_toc(filename,
              ordered=False,
              no_links=False,
              max_header_levels=3,
              anchor_type='standard'):
    r"""Parse file by line and build the table of contents.

    :parameter filename: the file that needs to be read.
    :parameter ordered: decides whether to build an ordered list or not.
    :parameter no_links: disables the use of links.
    :parameter max_header_levels: the maximum level of headers to be
         considered as such when building the table of contents. Defaults to
         ``3``.
    :parameter anchor_type: decides rules on how to generate anchor links.
         Defaults to ``standard``.
    :type filename: str
    :type ordered: bool
    :type no_links: bool
    :type max_header_levels: int
    :type anchor_type: str
    :returns: the corresponding table of contents.
    :rtype: str
    :raises: one of the built-in exceptions.

    :Example:

    ::

        >>> import md_toc
        >>> f = open('foo.md')
        >>> print(f.read(),end='')
        ## Hi

        hey

        ### How are you?           !!!

        fine, thanks

        # Bye
        >>> print(md_toc.build_toc('foo.md',anchor_type='gitlab'),end='')
            - [Hi](#hi)
                - [How are you?           !!!](#how-are-you)
        - [Bye](#bye)
    """
    assert isinstance(filename, str)

    # Base cases.
    header_type_counter = dict()
    header_type_curr = 0
    header_type_prev = 0
    toc = ''
    header_duplicate_counter = dict()

    with open(filename, 'r') as f:
        line = f.readline()
        while line:
            header = get_md_header(line, header_duplicate_counter,
                                   max_header_levels, anchor_type)
            if header is not None:
                header_type_curr = header['type']
                increase_index_ordered_list(header_type_counter,
                                            header_type_prev, header_type_curr)
                toc += build_toc_line(
                    header,
                    ordered,
                    no_links,
                    index=header_type_counter[header_type_curr]) + '\n'
                header_type_prev = header_type_curr
            line = f.readline()

    return toc


def increase_index_ordered_list(header_type_count, header_type_prev,
                                header_type_curr):
    r"""Compute the current index for ordered list table of contents.

    :parameter header_type_count: the count of each header type.
    :parameter header_type_prev: the previous type of header (h[1-Inf]).
    :parameter header_type_curr: the current type of header (h[1-Inf]).
    :type header_type_count: dict
    :type header_type_prev: int
    :type header_type_curr: int
    :returns: None
    :rtype: None
    :raises: one of the built in exceptions

    :Example:

    >>> ht = {1: 0, 2: 0, 3: 0}
    >>> md_toc.increase_index_ordered_list(ht,3,3)
    >>> ht
    {1: 0, 2: 0, 3: 1}
    """
    assert isinstance(header_type_count, dict)
    assert isinstance(header_type_prev, int)
    assert isinstance(header_type_curr, int)
    # header_type_prev might be 0 while header_type_curr can't.
    assert header_type_curr > 0

    # Base cases for a new table of contents or a new index type.
    if header_type_prev is 0:
        header_type_prev = header_type_curr
    if header_type_curr not in header_type_count:
        header_type_count[header_type_curr] = 0

    header_type_count[header_type_curr] += 1


def build_toc_line(header, ordered=False, no_links=False, index=1):
    r"""Return a list element of the table of contents.

    :parameter header: a data structure that contains the original
         text, the slugified text and the type of header.
    :parameter ordered: if set to ``True``, numbers will be used
         as list ids or otherwise a dash character, otherwise. Defaults
         to ``False``.
    :parameter no_links: disables the use of links.
    :parameter index: a number that will be used as list id in case of an
         ordered table of contents. Defaults to ``1``.
    :type header: dict
    :type ordered: bool
    :type no_links: bool
    :type index: int
    :returns: a single line of the table of contents.
    :rtype: str
    :raises: one of the built-in exceptions.

    :Example:

    >>> header =  {'type': 2, 'text_original': 'hi hOw Are YOu!!? ? #', 'text_anchor_link': 'hi-how-are-you'}
    >>> print(md_toc.build_toc_line(header,ordered=True,index=3))
        3. [hi hOw Are YOu!!? ? #](#hi-how-are-you)
    """
    assert isinstance(header, dict)
    assert 'type' in header
    assert 'text_original' in header
    assert 'text_anchor_link' in header
    assert isinstance(header['type'], int)
    assert isinstance(header['text_original'], str)
    assert isinstance(header['text_anchor_link'], str)
    assert header['type'] > 0
    assert isinstance(ordered, bool)
    assert isinstance(no_links, bool)
    assert isinstance(index, int)

    if ordered:
        list_symbol = str(index) + '.'
    else:
        list_symbol = '-'

    # Ordered list require 4-level indentation,
    # while unordered either 2 or 4. Common case is 4.
    no_of_indentation_spaces = 4 * (header['type'] - 1)
    indentation_spaces = no_of_indentation_spaces * ' '

    if no_links:
        line = header['text_original']
    else:
        line = '[' + header['text_original'] + ']' + '(#' + header['text_anchor_link'] + ')'

    toc_line = indentation_spaces + list_symbol + ' ' + line

    return toc_line


def build_anchor_link(header_text_trimmed,
                      header_duplicate_counter,
                      anchor_type='standard'):
    r"""Apply the specified slug rule to build the anchor link.

    :parameter header_text_trimmed: the text that needs to be transformed in a link
    :parameter header_duplicate_counter: a data structure that keeps track of
         possible duplicate header links in order to avoid them. This is
         meaningful only for certain values of anchor_type.
    :parameter anchor_type: decides rules on how to generate anchor links.
         Defaults to ``standard``. Supported anchor types are: ``standard``,
         ``github``, ``gitlab``, ``redcarpet``.
    :type header_text_trimmed: str
    :type header_duplicate_counter: dict
    :type anchor_type: str
    :returns: None if the specified anchor type is not recognized, or the
         anchor link, otherwise.
    :rtype: str
    :raises: one of the built-in exceptions.

    :note: For a detailed description of the behaviour of each anchor type
        and for the licenses of each markdown parser algorithm, please refer to
        the 'Markdown spec' documentation page.

    :Example:

    >>> print(md_toc.build_anchor_link('   hello ## how # are you ???  ! ',dict(),'gitlab'))
    hello-how-are-you
    """
    assert isinstance(header_text_trimmed, str)
    assert isinstance(header_duplicate_counter, dict)
    assert isinstance(anchor_type, str)

    if anchor_type == 'standard':
        return header_text_trimmed

    elif anchor_type == 'github':
        header_text_trimmed = header_text_trimmed.lower()
        # Remove punctuation: Keep spaces, hypens and "word characters"
        # only.
        header_text_trimmed = re.sub(r'[^\w\s\- ]', '', header_text_trimmed)
        header_text_trimmed = header_text_trimmed.replace(' ', '-')

        # Check for duplicates.
        ht = header_text_trimmed
        # Set the initial value if we are examining the first occurrency.
        # The state of header_duplicate_counter is available to the caller
        # functions.
        if header_text_trimmed not in header_duplicate_counter:
            header_duplicate_counter[header_text_trimmed] = 0
        if header_duplicate_counter[header_text_trimmed] > 0:
            header_text_trimmed = header_text_trimmed + '-' + str(
                header_duplicate_counter[header_text_trimmed])
        header_duplicate_counter[ht] += 1

        return header_text_trimmed

    elif anchor_type == 'gitlab' or anchor_type == 'redcarpet':
        # To ensure full compatibility what follows is a direct translation
        # of the rndr_header_anchor C function used in redcarpet.
        STRIPPED = " -&+$,/:;=?@\"#{}|^~[]`\\*()%.!'"
        header_text_trimmed_len = len(header_text_trimmed)
        inserted = 0
        stripped = 0
        header_text_trimmed_middle_stage = ''
        for i in range(0, header_text_trimmed_len):
            if header_text_trimmed[i] == '<':
                while i < header_text_trimmed_len and header_text_trimmed[i] != '>':
                    i += 1
            elif header_text_trimmed[i] == '&':
                while i < header_text_trimmed_len and header_text_trimmed[i] != ';':
                    i += 1
            # str.find() == -1 if character is not found in str.
            # https://docs.python.org/3.6/library/stdtypes.html?highlight=find#str.find
            elif not curses.ascii.isascii(
                    header_text_trimmed[i]) or STRIPPED.find(
                        header_text_trimmed[i]) != -1:
                if inserted and not stripped:
                    header_text_trimmed_middle_stage += '-'
                stripped = 1
            else:
                header_text_trimmed_middle_stage += header_text_trimmed[
                    i].lower()
                stripped = 0
                inserted += 1

        if stripped > 0 and inserted > 0:
            header_text_trimmed_middle_stage = header_text_trimmed_middle_stage[
                0:-1]

        if inserted == 0 and header_text_trimmed_len > 0:
            hash = 5381
            for i in range(0, header_text_trimmed_len):
                # Get the unicode representation with ord.
                # Unicode should be equal to ASCII in ASCII's range of
                # characters.
                hash = ((hash << 5) + hash) + ord(header_text_trimmed[i])

            # This is equivalent to %x in C. In Python we don't have
            # the length problem so %x is equal to %lx in this case.
            # Apparently there is no %l in Python...
            header_text_trimmed_middle_stage = 'part-' + '{0:x}'.format(hash)

        # Check for duplicates (this is working in github only).
        # https://gitlab.com/help/user/markdown.md#header-ids-and-links
        if anchor_type == 'gitlab':
            # Apparently redcarpet does not handle duplicate entries, but
            # Gitlab does, although I cannot find the code responsable for it.
            ht = header_text_trimmed_middle_stage
            if header_text_trimmed_middle_stage not in header_duplicate_counter:
                header_duplicate_counter[header_text_trimmed_middle_stage] = 0
            if header_duplicate_counter[header_text_trimmed_middle_stage] > 0:
                header_text_trimmed_middle_stage = header_text_trimmed_middle_stage + '-' + str(
                    header_duplicate_counter[header_text_trimmed_middle_stage])
            header_duplicate_counter[ht] += 1

        return header_text_trimmed_middle_stage

    else:
        return None


def get_md_header_type(line, max_header_levels=3):
    r"""Given a line extract the title type.

    :parameter line: the line to be examined.
    :parameter max_header_levels: the maximum level of headers to be
         considered as such when building the table of contents. Defaults to ``3``.
    :type line: str
    :type max_header_levels: int
    :returns: None if the line does not contain header elements, or the header
        type, otherwise.
    :rtype: int
    :raises: one of the built in exceptions.

    :warning: the parameter max_header_levels must be greater than 0.

    :Example:

    >>> print(md_toc.get_md_header_type('###  hello ## how # are you ???  ! ',6))
    3
    >>> print(md_toc.get_md_header_type('###  hello ## how # are you ???  ! ',2))
    None
    """
    assert isinstance(line, str)
    assert isinstance(max_header_levels, int)
    assert max_header_levels > 0

    # Remove leading and whitespace from line to engage a lax parsing.
    line = line.lstrip()

    # Determine the header type by counting the number of the
    # first consecutive '#' characters in the line.
    # Count until we are in range of max_header_levels.
    header_type = 0
    line_length = len(line)
    while header_type < line_length and line[header_type] == '#' and header_type <= max_header_levels:
        header_type += 1
    # Ignore not valid or empty headers.
    if header_type == 0 or header_type > max_header_levels or line.lstrip(
            '#') == '':
        return None
    else:
        return header_type


def remove_md_header_syntax(header_text_line):
    r"""Return a trimmed version of the input line without the markdown header syntax.

    :parameter header_text_line: a single markdown line that needs to be
         transformed into a TOC line.
    :type header_text_line: str
    :returns: a trimmed version of the input line without the markdown header
         syntax.
    :rtype: str
    :raises: one of the built-in exceptions.

    :note: this function removes the leading and trailing whitespaces, the first
        consecutive '#' characters and any space left behind after removing those.

    :Example:

    >>> md_toc.remove_md_header_syntax(' ### hello ## how # are you ???  ! ')
    'hello ## how # are you ???  !'
    """
    assert isinstance(header_text_line, str)

    return header_text_line.strip().lstrip('#').lstrip()


def get_md_header(header_text_line,
                  header_duplicate_counter,
                  max_header_levels=3,
                  anchor_type='standard'):
    r"""Build a data structure with the elements needed to create a TOC line.

    :parameter header_text_line: a single markdown line that needs to be
         transformed into a TOC line.
    :parameter header_duplicate_counter: a data structure that contains the
         number of occurrencies of each header anchor link. This is used to
         avoid duplicate anchor links and it is meaningful only for certain
         values of anchor_type.
    :parameter max_header_levels: the maximum level of headers to be
         considered as such when building the table of contents. Defaults to ``3``.
    :parameter anchor_type: decides rules on how to generate anchor links.
         Defaults to ``standard``.
    :type header_text_line: str
    :type header_duplicate_counter: dict
    :type max_header_levels: int
    :type anchor_type: str
    :returns: None if the input line does not correspond to one of the
         designated cases or a data structure containing the necessary
         components to create a table of contents line, otherwise.
    :rtype: dict
    :raises: one of the built-in exceptions.

    :note: this works like a wrapper to other functions.

    :Example:

    >>> print(md_toc.get_md_header(' ## hi hOw Are YOu!!? ? #'))
    {'type': 2, 'text_original': 'hi hOw Are YOu!!? ? #', 'text_anchor_link': 'hi hOw Are YOu!!? ? #'}
    """
    header_type = get_md_header_type(header_text_line, max_header_levels)
    if header_type is None:
        return header_type
    else:
        header_text_trimmed = remove_md_header_syntax(header_text_line)
        header = {
            'type':
            header_type,
            'text_original':
            header_text_trimmed,
            'text_anchor_link':
            build_anchor_link(header_text_trimmed, header_duplicate_counter,
                              anchor_type)
        }
        return header


if __name__ == '__main__':
    pass
