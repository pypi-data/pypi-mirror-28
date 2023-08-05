def split_length(sentence, length):
    start = 0
    limit = length
    while True:
        if ' ' in sentence[start:start+limit]:
            while limit > 0 and sentence[start+limit] != ' ':
                limit -= 1
        else:
            # full whole line is single unit
            while (start+limit) < len(sentence) and sentence[start+limit] != ' ':
                limit += 1

        yield sentence[start:start+limit]
        start = start+limit+1
        limit = length
        if len(sentence[start:]) < length or start+limit > len(sentence):
            break

    yield sentence[start:]
