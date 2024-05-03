import Code.global_vars as glb

class Location:
    def __init__(self, coords):
        # coords represnt the coordinates of this location
        self.coords = coords

        # nexCoords represent the set coordinates of all locations adjacent to us
        self.nexCoords = []
        for directionIdx in range(len(glb.DIRECTIONS)):
            xAxis = yAxis = zAxis = 0
            match directionIdx:
                case 0:         # North
                    yAxis += 1
                case 1:         # East
                    xAxis += 1
                case 2:         # South
                    yAxis -= 1
                case 3:         # West
                    xAxis -= 1  
                case 4:         # Up
                    zAxis += 1
                case 5:         # Down
                    zAxis -= 1
            self.nexCoords.append((coords[0] + xAxis, coords[1] + yAxis, coords[2] + zAxis))
