**Analyzor_Urls_V5.py** est une application qui analyse les liens contenus dans un fichier HTML. Grâce à une interface conviviale développée avec PyQt5, l'application permet de charger un fichier, de vérifier la validité des URLs et de visualiser les redirections ainsi que les erreurs potentielles.

L'objectif est de vous aider à identifier rapidement les liens cassés ou problématiques dans vos pages HTML.

![Analyzor_Urls](https://github.com/user-attachments/assets/c7b87ddf-494b-4495-8d0f-3e9de5680197)


* * * * *

Fonctionnalités
---------------

-   **Analyse des liens :** Vérifie la validité des URLs en effectuant des requêtes HTTP (HEAD et GET) avec gestion des redirections.

-   **Interface graphique conviviale :** Affiche les résultats dans une table avec des indicateurs visuels (couleurs pour les liens cassés).

-   **Export des résultats :** Possibilité d'exporter les données analysées en formats CSV et HTML.

-   **Options de filtrage :** Affiche uniquement les liens cassés ou filtre selon une recherche textuelle.

-   **Gestion des certificats SSL :** Option pour activer ou désactiver la vérification des certificats SSL.

* * * * *

Prérequis
---------

Avant de lancer l'application, assurez-vous d'avoir installé :

-   **Python 3.6+**

-   **Bibliothèques Python suivantes :**

    -   [Requests](https://pypi.org/project/requests/)

    -   [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)

    -   [PyQt5](https://pypi.org/project/PyQt5/)

    -   [urllib3](https://pypi.org/project/urllib3/)

Vous pouvez installer ces dépendances via pip :

```
pip install requests beautifulsoup4 PyQt5 urllib3
```

* * * * *

Utilisation
-----------

### Lancer l'application

Pour démarrer l'application, exécutez le script depuis votre terminal :

```
python Analyzor_Urls.py
```

L'interface graphique s'ouvrira et vous proposera plusieurs options.

### Charger un fichier HTML

-   Cliquez sur le bouton **"Charger un fichier HTML"**.

-   Sélectionnez le fichier HTML que vous souhaitez analyser depuis votre explorateur de fichiers.

### Analyse des liens

-   Une fois le fichier chargé, le script analyse automatiquement tous les liens (`<a href="...">`).

-   Vous verrez :

    -   Le **nombre total de liens** à analyser.

    -   Un **progress bar** indiquant l'avancement de l'analyse.

    -   La table des résultats affichant :

        -   **Description** (texte du lien)

        -   **URL** vérifiée

        -   **Statut** de l'URL (code HTTP et indication de validité)

        -   **Redirections** (chaîne des URLs en cas de redirection)

-   Les liens cassés ou invalides sont mis en évidence (fond coloré en rouge pâle).

### Exporter les résultats

Deux options d'export sont disponibles :

1.  **Exporter en CSV :**

    -   Cliquez sur le bouton **"Exporter en CSV"**.

    -   Choisissez le chemin et le nom du fichier.

    -   Le fichier CSV sera généré avec les colonnes : Description, URL, Statut, Redirections.

2.  **Exporter en HTML :**

    -   Cliquez sur le bouton **"Exporter en HTML"**.

    -   Choisissez le chemin et le nom du fichier.

    -   Un fichier HTML sera généré pour une consultation plus conviviale dans un navigateur.

* * * * *

Options et Paramètres
---------------------

-   **Afficher seulement les liens cassés :**

    -   Activez cette option via la case à cocher pour filtrer et n'afficher que les liens problématiques dans la table.

-   **Vérifier les certificats SSL :**

    -   Vous pouvez activer ou désactiver la vérification SSL selon vos besoins.

-   **Barre de recherche :**

    -   Utilisez la barre de recherche pour filtrer les liens en fonction de leur description ou URL.

-   **Bouton Stop :**

    -   Si vous souhaitez interrompre l'analyse en cours, cliquez sur le bouton **"Stop"**.

* * * * *
