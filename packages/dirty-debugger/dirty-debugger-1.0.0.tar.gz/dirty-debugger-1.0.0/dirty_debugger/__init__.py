def log(message):
    with open('/tmp/dirty-debuuger.log', 'a') as f:
            f.write(message + '\n')
