import random

class PersonalAssistant:
  def provide_tip(self):
      tips = [
          "Take regular breaks to improve concentration.",
          "Prioritize your tasks using the Eisenhower Box.",
          "Set specific goals for each work session."
      ]
      return random.choice(tips)

  def respond_to_faq(self, question):
      faq_responses = {
          "how to improve focus": "Try the Pomodoro technique to maintain focus.",
          "best productivity tools": "Consider using Trello for task management."
      }
      return faq_responses.get(question.lower(), "I'm not sure about that.")