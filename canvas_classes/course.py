class Course:
    def __init__(self, data):
        self.is_valid = "name" in data
        if self.is_valid:
            self.name = data["name"]
            self.id = data["id"]

    def __str__(self):
        if self.is_valid:
            return self.name
        return "Private Course"
    
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name
        }
    