from collections import defaultdict, Counter
from random import choice


def get_trigrams(text):
    tokens = text.split()
    filtered_trigrams = defaultdict(list)
    for i in range(len(tokens) - 2):
        filtered_trigrams[(tokens[i], tokens[i + 1])].append(tokens[i + 2])
    sorted_trigrams = {head: Counter(tails) for head, tails in filtered_trigrams.items()}
    for head, tails in sorted_trigrams.items():
        sorted_trigrams[head] = [(tail, tails[tail])
                                 for tail in sorted(tails,
                                                    key=tails.get,
                                                    reverse=True)]
    return sorted_trigrams


def create_sentence(beginning_heads, trigrams):
    head = choice(beginning_heads)
    sentence = []
    sentence.extend(head)
    while True:
        head = tuple(sentence[-2:])
        tail = trigrams[head][0][0]
        sentence.append(tail)
        if tail.endswith(('.', '!', '?')):
            if len(sentence) < 5:
                head = choice(beginning_heads)
                continue
            else:
                return ' '.join(sentence)


if __name__ == '__main__':
    filename = input()
    with open(filename, 'r', encoding='utf-8') as file:
        trigrams = get_trigrams(file.read())
        beginning_heads = [head for head in trigrams
                           if head[0].istitle()
                           and not head[0].endswith(('!', '.', '?'))
                           and not head[1].endswith(('!', '.', '?'))]
        for _ in range(10):
            print(create_sentence(beginning_heads, trigrams))