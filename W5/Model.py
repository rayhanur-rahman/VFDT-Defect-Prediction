class Weather:
    def __init__(self, outlook, temp, humid, wind, play):
        self.outlook = outlook
        self.temp = temp
        self.humid = humid
        self.wind = wind
        self.play = play
        self.tempRangeMin = None
        self.tempRangeMax = None
