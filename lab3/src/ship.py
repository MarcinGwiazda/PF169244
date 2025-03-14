class Ship:
    def __init__(self,destination,voyage_duration):
        self.crew_member = []
        if isinstance(destination,str):
            self.destination=destination
        else:
            raise TypeError("Destination must be a string")
        if isinstance(voyage_duration,int):
            self.voyage_duration=voyage_duration
        else:
            raise TypeError("Voyage duration must be an integer")

    def calculate_fuel(self):
        return self.voyage_duration*100

    def add_crew_member(self,crew_member):
        if isinstance(crew_member, str):
            if crew_member == "":
                raise ValueError("Crew member cannot be empty")
            self.crew_member.append(crew_member)

        else:
            raise TypeError("Crew member must be a string")
