class Joke:

  def __init__(self, id, contents):
    self.id = id
    self.contents = contents

  def __str__(self):
    return self.contents.encode('utf-8')
