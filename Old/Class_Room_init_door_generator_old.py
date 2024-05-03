                    # ifCondition = False
                    # try:
                    #     ifCondition = isinstance(otherLoc, Room) and otherLoc.doors[otherDir] == glb.DOOR_STATUS.P_NewDoor
                    # except:
                    #     pass

                    # if ifCondition:                                                     # If we know there is a door from the other side, but it is not opened
                    #     if random.random()*100 > glb.RNG.SuddenlySecretDoor:            #   either OUR wall has a door we know the passage to,
                    #         self._doors[directionIdx] = glb.DOOR_STATUS.P_KnownDoor 
                    #     else:                                                           #   or it is a secret passage openable from the other side
                    #         self._doors[directionIdx] = glb.DOOR_STATUS.U_NoDoorHandle  
                    # elif random.random()*100 < glb.RNG.RandomDoorSpawn:
                    #     if isinstance(otherLoc, Room):
                    #         self._doors[directionIdx] = glb.DOOR_STATUS.P_KnownDoor
                    #     else:
                    #         self._doors[directionIdx] = glb.DOOR_STATUS.P_NewDoor
                    #     glb.CH_OPENINGS += 1