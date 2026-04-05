import sqlite3, re
conn = sqlite3.connect('data/leaderboard.sqlite')
row = conn.execute('SELECT raw FROM Source LIMIT 1').fetchone()
conn.close()
raw = row[0]

from bs4 import BeautifulSoup
soup = BeautifulSoup(raw, 'html.parser')
scripts = soup.find_all('script')
big_script = None
for s in scripts:
    if len(s.string or '') > 50000 and 'models' in (s.string or ''):
        big_script = s.string
        break

print(f'Big script len: {len(big_script)}')

# Find the actual escaped sequence
models_search = '\\"models":['
idx = big_script.find(models_search)
print(f'Index of escaped models pattern: {idx}')

# Look for the push call start
push_idx = big_script.find('self.__next_f.push')
print(f'Push call at: {push_idx}')

# From earlier we know the data is in a push call with index "18:"
push18_idx = big_script.find('"18:')
print(f'"18:" at: {push18_idx}')
print('Around it:', repr(big_script[push18_idx:push18_idx+100]))

# Print first 200 chars
print('First 200:', repr(big_script[:200]))
