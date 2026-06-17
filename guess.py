import numpy as np

data = np.loadtxt('wordle-La.txt', dtype=str)

dataset = set(data)

the_word = None
#the_word = 'token'
my_guesses = [
  ('raise', '.....'),
  #('towel', 'gg.g.'),
  #('token', 'ggggg'),
  ]

def guess_to_known(guess):
  result = {'green': {}, 'yellow': {}, 'gray': set()}
  for i,l,c in zip(range(5),guess[0],guess[1]):
    if c=='g': result['green'][i] = l
    elif c=='y': result['yellow'][i] = l
    else: result['gray'].add(l)
  return result

def make_guess(guess, word):
  result = {'green': {}, 'yellow': {}, 'gray': set()}
  for i,lg,lw in zip(range(5), guess, word):
    if lg==lw: result['green'][i] = lg
    elif lg in word: result['yellow'][i] = lg
    else: result['gray'].add(lg) 
  return result

def test(guess, result):
  for i,lg in enumerate(guess):
    if lg in result['gray']: return False
    if lg != result['green'].get(i, lg): return False
  for i,l in result['yellow'].items():
    if l not in guess: return False
    if guess[i]==l: return False
  return True

def find_best_guess(word_list):
  best_guess = (0, '')
  n = len(word_list)
  for guess in word_list:
    nemesis = ('', n)
    for word in word_list:
      result = make_guess(guess, word)
      excluded = 0
      for next_guess in word_list:
        if not test(next_guess, result):
          excluded += 1
      if excluded < nemesis[1]:
        nemesis = (word, excluded)
    if nemesis[1]/n >= best_guess[0]:
      best_guess = (nemesis[1]/n, guess, nemesis[0])
  return best_guess


trials = 0

def update(known):
  global dataset, trials
  after = set()
  for word in dataset:
    if test(word, known): after.add(word)

  print(len(after), 'words remaining', end='')
  if len(after)<20: print(':', after)
  else: print()
  print('='*40)

  next_guess = find_best_guess(after)

  dataset = after
  trials += 1
  return next_guess

for my_guess in my_guesses:
  print(f'Guessed: {my_guess[0]}')
  known = guess_to_known(my_guess)
  next_guess = update(known)

while True:
  if len(known['green'])==5:
    print(f'Got it in {trials}/6: {the_word}')
    break

  print(f'Best guess: {next_guess[1]} ({next_guess[0]*100:.0f}%)')

  if the_word is None:
    the_word = np.random.choice(tuple(dataset))
    the_word = next_guess[2]
    print('*'*10, f'Set the word to {the_word}', '*'*10)

  known = make_guess(next_guess[1], the_word)
  next_guess = update(known)
