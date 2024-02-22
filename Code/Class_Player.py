class player():
    # The max value of something is the highest it can go
    def __init__(self, Health=100, Stamina=100, Magic=100):
        self._maxHealth  = self._topHealth  = self._curHealth  = 100 
        self._maxStamina = self._topStamina = self._curStamina = 100 
        self._maxMagic   = self._topMagic   = self._curMagic   = 100

    def __change_max(self, NewVal, MaxTrait, TopTrait, CurTrait):
        diff = NewVal - MaxTrait
        if diff >= 0:
            MaxTrait += diff
            TopTrait += diff
            CurTrait += diff
        else:
            if MaxTrait - diff <= 0:
                MaxTrait = TopTrait = CurTrait = 0
            else: 
                MaxTrait -= diff
                if TopTrait > MaxTrait:
                    TopTrait = MaxTrait
                if CurTrait > MaxTrait:
                    CurTrait = MaxTrait
        return MaxTrait, TopTrait, CurTrait
    

    def __change_top(self, NewVal, MaxTrait, TopTrait, CurTrait):
        diff = NewVal - TopTrait
        if diff >= 0:
            if TopTrait + diff > MaxTrait:
                diff = MaxTrait - TopTrait
            MaxTrait += diff
            CurTrait += diff
        else:
            if TopTrait - diff <= 0:
                TopTrait = CurTrait = 0
            else:
                TopTrait -= diff
                if CurTrait > TopTrait:
                    CurTrait = TopTrait
        return TopTrait, CurTrait


    def __change_cur(self, NewVal, TopTrait, CurTrait):
        diff = NewVal - CurTrait
        if diff >= 0:
            CurTrait += diff
            if CurTrait > TopTrait:
                CurTrait = TopTrait
        else:
            CurTrait = 0
        return CurTrait


    @property
    def maxHealth(self):
        return self._maxHealth
    
    @maxHealth.setter
    def maxHealth(self, NewVal):
        self._maxHealth, self._topHealth, self._curHealth = self.__change_max(NewVal, self._maxHealth, self._topHealth, self._curHealth)


    @property
    def topHealth(self):
        return self._topHealth
    
    @topHealth.setter
    def topHealth(self, NewVal):
        self._topHealth, self._curHealth = self.__change_top(NewVal, self._maxHealth, self._topHealth, self._curHealth)


    @property
    def curHealth(self):
        return self._curHealth
    
    @curHealth.setter
    def curHealth(self, NewVal):
        self._curHealth = self.__change_cur(NewVal, self._topHealth, self._curHealth)


    @property
    def maxStamina(self):
        return self._maxStamina
    
    @maxStamina.setter
    def maxStamina(self, NewVal):
        self._maxStamina, self._topStamina, self._curStamina = self.__change_max(NewVal, self._maxStamina, self._topStamina, self._curStamina)


    @property
    def topStamina(self):
        return self._topStamina
    
    @topStamina.setter
    def topStamina(self, NewVal):
        self._topStamina, self._curStamina = self.__change_top(NewVal, self._maxStamina, self._topStamina, self._curStamina)


    @property
    def curStamina(self):
        return self._curStamina
    
    @curStamina.setter
    def curStamina(self, NewVal):
        self._curStamina = self.__change_top(NewVal, self._topStamina, self._curStamina)


    @property
    def maxMagic(self):
        return self._maxMagic
    
    @maxMagic.setter
    def maxMagic(self, NewVal):
        self._maxMagic, self._topMagic, self._curMagic = self.__change_max(NewVal, self._maxMagic, self._topMagic, self._curMagic)


    @property
    def topMagic(self):
        return self._topMagic
    
    @topMagic.setter
    def topMagic(self, NewVal):
        self._topMagic, self._curMagic = self.__change_top(NewVal, self._maxMagic, self._topMagic, self._curMagic)


    @property
    def curMagic(self):
        return self._curMagic
    
    @curMagic.setter
    def curMagic(self, NewVal):
        self._curMagic = self.__change_top(NewVal, self._topMagic, self._curMagic)

