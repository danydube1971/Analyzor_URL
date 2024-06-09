# Analyzor_URL

Le script Analyzor_URL.py est un outil graphique permettant de vérifier la validité des liens dans un fichier HTML.

![Analyzor_URL](https://github.com/danydube1971/Analyzor_URL/assets/74633244/8e7dcef6-58bf-4b3f-9d9d-2c9890048859)

### Testé dans Linux Mint 21.3 sous Python3.11


# Installation des Pré-requis

Avant de commencer, assurez-vous que vous avez installé les dépendances nécessaires. Ce script nécessite Python et quelques bibliothèques supplémentaires.

  ## Installez Python (si ce n'est pas déjà fait) :

Assurez-vous que vous avez Python 3.10 ou supérieur installé sur votre système.

  Installez les Bibliothèques Requises :
Ouvrez un terminal et exécutez la commande suivante pour installer les dépendances :

      pip install requests urllib3 beautifulsoup4 pyqt5
       
# Étapes pour Utiliser le Script

  1. Lancer le Script :
Pour démarrer le script, ouvrez un terminal et exécutez la commande suivante :

       `python Analyzor_URL.py`
  
  2. Charger un Fichier HTML :

        ◦ Cliquez sur le bouton "Charger un fichier HTML".
     
        ◦ Une boîte de dialogue s'ouvre, vous permettant de sélectionner le fichier HTML que vous souhaitez analyser.
     
        ◦ Sélectionnez le fichier et cliquez sur "Ouvrir".
     
        ◦ Le script affiche le nombre de liens trouvés dans le fichier juste en dessous du bouton.
     
  3. Vérifier les Liens :

        ◦ Une fois le fichier chargé, le script commence automatiquement l'analyse des liens.
     
        ◦ Vous verrez une barre de progression indiquant l'avancement de l'analyse.
     
        ◦ Les liens sont affichés dans un tableau avec deux colonnes : Description et URL.
     
  4. Interpréter les Résultats :
     
        ◦ Les liens valides s'affichent normalement.
     
        ◦ Les liens cassés sont marqués comme "LIEN CASSÉ : [Description]" avec un fond rouge clair pour les différencier visuellement.
     
        ◦ Vous pouvez double-cliquer sur un lien dans la colonne URL pour l'ouvrir dans votre navigateur par défaut.

     **Dû à la complexité de l’analyse de certains serveurs DNS, veuillez vérifier les « Liens cassés » en double-cliquant sur l’url.**
 
  6. Arrêter l'Analyse (optionnel) :
     
        ◦ Si vous souhaitez interrompre l'analyse à tout moment, cliquez sur le bouton "Stop".
     
        ◦ L'analyse se termine et vous pouvez consulter les résultats déjà obtenus.

        
