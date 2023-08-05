import sys
import json
import time
import os
import re
from os.path import basename
from datetime import datetime
import logging
from logging import config
import smtplib
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
sys.path.append('../../')

from trelloreporter.writer import excel
from trelloreporter.config import yaml
from trelloreporter.rest import elastic

#Global variables: pass-by-reference messy
instance = excel.TrelloReader()
es_instance = elastic.ElasticRest()
logger = logging.getLogger('trelloreporter')
mail_config = dict()
connection = sqlite3.connect('/opt/trelloreporter/data/trelloreporter.db')
cursor = connection.cursor()
options = {'boards':0, 'lists':0, 'cards':0, 'pretty':0, 'spreadsheet':0, 'email':0, 'unsubscribe':0}


def setup_config(config_file_path):
    """
    A function to setup configuration paratmers.
    :param config_file_path: <str> : a file path to a configuration file, can be gathered
                                    from environment variable TRELLO_CONFIG or argv
    """
    config = yaml
    try:
        config_values = config.Yaml.read(os.getenv("TRELLO_CONFIG", default=config_file_path))
    except Exception as ex:
        print(ex)

    #Configure logging using the config file
    logging.config.dictConfig(config_values['log_config'])
    logger.info('=============Start=============')

    logger.info('Using config {0}'.format(config_file_path))

    instance.configure_api_parameters(
        api_token=os.getenv("TRELLO_TOKEN", default=config_values['api']['token']),
        api_key=os.getenv("TRELLO_KEY", default=config_values['api']['key']),
        api_url=os.getenv("TRELLO_URL", default=config_values['api']['url']),
        api_organisation=os.getenv("TRELLO_ORG", default=config_values['api']['organization'])
    )

    es_instance.configure_elastic_parameters(
        username=os.getenv("ES_USERNAME", default=config_values['elasticsearch']['username']),
        password=os.getenv("ES_PASSWORD", default=config_values['elasticsearch']['password']),
        endpoint=os.getenv("ES_ENDPOINT", default=config_values['elasticsearch']['endpoint']),
        port=os.getenv("ES_PORT", config_values['elasticsearch']['port']),
        index=os.getenv("ES_INDEX", default=config_values['elasticsearch']['index'])
    )

    mail_config['Subject'] = config_values['mail']['subject']
    mail_config['From'] = config_values['mail']['from']
    mail_config['Recipients'] = config_values['mail']['recipients']
    mail_config['Relay'] = config_values['mail']['relay']

    logger.info('Checking config file for new subscribers...')
    if mail_config['Recipients'] == [None]:
       logger.info('No subscribers in the config file')
       mail_config['Recipients'] = list()
    else:
       add_subscribers(mail_config['Recipients'])
    
    for recipient in connection.execute('SELECT * FROM subscribers').fetchall():
       mail_config['Recipients'].append(recipient)
    
    if options['email'] == 1:
       index = sys.argv.index('-e')
       email_address = str(sys.argv[index + 1])
       if mail_config['Recipients'] == [None]:
          mail_config['Recipients'] = email_address
       else:
          mail_config['Recipients'].append([email_address])
       add_subscribers([email_address])
     
    logger.info(json.dumps(mail_config, indent=4))
    logger.info('Mail configuration completed. Recipients: {0}'.format(mail_config['Recipients']))

def write_to_elastic():
    """
    Write card content to Elasticsearch
    :return:
    """
    if datetime.today().day == es_instance.search_latest_document(type="card").day:
        logger.info("Data found in Elastic for today: no updates to elastic")
    else:
        logger.info('No data found in Elasticsearch for today: writing documents')
        logger.debug('Boards {0}'.format(instance.get_boards().keys()))
        for board in instance.get_boards().keys():
            logger.debug('Writing card documents for board ID {0} to Elasticsearch'.format(board))
            for card in instance.get_board_cards(board):
                es_instance.write_to_elastic(instance.get_card_summary(card), 'card')

def generate_spreadsheet():
    """
    Write data to excel
    """
    instance.write_to_excel('/opt/trelloreporter/data/TrelloReport-'+ datetime.now().strftime('%Y-%m-%d') +'.xlsx')

def add_subscribers(subscribers):
    """

    :param subscribers: <list> a list of subscribers to add to the SQLite database
    :return:
    """
    cursor.execute('CREATE TABLE IF NOT EXISTS subscribers (email text)')

    for subscriber in subscribers:
        address = (subscriber,)
        cursor.execute('SELECT * FROM subscribers WHERE email=?', address)
        if cursor.fetchone() == None:
            cursor.execute('INSERT INTO subscribers VALUES (\'{0}\')'.format(subscriber))
            logger.info('No subscribers found in the database')
            logger.info('Adding user to subscribers: {0}'.format(subscriber))

    #Commit the changes
    connection.commit()

def remove_subscriber(subscriber):
    """
    Remove subscribers from the SQL database
    :param subscriber: <str> a subscriber to remove
    :return:
    """
    address = (subscriber,)
    if cursor.execute('SELECT * FROM subscribers WHERE email=(?)', address).fetchone() == None:
        logger.error('No subscriber found {0}'.format(subscriber))
    else:
        cursor.execute('DELETE FROM subscribers WHERE email=(?)', address)
        logger.info('Subscriber deleted: {0}'.format(subscriber))

    connection.commit()

