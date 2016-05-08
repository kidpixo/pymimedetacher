# pymimedetacher

[![Join the chat at https://gitter.im/kidpixo/pymimedetacher](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/kidpixo/pymimedetacher?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Compact script to parse maildir structure, detach attachment and save them in a directory structure mirroring the mailbox folders.

It is based on python core-library [mailbox (Manipulate mailboxes in various formats — Python 2.7.10 documentation)](https://docs.python.org/2/library/mailbox.html).

## Options

`-h, --help`

show help message and exit

`-i PATH, --input=PATH`

Input [Maildir](https://en.wikipedia.org/wiki/Maildir) path to parse.

You easly can obtain a local copy of your IMAP mailbox with [OfflineIMAP](http://offlineimap.org/).

Some good tutorials on offlineimap setup specific to gmail:
- [The Homely Mutt / Steve Losh](http://stevelosh.com/blog/2012/10/the-homely-mutt/)
- [Mutt + Gmail + Offlineimap](https://pbrisbin.com/posts/mutt_gmail_offlineimap/)
- [OfflineIMAP - ArchWiki](https://wiki.archlinux.org/index.php/OfflineIMAP)

`-o OUTPATH, --output=OUTPATH`

Output path to store the attachments, the subfolders will mirror the mailbox folder structure.

`-d, --delete-attachment`

Delete the attachments in the original mail, default is to leave there.

`-s, --save_attachment`

Save and decode the attachments files, default is do nothing.

`-v, --verbose`

Print more verbose output.

