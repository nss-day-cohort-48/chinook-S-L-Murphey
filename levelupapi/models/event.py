from django.db import models



class Event(models.Model):
    """Event Model
    Fields:
        host (ForeignKey): the user that made the event
        game (ForeignKey): the game associated with the event
        date (DateField): The date of the event
        time (TimeFIeld): The time of the event
        description (TextField): The text description of the event
        title (CharField): The title of the event
        attendees (ManyToManyField): The gamers attending the event
    """
    host = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name='events')
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField()
    description = models.TextField()
    title = models.CharField(max_length=100)
    attendees = models.ManyToManyField("Gamer", through="EventGamer", related_name="attending")

    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value

    @property
    def attendees_count(self):
        return self.__attendees_count

    @attendees_count.setter
    def attendees_count(self, value):
        self.__attendees_count = value

    def __str__(self) -> str:
        return f'{self.game.name} on {self.date} hosted by {self.host}'