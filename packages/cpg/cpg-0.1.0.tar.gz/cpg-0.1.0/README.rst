Configurable Playlist Generator
===============================

CPG (stands for configurable playlist generator) is a command line application
for recursively scanning a directory for audio files and outputing a playlist
file.  Several ways of influencing the ordering of tracks in the generated
playlist are available.  The generated playlist's file format and the type of
its paths (absolute or relative) can be configured too.

Quick feature overview:

- recursively scans a directory for audio files
- sorts the found tracks into groups according to tag information
- it can be configured based on which tags to create groups
- groups can be additionally split up based on configurable criteria
- tracks can be blacklisted in a configurable way
- the resulted groups are randomly shuffled
- ordering of tracks withing groups is configurable
- resulted playlists can be exported into various playlist formats

For more information regarding installation and usage please refer to the
`documentation`_.

.. _documentation: https://cpg.readthedocs.io/
