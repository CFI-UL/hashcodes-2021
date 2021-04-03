# hashcodes-2021

Compétition organisée en partenariat avec l'AEGLO

Basée les hashcodes organisés anuellement par Google.

Ce challenge en particulier est la round de qualification de 2016.\
[Lien vers les archives](https://codingcompetitions.withgoogle.com/hashcode/archive)

## Serveur de validation

Pour lancer le serveur, il suffit de rouler la commande suivante `python launch_server.py`. Il est important d'avoir python 3 minimum.

Sinon, pour utiliser la classe de validation, on peut se baser sur la partie `__main__`. Il faut instancier la classe puis utiliser la fonction `verify` avec les données d'entrée et celles de sortie. Il faut préalablement que le texte soit séparé en une liste de lignes.

## Informations pertinentes

Nombre de participants estimés: 20

Il aurait été probablement préférable de donner le parser en python. On croyait bon de ne pas le mettre pour mettre tout le monde sur un pieds d'égalité peu importe le language.\ Or, de ce que nous avons remarqués, le fait de donner le parser aurait grandement aidé les plus faibles, les plus forts ayant passé beaucoup moins de temps sur le parser.\
De plus, nous croyons que, règle générale, ceux ayant tendance à choisir un autre language que python sont assez habitués et ne perdront pas trop de temps à recréer le parser.\
Morale de l'histoire, on croit que donner le parser aurait été une meilleure idée.
