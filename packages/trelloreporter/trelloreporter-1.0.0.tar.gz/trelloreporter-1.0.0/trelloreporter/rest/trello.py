import asyncio
import logging

import uvloop
import aiohttp

class TrelloRest(object):

    def __init__(self):
        """
        TODO: dictate preference of receiving class-level variables
        api_token, api_key, api_url, api_organisation)
        """
        self._boards = dict()
        self._lists = dict()
        self._cards = dict()
        self._members = dict()
        self._api_url = ""
        self._api_token = ""
        self._api_key = ""
        self._organisation = ""
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        self._loop = asyncio.get_event_loop()
        self._logger = logging.getLogger('trelloreporter')

    def configure_api_parameters(self, api_token, api_key, api_url, api_organisation):
        """
        A function to initialise the API parameters for Trello Method calls
        :param api_token: The API Token
        :param api_key: The API Key
        :param api_url: The API URL
        :param api_organisation: The API organisation
        :return: <None>
        """
        self._api_token = api_token
        self._api_key = api_key
        self._api_url = api_url
        self._organisation = api_organisation
        self._logger.info('Trello API configuration URL:{0} API Organisation:{1}'.format(api_url, api_organisation))


    #Accessor methods for the api_url, api_token, api_key, api_organisation
    #https://docs.python.org/3.5/library/asyncio-task.html - co-routines used to synchronise states
    @property
    def api_url(self):
        """
        Accessor for API URL
        :return: <string> return the value of the API URL
        """
        return self._api_url

    @api_url.setter
    def api_url(self, url_string):
        """

        :param url_string: Set the value of the API string
        """
        #TODO : validate strings - sanitize URL
        self._api_url = url_string

    @property
    def api_token(self):
        """
        Accessor for the api token
        :return:<string> return the current value of the API token
        """
        return self._api_token

    @api_token.setter
    def api_token(self, token_string):
        """
        Set the value of _api_token
        :param token_string: <string> value of the token
        """
        self._api_token = token_string

    @property
    def organisation(self):
        """

        :return: <string> Returns the _organisation object
        """
        return self._organisation

    @organisation.setter
    def organisation(self, org_string):
        """

        :param org_string: <string> the trello organisation to perform lookups against
        """
        #TODO validate strings or perform a lookup on trello ???
        self._organisation = org_string

    #Accessor/Mutator methods for the trello elements
    @property
    def boards(self):
        """

        :return: A dictionary of boards read from the trello API
        """
        return self._boards

    @boards.setter
    async def boards(self):
        """
        Read boards of the organisation using the self._api_url
        Chained to property methods:
            lists
            cards
            members
        """
        await self.populate_boards()

    @property
    def lists(self):
        """

        :return: <dict> A dictionary containing all the lists of the orgnanisation
        """
        return self._lists

    @lists.setter
    async def lists(self):
        """
        Method to populate all the trello lists of the self._organisation
        """
        if self._boards == {}:  #if the self._boards has not been populated, populate
            await self.populate_boards() #wait for the populate_boards()

        await self.populate_lists()

    @property
    def cards(self):
        """

        :return: <dict> returns a dict of the organisation's cards self._cards
        """
        return self._cards

    @cards.setter
    async def cards(self):
        """
        Fetch the cards of the self._organisation and populate them into self._cards
        """
        if self._boards == {}:
            await self.populate_boards()

        await self.populate_cards()

    @property
    def members(self):
        """

        :return: <dict> return a dict of the members of the self._organisation
        """

        return self._members

    @members.setter
    async def members(self):
        """
        Retrieve the members of the self._organisation from the Trello API
        """
        await self.populate_members()

    async def populate_boards(self):
        """
        Asynchronous method to populate the boards of the self._organisation, using the class-lvel
        self._api_url, self._api_token, self._api_key, self._organisation
        """
        self._logger.info('Attempting to populate board data from Trello')
        url_string = "{0}/organizations/{1}/boards?key={2}&token={3}".format(self._api_url,
                                                                            self._organisation,
                                                                            self._api_key,
                                                                            self._api_token
                                                                            )
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url_string) as response_string:
                    resp = await response_string.json()

        except Exception:
            self._logger.exception('Error connecting to Trello for board population')

        for board in range(len(resp)):
            board_text = resp[board]
            board_id = board_text['id']
            self._boards[board_id] = board_text
            self._logger.debug('Found board: {0}'.format(board_text['name']))

        self._logger.info('{0} boards populated successfully from Trello'.format(len(resp)))

    async def populate_lists(self):
        """
        Async method to facilitate the requesting of lists under a trello organisation
        """
        self._logger.info('Attempting to populate list data from Trello')
        if self._boards == {}:
            self._logger.info('Lists waiting for boards to populate')
            await self.populate_boards() #Ensure the boards are populated

        for board in self._boards.keys():
            try:
                url_string = "{0}/boards/{1}/lists?key={2}&token={3}".format(self._api_url,
                                                                                board,
                                                                                self._api_key,
                                                                                self._api_token
                                                                                )
                async with aiohttp.ClientSession() as session:
                    async with session.get(url_string) as response_string:
                        self._lists[board] = dict() #Initialise a dict at this boardID
                        resp = await response_string.json()
                        for list in resp:
                            list_id = list['id']
                            self._lists[board][list_id] = list
                            self._logger.debug('Found list: {0}'.format(list['name']))
            except Exception:
                self._logger.exception('Error connecting to Trello for list population')

        self._logger.info('Lists populated successfully from Trello')

    async def populate_cards(self):
        """
        Method to read the cards of an organisation from the trello API and store them as a dict
        using the board_id and the card_id as the keys
        """
        self._logger.info('Attempting to populate card data from Trello')
        if self.cards == {}:
            self._logger.info('Cards waiting for boards to populate')
            await self.populate_boards() #Ensure the boards are populated

        for board in self._boards.keys():
            try:
                url_string = "{0}/boards/{1}/cards/?key={2}&token={3}".format(self._api_url,
                                                                              board,
                                                                              self._api_key,
                                                                              self._api_token
                                                                              )
                async with aiohttp.ClientSession() as session:
                    async with session.get(url_string) as response_string:
                        resp = await response_string.json()
                        self._cards[board] = dict()
                        for card in resp:
                            card_id = card['id']
                            self._cards[board][card_id] = card
                            self._logger.debug('Found card: {0}'.format(card['desc']))

            except Exception:
                self._logger.exception('Error connecting to Trello for card population')

        self._logger.info('Cards populated successfully from Trello')

    async def populate_members(self):
        """
        Populate the members under the organisation, storing each member in the members dict()
        """
        self._logger.info('Attempting to populate member data from Trello')
        url_string = "{0}/organization/{1}/members?key={2}&token={3}".format(self._api_url,
                                                                             self._organisation,
                                                                             self._api_key,
                                                                             self._api_token)
        try:
            async with aiohttp.ClientSession() as session:
                response_string = await session.get(url_string)
                async with response_string:
                    resp = await response_string.json()
                    for member in range(len(resp)):
                        member_text = resp[member]
                        member_id = member_text['id']
                        self._members[member_id] = member_text
                        self._logger.debug('Found member: {0}'.format(member_text['fullName']))
                    self._logger.info(
                        '{0} members populated successfully from Trello'.format(len(resp)))
        except Exception:
            self._logger.exception('Error connecting to Trello for board member population')