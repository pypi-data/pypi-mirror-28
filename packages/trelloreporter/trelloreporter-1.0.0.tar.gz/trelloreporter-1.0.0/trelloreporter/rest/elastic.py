import asyncio
from datetime import datetime
import logging

import uvloop
from elasticsearch import Elasticsearch

class ElasticRest(object):

    def __init__(self):
        """
        Configure the credentials required to access the ES endpoint
        """
        self._username = ""
        self._password = ""
        self._elastic_endpoint = ""
        self._elastic_port = ""
        self._elastic_index = ""

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        self._loop = asyncio.get_event_loop()
        self._es_instance = Elasticsearch()
        self._logger = logging.getLogger('trelloreporter')

    def configure_elastic_parameters(self, username, password, endpoint, port, index):
        """
        A function to initialise the Elasticsearch parameters; ready for shipping data
        :param username: the ES username
        :param password: the ES password
        :param endpoint: the ES endpoint
        :param port: the ES port
        :param index: the index within ES
        :return: <None>
        """
        self._elastic_index = index
        self._elastic_port = port
        self._elastic_endpoint = endpoint
        self._password = password
        self._username = username
        self._es_instance = Elasticsearch([endpoint],
                                          http_auth=(username, password),
                                          port=port
                                          )

        self._logger.info(
            'Elasticsearch configuration endpoint:{0} port:{1} index:{2}'.format(endpoint, port, index)
            )

    def write_to_elastic(self, document, type):
        """
        curl -u elastic -XPUT "http://127.0.0.1:9200/trello/members/1/_create {document}"
        A function to write data to an ElasticSearch endpoint. The function adds a timestamp
        indicating the current time - this is for generating time-series data in ES
        :param document: The object to be written as an elastic document
        :param type: The type of document
        :return: 0 if the write was successful.
        """
        document['writeTime'] = datetime.now().isoformat()

        try:
            self._logger.debug('Attempting to create {0} document: {1}'.format(
                type, document['Description']))
            res = self._es_instance.index(index=self._elastic_index,
                                          doc_type=type,
                                          body=document)
            if (res['created']) is not 'True':
                self._logger.debug('{0} document written successfully'.format(
                    document['Description']))
                return 0
            else:
                self._logger.debug('{0} document not written'.format(
                    document['Description']))
                return 1

        except Exception as ex:
            self._logger.error('Writing to Elasticsearch failed: {0}'.format(ex))
            return 1

    def search_latest_document(self, type):
        """
        Return the timestamp of the most recent document in the index.
        The function uses 'writeTime' as the aggregation field.
        :param index: <str> : the index
        :param type: <str> : the type of document
        :return: <datetime> : a timestamp of the most recent document in the index

        Elastic REST call : GET http://<ES_HOST>:<ES_PORT>/trello_reports-/card/_search?q=writeTime:<date>
        """
        time_of_insert = datetime.now()
        try:
            self._logger.debug('Searching for latest {0} document'.format(type))
            result = self._es_instance.search(index=self._elastic_index,
                                              doc_type=type,
                                              sort="writeTime:desc",
                                              size=1)
            time_of_insert = datetime.strptime(result['hits']['hits'][0]['_source']['writeTime'],
                                               "%Y-%m-%dT%H:%M:%S.%f")
            self._logger.info('Latest time of insert for {0} is {1}'.format(type, time_of_insert))
        except Exception as ex:
            self._logger.error('Unable to obtain latest document in index {0}. ERROR :{1}'.format(
                self._elastic_index, ex))

        return time_of_insert
