class Player():
    # The max value of something is the highest it can go
    def __init__(self, Health=100, Stamina=100, Magic=100):
        self._maxHealth  = self._topHealth  = self._curHealth  = Health 
        self._maxStamina = self._topStamina = self._curStamina = Stamina
        self._maxMagic   = self._topMagic   = self._curMagic   = Magic
        self.show_stats = False

    def __str__(self) -> str:
        message = ''
        # 0 = type, 1 = max, 2 = top, 3 = current, 4 = RGB
        category = [('Health ', self._maxHealth, self._topHealth, self._curHealth, '\033[0;42m'),\
                    ('Stamina', self._maxStamina, self._topStamina, self._curStamina, '\033[0;43m'),\
                    ('Magic  ', self._maxMagic, self._topMagic, self._curMagic, '\033[0;44m')]
        
        # Loop through each category
        for catIdx in range(len(category)):
            # Get numerical values for each category
            # currentPercent is the percentage of the current Stat to the max Stat
            #<type>Bar is how many whitespaces to put in the Stat bar for the current, top or max value
            currentPercent = category[catIdx][3]*100/category[catIdx][1]
            currentBar = int(currentPercent/4)
            topBar = int(((category[catIdx][2] - category[catIdx][3])*100/category[catIdx][1])/4)
            maxBar = int(25 - currentBar - topBar)

            # Append to the message
            message += category[catIdx][0] + " :" + \
                       category[catIdx][4] + ' '*currentBar + \
                       '\033[0;41m' + ' '*topBar + '#'*maxBar + \
                       '\033[0m' +'| '+ str(currentPercent) +'%\n'
        return message

    def __change_max(self, NewVal, MaxTrait, TopTrait, CurTrait):
        diff = NewVal - MaxTrait
        MaxTrait = NewVal
        if MaxTrait < 0:
            CurTrait = TopTrait = MaxTrait = 0

        if diff >= 0:
            TopTrait += diff
            CurTrait += diff
        if TopTrait > MaxTrait:
            TopTrait = MaxTrait
        if CurTrait > MaxTrait:
            CurTrait = MaxTrait

        return MaxTrait, TopTrait, CurTrait
    

    def __change_top(self, NewVal, MaxTrait, TopTrait, CurTrait):
        diff = NewVal - TopTrait
        TopTrait = NewVal
        if TopTrait > MaxTrait:
            diff = MaxTrait - (TopTrait - diff)
            TopTrait = MaxTrait
        if TopTrait < 0:
            CurTrait = TopTrait = 0
        
        if diff >= 0:
            CurTrait += diff
        if CurTrait > TopTrait:
            CurTrait = TopTrait

        print(diff, MaxTrait, TopTrait, CurTrait)
        return TopTrait, CurTrait


    def __change_cur(self, NewVal, TopTrait, CurTrait):
        CurTrait = NewVal
        if CurTrait > TopTrait:
            CurTrait = TopTrait
        if CurTrait < 0:
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

    

