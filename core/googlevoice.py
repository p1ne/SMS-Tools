import time, sqlite3, csv
from core import Text


class GoogleVoice:
    """ Google Voice (in sqlite or format) reader and writer """

    def parse(self, file):
        return self.parseSQL(file)
        #TODO add direct files parsing?

    def parseSQL(self, file):
        """ Parse a GV sqlite file to Text[] """

        conn = sqlite3.connect(file)
        c = conn.cursor()
        texts = []
        query = c.execute(
            'SELECT TextMessageID, TimeRecordedUTC, Incoming, Text, PhoneNumber \
            FROM TextMessage \
            INNER JOIN TextConversation ON TextMessage.TextConversationID = TextConversation.TextConversationID \
            INNER JOIN Contact ON TextConversation.ContactID = Contact.ContactID \
            ORDER BY TextMessage.TextMessageID ASC')
        for row in query:
            try:
                ttime = time.mktime(time.strptime(row[1], '%Y-%m-%d %H:%M:%S.%f'))
            except ValueError:
                ttime = time.mktime(time.strptime(row[1], '%Y-%m-%d %H:%M:%S'))
            txt = Text(row[4],long(ttime*1000),row[2]==0,row[3])
            texts.append(txt)
        return texts

    def write(self, texts, outfile):
        raise Exception("not implemented!")
        #TODO!!