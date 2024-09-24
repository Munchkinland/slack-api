import time

class PomodoroTimer:
  def __init__(self):
      self.pomodoro_duration = 25 * 60  # 25 minutes
      self.break_duration = 5 * 60  # 5 minutes

  def start_pomodoro(self):
      print("Pomodoro started. Focus for 25 minutes.")
      time.sleep(self.pomodoro_duration)
      print("Time for a break!")

  def start_break(self):
      print("Break started. Relax for 5 minutes.")
      time.sleep(self.break_duration)
      print("Break over. Time to get back to work!")