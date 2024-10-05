def backbofwords_occurence(list_phrase, list_mot):
    list_backbofwords = [[0 for _ in list_mot] for _ in list_phrase]
    list_mots = [mot.lower() for mot in list_mot]
    list_phrase = [phrase.lower() for phrase in list_phrase]

    for indice in range(len(list_phrase)):
        for i, mot in enumerate(list_mots):
            if mot in list_phrase[indice]:
                split_phrase = list_phrase[indice].split()
                split_phrase = [mot.lower() for mot in split_phrase]
                list_backbofwords[indice][i] = split_phrase.count(mot)
            else:
                list_backbofwords[indice][i] = 0

    return list_backbofwords