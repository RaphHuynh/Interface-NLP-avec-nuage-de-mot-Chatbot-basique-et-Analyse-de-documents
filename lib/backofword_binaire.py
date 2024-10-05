def backbofwordsBinaire(list_phrase, list_mot):
    list_backbofwords = [[0 for _ in list_mot] for _ in list_phrase]
    list_phrase = [phrase.lower() for phrase in list_phrase]
    list_mot = [mot.lower() for mot in list_mot]

    for indice in range(len(list_phrase)):
        for mot in list_phrase[indice].split():
            if mot in list_mot:
                list_backbofwords[indice][list_mot.index(mot)] = 1
            else:
                list_backbofwords[indice][list_mot.index(mot)] = 0

    return list_backbofwords