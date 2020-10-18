import re

USERNAME_PATTERN = re.compile(r"-username=(\w+)$")
print(USERNAME_PATTERN.match("-username=Horse").group(1))
