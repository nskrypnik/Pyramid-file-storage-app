import sys
import re
import os.path
import getopt
import getpass
import gdata.docs.service
import gdata.docs.client
import gdata.spreadsheet.service
import md5


class Gdoc(object):

    def __init__(self, email, password):
        """Constructor for the DocsSample object.

        Takes an email and password corresponding to a gmail account to
        demonstrate the functionality of the Document List feed.

        Args:
          email: [string] The e-mail address of the account to use for the sample.
          password: [string] The password corresponding to the account specified by
              the email parameter.

        Returns:
          A DocsSample object used to run the sample demonstrating the
          functionality of the Document List feed.
        """
        source = 'Document List Python Sample'
        self.client = gdata.docs.client.DocsClient(source='noodles-Python_file_storage-v0.1')
        
        self.gd_client = gdata.docs.service.DocsService()
        self.gd_client.ClientLogin(email, password, source=source)

        # Setup a spreadsheets service for downloading spreadsheets
        self.gs_client = gdata.spreadsheet.service.SpreadsheetsService()
        self.gs_client.ClientLogin(email, password, source=source)

    def _GetFileExtension(self, file_name):
        """Returns the uppercase file extension for a file.

        Args:
          file_name: [string] The basename of a filename.

        Returns:
          A string containing the file extension of the file.
        """
        match = re.search('.*\.([a-zA-Z]{3,}$)', file_name)
        if match:
          return match.group(1).upper()
        return False

    def g_upload(self, file):
        """Prompts that enable a user to upload a file to the Document List feed."""
        
        file_name = file.filename
        ext = self._GetFileExtension(file_name)

        if not ext or ext not in gdata.docs.service.SUPPORTED_FILETYPES:
            print 'File type not supported. Check the file extension.'
            return
        else:
            content_type = gdata.docs.service.SUPPORTED_FILETYPES[ext]

        title = md5.md5(file_name).hexdigest()
    #    while not title:
    #        title = raw_input('Enter name for document: ')



        try:
#            import pdb; pdb.set_trace()
            ms = gdata.MediaSource(file_handle=file.file, content_type=content_type,content_length=os.fstat(file.file.fileno())[6])
        except IOError:
            print 'Problems reading file. Check permissions.'
            return

        entry = self.gd_client.Upload(ms, title)
#        entry.publish = True
#        self.client.Update(entry, media_source=ms)

        if not entry:
            return False
            
        return entry.GetAlternateLink().href




#    def gAuth(user, password):

#        client = gdata.docs.client.DocsClient(source='noodles-Pyramid-v0.1')
#        return client.ClientLogin(user, password, client.source)


#    def PrintFeed(feed):
#        print '\n'
#        if not feed.entry:
#            print 'No entries in feed.\n'
#        for entry in feed.entry:
#            print entry.title.text.encode('UTF-8'), entry.GetDocumentType(), entry.resource_id.text

#            # List folders the document is in.
#        for folder in entry.InFolders():
#            print folder.title
#            







