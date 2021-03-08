# Compétition d'algorithmie présentée par

![CFIUL](a649dadf42dfe57e532f09a9fa7eb187.png)

![AEGLO](98abe3e59440438da9a811c1326f4d19.png)


# Introduction

Après s'être fait dépassé par Elon Musk au classement mondial, notre bon ami Bezos a décidé de step up son game et décide d'investir encore plus de ressources dans la livraison par drones, évidemment c'était avant de redevenir premier à cause qu'un investissement dans les bitcoins est aussi volatile qu'un gallon d'éther. Pour mener à terme ce projet, c'est bien beau bâtir des drones et offrir des pots de vin aux agents pour avoir les accès au ciel, il faut aussi faire un système de gestion.

# Tâche

On vous donne une liste de commandes et une liste des entrepôts ainsi que leur produits disponibles et vous devez organiser les drones de façon a remplir le plus de commandes possible dans le temps imparti.

# Description du problème

## Carte 

La simulation prendra place sur un plan cartésien **fermé** et **non-cylique**, donc les drones ne pourront par sortir des bordures de la carte et ne pourront pas non plus traverser d'une bordure à l'autre instantanément. Par contre, comme les drones peuvent voler, il sont capable de survoler n'importe quelle cellule de la carte (supposont qu'il n'y a pas d'aéroport dans la ville).

Chaque cellule sera identifiée par une paire d'entiers [_r_, _c_] (rangée, colonne; chacun limité par la taille de la carte définie au début du fichier)

## Produits

Il y a un catalogue limité de produits disponibles pour la livraison et chaque type possède un poids fixe, déterminé au préalable par le challenge.

- _**N.B: Chaque produit est disponible en, au moins, un exemplaire dans la carte et le poids d'un produit sera toujours inférieur à la capacité de charge d'un drone.**_

## Entrepôts

Les entrepôts ainsi que leur emplacements sont déterminés au début du fichier de challenge. Il est garanti que deux entrepôts ne seront jamais sur la même cellule. Au début de la simulation, les entrepôts seront stockés avec une quantité limitée de chaque type de produit, cependant il est possible que certains types de produits ne se retrouvent pas dans un entrepôt. Malgré que les entrepôts ne sont pas remplis au fil de la simulation, il est toujours possible de transférer des produits entre eux. Aucune limite de capacité n'est imposée.

## Commandes

Chaque commande possède une liste de produits, ces derniers se trouvant en un ou plusieurs exemplaires. De plus, une commande possède une cellule à laquelle faire la livraison et elle est garantie de ne jamais tomber sur un entrepôt.

Pour compléter une livraison, il ne suffit que de livrer les produits requis à l'endroit spécifié peu importe l'ordre. Il est tout à fait possible de séparer la commande en plusieurs drones et il n'est pas obligatoire de tout livrer en même temps.

Il est garanti qu'il y aura toujours assez de produits disponibles dans l'ensemble des entrepôts pour remplir chacune des commandes.

Pour finir, il n'est pas nécessaire de remplir chacune des commandes, le but est d'en faire le plus possible.