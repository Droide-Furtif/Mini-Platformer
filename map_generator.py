from walls import Wall, Spike
from collectibles import Collectible
from laser_class import Laser
from bumper_class import Bumper


class Generator:
    def __init__(self, game):
        self.GAME = game
        self.scale = self.GAME.screenWidth / 30

    def loadMap(self, filepath: str):
        # Open txt file and get lines list
        with open(filepath) as file:
            lines = file.readlines()
            file.close()
            print(lines)
            for line in lines:
                if line != "\n" and line[0] != '-':
                    x = y = w = h = r = 0
                    # String slicing
                    x = int(line[2:4])
                    print(x)
                    y = int(line[5:7])
                    print(y)
                    if line[0] in "WSL":
                        w = int(line[9:11])
                        print(w)
                        h = int(line[12:14])
                        print(h)

                    if line[0] == 'W':
                        self.GAME.wallList.append(Wall(self.GAME, x, y, w, h))
                    elif line[0] == 'S':
                        r = int(line[15])
                        self.GAME.spikeList.append(Spike(self.GAME, x, y, w, h, r))
                    elif line[0] == 'C':
                        self.GAME.coinList.append(Collectible(self.GAME, x, y))
                    elif line[0] == 'P':
                        self.GAME.player.setStartingPos((x * self.scale, y * self.scale))
                    elif line[0] == 'L':
                        r = int(line[15])
                        self.GAME.laserList.append(Laser(self.GAME, x, y, w, h, r))
                    elif line[0] == 'B':
                        self.GAME.bumperList.append(Bumper(self.GAME, x, y))
