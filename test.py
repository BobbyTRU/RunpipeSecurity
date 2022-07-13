import re

pattern = r'[a-z_A-Z0-9]+\([^\)]*?'


myString = "test(func(),param)"

print(re.findall(pattern,myString))
