import requests
from joke import Joke

def joke():
  r = requests.get('https://icanhazdadjoke.com', headers={"Accept":"application/json"})
  raw_joke = r.json();
  joke = Joke(raw_joke['id'], raw_joke['joke'])
  return joke
