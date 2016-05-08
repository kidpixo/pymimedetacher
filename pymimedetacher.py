#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mailbox
import os
import optparse

# Input path with (Courier) maildir data
PATH = os.path.expanduser('~/.mail')
# Output path to store the attachments
OUTPATH = os.path.expanduser('~/detachments/')+PATH.split(os.sep)[-1] # the idea is to have an output folder per account

parser = optparse.OptionParser()

parser.add_option('-i', '--input', action="store", dest="PATH",
                  help="input maildir path to parse", default=PATH)
parser.add_option('-o', '--output', action="store", dest="OUTPATH",
                  help="output path to store the attachments", default=OUTPATH)
parser.add_option('-d', '--delete-attachment', action="store_true",
                  dest="del_attach", help="delete the attachments", default=False)
parser.add_option('-s', '--save_attachment', action="store_true",
                  dest="save_attach", help="save the attachments", default=False)
parser.add_option('-v', '--verbose', action="store_true",
                  dest="verbose", help="verbose output", default=False)

options, args = parser.parse_args()

PATH   = os.path.expanduser(options.PATH)
OUPATH = os.path.expanduser(options.OUTPATH)

print 'Options :'
print '%20s : %s' % ('Mailbox Path', PATH)
print '%20s : %s' % ('Output Path ', OUTPATH)
print '%20s : %s' % ('delete attachment', options.del_attach)
print '%20s : %s' % ('save attachment', options.save_attach)
print '%20s : %s' % ('verbose', options.save_attach)
# Useful links:
# - MIME structure :Parsing email using Python part 2,  http://blog.magiksys.net/parsing-email-using-python-content
# - Parse Multi-Part Email with Sub-parts using Python, http://stackoverflow.com/a/4825114/1435167

def mylistdir(directory):
    """A specialized version of os.listdir() that ignores files that
    start with a leading period."""
    filelist = os.listdir(directory)
    return [x for x in filelist
            if not (x.startswith('.'))]

def openmailbox(inmailboxpath,outmailboxpath):
    """ Open a mailbox (maildir) at the given path and cycle
    on all te given emails.
    """
    # If Factory = mailbox.MaildirMessage or rfc822.Message  any update moves the email in /new from /cur
    # see > http://stackoverflow.com/a/13445253/1435167
    mbox = mailbox.Maildir(inmailboxpath, factory=None)
    # iterate all the emails in the hierarchy
    for key, msg in mbox.iteritems():
        # ToDo Skip messages without 'attachment' without parsing parts,but what are attachments?
        #      I retain text/plain and text/html.
        # if 'alternative' in msg.get_content_type():
        # if msg.is_multipart():

        print 'Key          : ',key
        print 'Subject      : ',msg.get('Subject')
        if options.verbose:
            print 'Multip.      : ',msg.is_multipart()
            print 'Content-Type : ',msg.get('Content-Type')
            print 'Parts        : '
        detach(msg, key, outmailboxpath, mbox)
        print '='*20

def detach(msg, key, outmailboxpath, mbox):
    """ Cycle all the part of message,
    detach all the not text or multipart content type to outmailboxpath
    delete the header and rewrite is as a text inline message log.
    """
    print '-----'
    for part in msg.walk():
            content_maintype = part.get_content_maintype()
            if (content_maintype != 'text') & (content_maintype != 'multipart'):
                filename = part.get_filename()
                if options.verbose:
                    print '   Content-Disposition  : ', part.get('Content-Disposition')
                    print '   maintytpe            : ',part.get_content_maintype()
                print '    %s : %s' % (part.get_content_type(),filename)
                outpath = outmailboxpath+key+'/'
                if options.save_attach:
                    try:
                        os.makedirs(outpath)
                    except OSError:
                        if not os.path.isdir(outpath):
                            raise

                    if filename is None:
                        import tempfile
                        fp = tempfile.NamedTemporaryFile(dir=outpath,
                                                         delete=False)
                        filename = os.path.basename(fp.name)
                        print("Will save in {}".format(fp.name))
                    else:
                        fp = open(outpath+filename, 'wb')
                    fp.write(part.get_payload(decode=1) or "")
                    fp.close()
                outmessage = '    ATTACHMENT=%s\n    moved to\n    OUTPATH=%s' %(filename,outpath[len(OUTPATH):]+filename)
                if options.del_attach:
                    # rewrite header and delete attachment in payload
                    tmp = [part.__delitem__(h) for h in part.keys()]
                    part.set_payload(outmessage)
                    part.set_param('Content-Type','text/html; charset=ISO-8859-1')
                    part.set_param('Content-Disposition','inline')
                    mbox.__setitem__(key, msg)
                print outmessage
                print '-----'

# Recreate flat IMAP folder structure as directory structure
# WARNING: If foder name contains '.' it will changed to os.sep and it will creare a new subfolder!!!
for folder in mylistdir(PATH):
    folderpath = OUTPATH+folder.replace('.',os.sep)+os.sep
    try:
        os.makedirs(folderpath)
    except OSError:
        if not os.path.isdir(folderpath):
            raise
    print
    print 'Opening mailbox:',PATH+os.sep+folder
    print '  Output folder: ',folderpath
    print
    print '='*20
    openmailbox(PATH+os.sep+folder,folderpath)
    print 40*'*'
