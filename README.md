# Vérificateur de Liens HTML

![Analyzor_Url](https://github.com/user-attachments/assets/a03d8510-1733-4ef2-80cf-14007db2bfe8)


Le **Vérificateur de Liens HTML** est une application conviviale conçue pour analyser et identifier les liens brisés dans vos fichiers HTML. Idéal pour les développeurs web et les gestionnaires de contenu souhaitant assurer la qualité des liens sur leurs sites.

## Fonctionnalités

- **Analyse Rapide** : Scanne tous les liens présents dans un fichier HTML.
- **Identification des Liens Cassés** : Détecte les liens inaccessibles ou problématiques.
- **Filtrage Avancé** : Affiche uniquement les liens cassés sur demande.
- **Recherche Intelligente** : Trouve rapidement des liens spécifiques.
- **Exportation des Résultats** : Sauvegarde les résultats au format CSV.
- **Vérification SSL** : Option pour vérifier les certificats SSL des liens.

## Installation

### Prérequis

- **Python 3.6+**
- **pip** (Gestionnaire de paquets Python)

### Étapes

1. **Cloner le Dépôt**
    ```bash
    git clone [https://github.com/votre-utilisateur/votre-depot.git](https://github.com/danydube1971/Analyzor_URL)
    cd votre-depot
    ```

2. **Installer les Dépendances**
    ```bash
    pip install -r requirements.txt
    ```
    *Si `requirements.txt` n'est pas disponible, installez manuellement :*
    ```bash
    pip install requests beautifulsoup4 pyqt5
    ```

3. **Lancer l'Application**
    ```bash
    python Analyzor_Url_V4
    ```

## Utilisation

1. **Charger un Fichier HTML**
    - Cliquez sur **"Charger un fichier HTML"**.
    - Sélectionnez le fichier HTML à analyser.

2. **Analyser les Liens**
    - L'analyse démarre automatiquement après le chargement.
    - La barre de progression indique l'avancement.

3. **Afficher les Résultats**
    - **Nombre de Liens** : Affiche le total des liens analysés.
    - **Nombre de Liens Cassés** : Indique combien de liens sont brisés.
    - **Tableau des Liens** : Liste détaillée avec Description, URL et Statut.

4. **Filtrer les Liens Cassés**
    - Cochez **"Afficher seulement les liens cassés"** pour ne voir que les liens problématiques.

5. **Rechercher des Liens**
    - Utilisez la barre de recherche pour trouver des liens spécifiques.

6. **Exporter les Résultats**
    - Cliquez sur **"Exporter les résultats"**.
    - Choisissez l'emplacement et le nom du fichier.
    - L'extension `.csv` est ajoutée automatiquement si non spécifiée.

7. **Arrêter l'Analyse**
    - Cliquez sur **"Stop"** pour interrompre l'analyse en cours.

## Options Avancées

- **Vérification des Certificats SSL**
    - Activez la case **"Vérifier les certificats SSL"** pour renforcer la vérification des liens sécurisés.

## Résolution des Problèmes

- **L'application ne se lance pas** :
    - Vérifiez que Python est installé et ajouté au PATH.
    - Assurez-vous que toutes les dépendances sont correctement installées.

- **Les liens ne sont pas analysés correctement** :
    - Vérifiez le format de votre fichier HTML.
    - Assurez-vous que les liens sont dans les balises `<a>` avec l'attribut `href`.

## Contribuer

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le dépôt.
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/nom-feature`).
3. Committez vos changements (`git commit -m 'Ajout de nouvelle fonctionnalité'`).
4. Push vers la branche (`git push origin feature/nom-feature`).
5. Ouvrez une Pull Request.




