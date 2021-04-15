from Card import Card

#Storage class to transport playerdata between server and client
class Player():
    def __init__(self, room, id, hand):
        self.room = room
        self.id = id
        self.hand = []
        for card in hand:
            self.hand.append(card)
