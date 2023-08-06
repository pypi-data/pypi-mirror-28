Using CPG
=========

CPG is a command line application and can be run by executing command ``cpg``.
Passing option ``-h`` or ``--help`` to CPG prints basic usage information::

  $ cpg --help
  Usage: cpg [OPTIONS] AUDIO_DIR PLAYLIST_FILE

    [...]

  Options:
    -a, --absolute           Output playlist with absolute paths.
    -c, --config FILENAME    Configuration file path.
    -f, --format [m3u8|pls]  Playlist format.
    -r, --relative           Output playlist with relative paths.
    -h, --help               Show this message and exit.

CPG expects two arguments.  The first argument ``AUDIO_DIR`` is a path to a
directory which will be recursively scanned for audio files.  The second
argument ``PLAYLIST_FILE`` will be used as the path of the generated playlist.

The command line interface supports specifying the output playlist's file
format via options ``-f`` and ``--format``.  Whether the playlist should use
absolute or relative paths can be specified with options ``--absolute`` or
``--relative`` and their respective short options.  By default CPG generates
M3U8 playlists with relative paths.


Configuration File
------------------

CPG's advanced features can only be configured through a configuration file.
Its path can be specified with options ``-c`` and ``--config``.  CPG supports
reading TOML configuration files.  Details about the TOML file format's syntax
can be found in its `README`_.

.. _README: https://github.com/toml-lang/toml/blob/master/README.md

.. code-block:: text

   # Example TOML configuration file for CPG.

   [playlist]
   format = "m3u8"
   paths = "relative"


   [tracks]
   sort = [
     ["tracknumber", "discnumber"],
     ["tracknumber"],
   ]

     [[tracks.blacklist."Album 1"]]
     discnumber = "1"
     tracknumber = "4"

     [[tracks.blacklist."Album 2"]]
     tracknumber = "5"


   [groups]
   tags = [
     # ["album", "catalognumber"],
     ["album"],
   ]
   fallback_name = "fallback"

     [groups.split_tags]
     "Album 1" = ["discnumber"]
     "Album 2" = ["artist", "title"]
     fallback = ["title"]

     [[groups.separate."Album 3"]]
     title = "Track title"

     [[groups.separate."Album 3"]]
     discnumber = "1"
     tracknumber = "11"

     [[groups.separate."Album 4"]]
     discnumber = "2"
     tracknumber = "9"


Table ``playlist``
^^^^^^^^^^^^^^^^^^

.. code-block:: text

   [playlist]
   format = "m3u8"
   paths = "relative"

In the configuration file, table ``playlist`` can contain keys ``format`` and
``paths`` to specify the playlist format and paths, respectively.  Valid values
for ``format`` are ``m3u8`` and ``pls``, valid values for ``paths`` are
``absolute`` and ``relative``.  CPG interprets the values of these keys in a
case insensitive manner.


.. _table_groups:

Table ``groups``
^^^^^^^^^^^^^^^^

When CPG finishes searching for audio files, it categorizes the found tracks
into groups.  Groups are created based on the audio files' tag information.
Categorizing tracks into groups is controled by keys in table ``groups``.
Tracks are first grouped together according to tags specified in key ``tags``.
``tags`` is a list of lists of tags.

.. code-block:: text

   [groups]
   tags = [
     ["album", "catalognumber"],
     ["album"],
   ]

The above configuration snippet would cause CPG to first attempt to categorize
each track based on tags ``album`` and ``catalognumber``.  If a track has any
of these tags empty or unspecified, CPG attempts to categorize it with the next
list of tags -- in this case only tag ``album``.  The name of the resulting
group is a concatenation of each of the matched tags (in the same order as in
the configuration file).  CPG supports an arbitrarily long list of arbitrarily
long lists of tags.

.. code-block:: text

   [groups]
   fallback_name = "fallback"

If a track can't be categorized by any of the tag lists described in the
previous paragraph (all lists get skipped because of a missing tag), the track
is assigned to a fallback group.  The default fallback group name is
``fallback``.  The desired name can be assigned to key ``fallback_name``.

.. code-block:: text

   [groups.split_tags]
   "Album 1" = ["discnumber"]
   "Album 2" = ["artist", "title"]
   fallback = ["title"]

CPG can be configured to further split the created groups of tracks in table
``groups.split_tags``.  The above configuration snippet would split Group
``Album 1`` based on the value of tag ``discnumber``.  This means that if
``Album 1`` consisted of two discs, it would be split into two separate groups.
Group splitting can be performed using an arbitrary amount of tags, as shown in
the example with ``Album 2``.  Tracks from group ``Album 2`` would be split
into groups with unique combinations of ``artist`` and ``title`` tags.  It's
even possible to match the fallback group mentioned in the previous paragraph.

.. code-block:: text

   [[groups.separate."Album 3"]]
   title = "Track title"

   [[groups.separate."Album 3"]]
   discnumber = "1"
   tracknumber = "11"

   [[groups.separate."Album 4"]]
   discnumber = "2"
   tracknumber = "9"

After spliting groups, CPG can separate specific tracks into a new group.  This
can be configured by creating arrays of tables nested in table
``groups.separate``.  The table array names -- in the above example ``Album 3``
and ``Album 4`` -- are the names of the groups which should be matched.  The
above example will first move tracks from ``Album 3`` into a single new group.
Only tracks which match the tag criteria in the first or second table of the
array will be moved, though.  A track matches a tag criteria when all keys and
values specified in a table match the track's respective tags and tag values.
Then tracks from ``Album 4`` will be moved into a *different* new group.
Again, only tracks which match the tag criteria will be moved.

After creating all groups CPG shuffles the groups so that they're randomly
ordered in the resulting playlist.  This shuffling only affects the relative
order of groups and doesn't affect the order of tracks *within* each group.


Table ``track``
^^^^^^^^^^^^^^^

.. code-block:: text

   [tracks]
   sort = [
     ["tracknumber", "discnumber"],
     ["tracknumber"],
   ]

Table ``tracks`` controls track sorting and blacklisting.  The value of key
``sort`` is a list of lists of tags for sorting groups of tracks.  Track
sorting is performed after creating all groups, as described in section
:ref:`table_groups`.  A group of tracks can be sorted according to a list of
tags when each track has all tags from the list non-empty.  CPG sorts each
group of tracks according to the first such list of tags.  In other words, a
group of tracks where all of them have tags ``tracknumber`` and ``discnumber``
non-empty would be sorted according to the first tag list of the above
configuration snippet.  On the contrary, a group of tracks where some are
missing the ``discnumber`` tag would be sorted according to the second list.
An arbitrarily long list of arbitrarily long lists of tags is supported.  If no
tag list can be chosen for sorting, the group is left unsorted.

.. code-block:: text

   [[tracks.blacklist."Album 1"]]
   discnumber = "1"
   tracknumber = "4"

   [[tracks.blacklist."Album 2"]]
   tracknumber = "5"

Blacklisted tracks are removed from their groups immediately after assigning
tracks to groups but before any group splitting.  Blacklists can be configured
by creating arrays of tables nested in table ``groups.blacklist``.  The table
array names specify which group to blacklist tracks from, in the above example
from groups ``Album 1`` and ``Album 2``.  Narrowing down the choice of
blacklisted tracks is performed by specifying key value pairs in the tables.
Key value pairs correspond to track tag name and value pairs.  A table without any
key value pair will blacklist the entire group.