def dispatch_spreadsheet():
    """
    A method to send an email of the spreadsheet (as an attachment)
    :return:
    """
    #Create a text/plain message, populate mail headers
    message = MIMEMultipart()
    message['Subject'] = mail_config['Subject']
    message['From'] = mail_config['From']

    message.attach(MIMEText('{0} TrelloReport attached'.format(datetime.today())))

    filename = '/opt/trelloreporter/data/TrelloReport-{0}.xlsx'.format(datetime.now().strftime('%Y-%m-%d'))
    with open(filename, 'rb') as file:
        part = MIMEApplication(file.read(), Name=basename(filename))

    part['Content-Disposition'] = 'attachment; filename={0}'.format(basename(filename))
    logger.info('Attaching file: {}'.format(filename))
    message.attach(part)

    logger.info('Preparing to dispatch spreadsheet using SMTP')
    try:
        smtp_service = smtplib.SMTP(mail_config['Relay'])
        smtp_service.sendmail(from_addr=mail_config['From'],to_addrs=mail_config['Recipients'],
                          msg=message.as_string())
        smtp_service.quit()
    except Exception as ex:
        logger.info('Failed to send email... {0}'.format(ex))

def main():
    start_time = time.time()
    # A static configuration file
    config_file_path = "/opt/trelloreporter/config/trelloreporter.yml"

    usage = "trelloreporter \n\n " \
            "Usage: trelloreporter [option] --config <config.yml>\n" \
            " config.Yaml is the Yaml configuration file\n" \
            " Options:\n" \
            "   -b            Print boards\n" \
            "   -l            Print lists\n" \
            "   -c            Print cards\n" \
            "   -s            Generate an excel spreadsheet\n" \
            "   -e            Subscribe to the TrelloReporter via email\n" \
            "   -r            Remove a subscriber from the database\n" \
            "   --pretty      Pretty-Print the json data\n" \
            "   --config      Specify a Yaml file containing the API credentials\n\n" \
            "Example: \n" \
            "   trelloreporter -b --pretty --config myconfigfile.yml"

    if len(sys.argv) == 1:
       print(usage)
       sys.exit(0)

    #Process the command line arguments
    #Check for config file
    try:
        config_index = sys.argv.index("--config")
        config_file_path = sys.argv[config_index + 1]
        setup_config(config_file_path=config_file_path)

    except ValueError:
        print("Assuming default configuration")
        print("==========")
        print(usage)
        print("==========")
        setup_config(config_file_path=config_file_path)

    #Start with the display output filters
    # If no index is found, the list.index() method throws a ValueError
    try:
        display_index = sys.argv.index('-b')
        options['boards'] = 1
    except Exception as ex:
        logger.info('Board display not selected')

    try:
        display_index = sys.argv.index('-l')
        options['lists'] = 1
    except ValueError:
        logger.info('List display not selected')

    try:
        display_index = sys.argv.index('-c')
        options['cards'] = 1
    except:
        logger.info('Card display not selected')

    try:
        display_index = sys.argv.index('-s')
        options['spreadsheet'] = 1
    except:
        logger.info('Spreadsheet not selected')

    try:
        display_index = sys.argv.index('-e')
        options['email'] = 1
    except:
        logger.info('Email subscription dispatch not selected')

    try:
        pretty_index = sys.argv.index("--pretty")
        options['pretty'] = 1
    except ValueError:
        logger.info("Dumping raw JSON: pretty-printing not set")

    try:
        display_index = sys.argv.index('-r')
        options['unsubscribe'] = 1
        try:
           remove_subscriber(sys.argv[display_index + 1])
        except:
           logger.error('Unable to read supplied email address... was it provided?')
    except ValueError:
        logger.info('Unable to read supplied email address')


    logger.debug('Reading member data from the trello API')
    instance.populate_members()
    logger.debug('Reading list data from the trello API')
    instance.populate_lists()
    logger.debug('Reading trello cards from the trello API')
    instance.populate_cards()

    if options['pretty'] == 1:
        if options['boards'] == 1:
            print(json.dumps(instance.get_boards(), indent=4, sort_keys=True))
            print("==========")
        if options['lists'] == 1:
            print(json.dumps(instance.get_lists(), indent=4, sort_keys=True))
            print("==========")
        if options['cards'] == 1:
            for board_id in instance.get_cards().keys():
                for card in instance.get_board_cards(board_id):
                    print(json.dumps(instance.get_card_summary(card), indent=4, sort_keys=True))
            print("==========")
    else:
        if options['boards'] == 1:
            print(instance.get_boards())
            print("==========")
        if options['lists'] == 1:
            print(instance.get_lists())
            print("==========")
        if options['cards'] == 1:
            print(instance.get_cards())
            print("==========")

    #Push data into Elasticsearch
    write_to_elastic()

    #Generate spreadsheet on the first day of the month or when the generate spreadsheet switch is set.
    if datetime.today().day == 1 or options['spreadsheet'] == 1:
        generate_spreadsheet()
        dispatch_spreadsheet()

    connection.close()

    logger.info('Runtime: {:.2f}s'.format(time.time() - start_time))
    logger.info('=============End=============')
    exit()

main()
