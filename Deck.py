from Card import Card


class Deck:
    def __init__(self):
        self.weapons = [Card("Rope"), Card("Pipe"), Card("Knife"), Card("Wrench"), Card("Candlestick"),
                        Card("Revolver")]
        self.people = [Card("Plum"), Card("Green"), Card("Scarlet"), Card("White"), Card("Peacock"), Card("Mustard")]
        self.rooms = [Card("Billiard"), Card("Study"), Card("Hall"), Card("Lounge"), Card("Dining"), Card("Ball"),
                      Card("Conservatory"), Card("Library"), Card("Kitchen")]
