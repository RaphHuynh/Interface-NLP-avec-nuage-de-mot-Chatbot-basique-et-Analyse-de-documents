def retirer_ponctuation(doc):
    ponctuations = ['.', ',', '!', '?', ':', ';', '(', ')', '-', '_', '"', "'", '...', '—', '/']
    for ponctuation in ponctuations:
        doc = doc.replace(ponctuation, ' ')
    return doc


def supp_poc_corpus(corpus):
    corpus_sans_poc = []
    for doc in corpus:
        doc_sans_poc = retirer_ponctuation(doc)
        corpus_sans_poc.append(doc_sans_poc)
    return corpus_sans_poc


def split_phrase_mot(corpus):
    phrases = corpus.split('.')
    liste_mots = []

    for phrase in phrases:
        phrase = phrase.strip()
        if phrase:
            mots = phrase.split()
            liste_mots.extend(mots)

    return liste_mots


def split_doc_mot(corpus):
    liste_mots_totale = []

    for doc in corpus:
        mots = split_phrase_mot(doc)
        liste_mots_totale.extend(mots)

    return liste_mots_totale


def retirer_doublons(corpus):
    vus = set()
    liste_sans_doublons = []
    for mot in corpus:
        mot_lower = mot.lower()
        if mot_lower not in vus:
            liste_sans_doublons.append(mot_lower)
            vus.add(mot_lower)

    return liste_sans_doublons

def separer_phrase(contenu):
    phrases = contenu.split('.')
    phrases_temp = []
    for phrase in phrases:
        phrases_temp.extend(phrase.split('!'))
    phrases_finales = []
    for phrase in phrases_temp:
        phrases_finales.extend(phrase.split('?'))
    return [phrase.strip() for phrase in phrases_finales if phrase.strip()]