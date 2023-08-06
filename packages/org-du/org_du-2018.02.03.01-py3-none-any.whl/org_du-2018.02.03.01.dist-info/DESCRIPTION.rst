org-du
-----------------------------
This Python 3 script parses parses a list of Org-mode files and
generates output similar to "du" (disk usage) but with lines of
Org-mode instead of kilobytes.

The purpose of this script is to use its output as the input for "xdu" in order
to get a graphical visualization:

: org-du.py my_org_file.org another_org_file.org | xdu

The script accepts an arbitrary number of files (see your shell for
possible length limitations).

Please read https://github.com/novoid/org-du/ for further information and descriptions.


