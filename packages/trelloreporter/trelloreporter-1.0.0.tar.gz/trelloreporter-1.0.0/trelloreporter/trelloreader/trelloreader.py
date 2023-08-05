import requests
from requests import Session

from trelloreporter.rest import trello

class TrelloReader(object):

    def __init__(self, apiToken, apiKey, apiURL, apiOrganisation):
        """

        :param apiToken: The API token
        :param apiKey:   The API key
        :param apiURL:   The API URL
        :param apiOrganisation: The API Organisation name as it appears in trello
        """
        self.api_token = apiToken
        self.api_key = apiKey
        self.api_url = apiURL
        self.boards = dict()
        self.cards = dict()
        self.lists = dict()
        self.members = dict()
        self.organisation = apiOrganisation

    def populate_boards(self):
        """
        Boards are the highest level concept within the Trello workflow.
        The Boards API allows you to list, view, create, and edit Boards.
        Each Board has a name, description, a set of members attached, and an ordered array of Lists.

        Populates the boards found under the api_key's endpoint as a JSON dict.
        :return: <null> initialises the cards to the json list of boards
        """
        urlString = "{0}/organizations/{1}/boards?key={2}&token={3}".format(self.api_url, self.organisation, self.api_key,
                                                                      self.api_token)
        responseString = requests.get(urlString)
        resp = responseString.json()

        for board in range(len(resp)):
            boardText = resp[board]
            boardID = boardText['id']
            self.boards[boardID] = boardText

    def populate_cards(self):
        """
        Extracts the cards found at the api_key's endpoint, storing each
        card as a JSON item in a dict
        :return:
        """
        for board in self.boards.keys():
            boardID = board
            urlString = "{0}/boards/{1}/cards/?key={2}&token={3}".format(self.api_url, boardID, self.api_key, self.api_token)
            responseString = requests.get(urlString)
            self.cards[boardID] = dict() #Initialise a new key using the ID extracted from the response
            for card in responseString.json():
                cardID = card['id']
                self.cards[boardID][cardID] = card

    def populate_lists(self):
        """
        Populates the lists found under the organisation and stores them in the lists() dictionary
        :return: <dict> of Trello lists
        """
        for board in self.boards.keys():
            boardID = board
            urlString = "{0}/boards/{1}/lists/?key={2}&token={3}".format(self.api_url, boardID, self.api_key, self.api_token)
            responseString = requests.get(urlString)
            self.lists[boardID] = dict() #Initialise a dictionary at lists.[boardID]
            for list in responseString.json():
                listID = list['id']
                self.lists[boardID][listID] = list

    def populate_members(self):
        """
        Method to populate the members of the Trello organisation
        :return: <null> : Initialises the members() dict
        """
        urlString = "{0}/organizations/{1}/members?key={2}&token={3}".format(self.api_url, self.organisation,
                                                                             self.api_key, self.api_token)

        responseString = requests.get(urlString)
        resp = responseString.json()

        for member in range(len(resp)):
            memberText = resp[member]
            memberID = memberText['id']
            self.members[memberID] = memberText

    def get_members(self):
        """

        :return: <dict> : return the members of the organisation
        """
        return self.members

    def get_list_cards(self,listID):
        """
        Returns a dict of cards based on a filter argument "lane"

        :param lane: <str> The lane in which the cards reside
        :return: <list> The cards which all belong to the lane
        """
        listFound = 0   #Marker for list found: this remains zero if there is no list which matches the search
        myCards = dict() #A place to store cards belonging to the list
        for boardID in self.boards.keys():
            for cardID in self.cards[boardID]:
                if listID == self.cards[boardID][cardID]['idList']:
                    myCards[cardID] = self.cards[boardID][cardID]
                    listFound = 1   #Set the marker to one

        if listFound == 1:
            return myCards
        else:
            return "List " + listID + " not found"

    def get_boards(self):
        """

        :return: <list> : returns a json array of boards
        """
        return self.boards

    def get_board(self, boardID):
        """
        :param: <str> : the ID of the board to return
        :return: <dict> : returns a json array of boards
        """
        if boardID in self.boards.keys():
            return self.boards[boardID]
        else:
            return "Board "+ boardID +" not found"

    def get_board_cards(self, boardID):
        """

        :param boardID: The boardID of the cards to return
        :return: <dict> All the cards which belong ot the board at hand
        """
        if boardID in self.boards.keys():
            return self.cards[boardID]
        else:
            return "Board " + boardID + " not found"

    def get_board_lists(self, boardID):
        """

        :param boardID: the boardID of the lists
        :return: <dict> : returns a dict of all the lists in a given board
        """
        if boardID in self.boards.keys():
            return self.lists[boardID]
        else:
            return "Board " + boardID + " not found"

    def get_lists(self):
        """

        :return: <dict> : returns a dict of lists
        """
        return self.lists

    def get_list(self, listID):
        """
        :param listID:  <str> : the ID of the list
        :return: <dict> : returns a json representation of a list item
        """
        for board in self.boards.keys():
            boardID = board
            for list in self.lists:
                if listID in self.lists[boardID].keys():
                    return self.lists[boardID][listID]

        return "List " + listID + " not found" #At the end of the loop, there is no list found

    def get_cards(self):
        """

        :return: <dict> : returns a json dict of cards
        """
        return self.cards

    def get_card(self, cardID):
        """
        :param cardID: <str> : the ID of the card to retrieve
        :return: <dict> : returns a json representation of the card
        """
        for board in self.boards.keys():
            boardID = board
            for card in self.cards:
                if cardID in self.cards[boardID].keys():
                    return self.cards[boardID][cardID]

        return "Card " + cardID + " not found" #At the end of the loop there is no card found

    def get_card_summary(self, cardID):
        """
        :parameter : str : The ID of the card to return a summary of
        :return: <json> A summarized version of the card object in cards[boardID][boards]
        """
        for board in self.boards.keys():
            boardID = board
            for card in self.cards:
                if cardID in self.cards[boardID].keys():
                    myCard = {'Board':'','Description':'','Status':'','DueDate':'','Members':'','LastUpdate':'','URL':''}
                    myCard['Board'] = self.boards[boardID]['name']
                    myCard['Description'] = self.cards[boardID][cardID]['name']
                    listID = self.cards[boardID][cardID]['idList']
                    myCard['Status'] = self.lists[boardID][listID]['name']
                    myCard['DueDate'] = self.cards[boardID][cardID]['due']
                    myCard['LastUpdate'] = self.cards[boardID][cardID]['dateLastActivity']
                    myCard['URL'] = self.cards[boardID][cardID]['url']
                    myCard['Members'] = dict()
                    for memberID in self.cards[boardID][cardID]['idMembers']:
                        memberUserName = self.members[memberID]['username']
                        myCard['Members'][memberUserName] = self.members[memberID]['fullName']
                    return myCard

        return "Card " + cardID + " not found"