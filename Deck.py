from Card import Card


class Deck:
    def __init__(self):
        self.weapons = [Card("Rope"), Card("Pipe"), Card("Knife"), Card("Wrench"), Card("Candlestick"), Card("Revolver")]
        self.people = [Card("Yellow"), Card("Red"), Card("Purple"), Card("Green"), Card("White"), Card("Blue")]
        self.rooms = [Card("Billiards"), Card("Study"), Card("Hall"), Card("Lounge"), Card("Dining"), Card("Ballroom"), Card("Conservatory"), Card("Library"), Card("Kitchen")]