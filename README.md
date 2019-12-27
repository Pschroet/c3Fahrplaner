### c3Fahrplaner

=============================

This software is released under the GNU General Public License v3.0 (see LICENSE).

This is a little tool to create a webpage containing the fahrplan of the Chaos Communication Congress, the Chaos Communication Camp and Datenspuren.
The events are clickable and everything needed to work is a web server (for the cookies, the rest should work even if opened as a file).

To start the script just run

```
python3 main.py
```

At the moment, this processes the fahrplan for the Datenspuren 2019. To change this, modify the file to be parsed in _main.py_ to either a local file or a remote one.

The tool can be used to process other schedules in XML the same format as the fahrplans, but there won't be any links, although the events should be shown.
