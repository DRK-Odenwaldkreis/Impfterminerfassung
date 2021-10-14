import logging
import locale
import time
import datetime
import sys
import csv
import numpy as np 
from pdfcreator.pdf import PDFgenerator
sys.path.append("..")
from utils.database import Database
from utils.sendmail import send_mail_report
from utils.getRequesterMail import get_Leitung_from_StationID


logFile = '../../Logs/Impfzentrum/TagesreportJob.log'
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Tagesreport')
logger.info('Starting Tagesreporting')


def create_PDFs(content, date):

    logger.debug('Calculated this total number of tests: %s' % (str(tests)))
    
    return PDF.generate()

if __name__ == "__main__":
    try:
        if len(sys.argv)  == 2:
            requestedDate = sys.argv[1]
            send=False
        elif len(sys.argv) == 3:
            requestedDate = sys.argv[1]
            send=True
        else:
            logger.debug('Input parameters are not correct, date and/or requested needed')
            raise Exception
        DatabaseConnect = Database()
        sql = "Select Count(Voranmeldung.id),Impfstoff.Kurzbezeichnung from Voranmeldung JOIN Termine ON Voranmeldung.Termin_id=Termine.id JOIN Station ON Station.id=Termine.id_station JOIN Impfstoff ON Impfstoff.id=Station.Impfstoff_id where Voranmeldung.Tag='%s' and Voranmeldung.Used=1 ORDER BY Impfstoff.id;" % (requestedDate.replace('-', '.'))
        logger.debug('Getting all Events for a date with the following query: %s' % (sql))
        exportEvents = DatabaseConnect.read_all(sql)
        logger.debug('Received the all entries: %s' %(str(exportEvents)))
        PDF = PDFgenerator(exportEvents, f"{requestedDate}")
        filename = PDF.generate()
        if send:
                logger.debug('Sending Mail')
                send_mail_report(filename,requestedDate,get_Leitung_from_StationID(0))
        logger.info('Done')
    except Exception as e:
        logging.error("The following error occured: %s" % (e))
    finally:
        DatabaseConnect.close_connection()