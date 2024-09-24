import random

class WellnessManager:
  def send_break_reminder(self):
      return "Time to take a break! Stand up and stretch."

  def conduct_wellness_survey(self):
      questions = [
          "How are you feeling today?",
          "Did you take breaks during your work sessions?"
      ]
      return random.choice(questions)