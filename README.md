# projet_nlp_info708

## Comment faire fonctionner l'application ?
- Installer les librairies avec la commande :
  
```
    pip install -r requirements.txt -v
```

- Pour allumer l'application :
  
    Reste dans le document de l'application est lancé la commande ci-dessous

```
    python main.py
```

## Comment utiliser l'application ?
- Choisir la bonne langue en fonction du fichier à lire
- Il n'y a que le français et l'anglais de disponible
- Si vous cochez les stopwords cela va supprimer du document les stopwords de la langue choisie.
- Apres avoir choisi votre document et la phrase que vous cherchez il suffit de cliquer sur le bouton générer
- Apres la génération vous pouvez changer sans soucis les paramètres du menu, cela mettra les valeurs à jour automatiquement

## Que fait l'application ?
L'application permet d'analayser des textes au format.txt en utilisant des méthodes basiques de traitement de langage naturel.
On peut donc retrouver comme résultat les k plus proches phrases d'une phrase d'un document. Voir graphiquement les distances de chaque phrase entre la phrase sélectionnée. On y retrouve aussi la liste des fréquences des mots les plus utilisés et leur répartition en pourcentage ainsi que deux autres graphiques directement expliqués dans l'application.