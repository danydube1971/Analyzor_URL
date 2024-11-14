# Analyzor Url V3 - Vérificateur de Liens HTML

Bienvenue dans Analyzor Url, une application Python développée avec PyQt5 qui permet d'analyser et de vérifier la validité des liens contenus dans vos fichiers HTML. Cette application offre une interface graphique intuitive pour charger des fichiers HTML, analyser leurs liens et exporter les résultats.

## 🚀 Fonctionnalités

- Chargement et analyse de fichiers HTML
- Vérification de la validité des liens en temps réel
- Interface graphique interactive avec PyQt5
- Filtrage des résultats par recherche
- Export des résultats en CSV
- Gestion des certificats SSL
- Barre de progression pour suivre l'analyse
- Affichage coloré des liens cassés

## 📋 Prérequis

- Système d'exploitation : Linux Mint Mate (ou distribution Linux compatible)
- Python 3.12
- Modules Python requis :
  - PyQt5
  - requests
  - beautifulsoup4
  - urllib3

## 💻 Installation

### 1. Vérification de Python

```bash
python3 --version
```
Assurez-vous que la version 3.12.x est installée.

### 2. Installation des dépendances

```bash
sudo apt-get update
sudo apt-get install python3-pip
pip3 install PyQt5 requests beautifulsoup4 urllib3
```

### 3. Téléchargement

Téléchargez le script `Analyzor_Url_V3.py` et placez-le dans le répertoire de votre choix.

### 4. Lancement

```bash
python3 Analyzor_Url_V3.py
```

## 🖥️ Interface Utilisateur

### Boutons et Contrôles

1. **Charger un Fichier HTML**
   - Sélection du fichier HTML à analyser
   
2. **Exporter les Résultats**
   - Sauvegarde des résultats en format CSV
   
3. **Vérifier les Certificats SSL**
   - Active/désactive la vérification SSL
   
4. **Barre de Recherche**
   - Filtre les liens en temps réel
   
5. **Stop**
   - Interrompt l'analyse en cours

### Tableau des Résultats

Le tableau affiche trois colonnes principales :

| Colonne | Description |
|---------|-------------|
| Description | Texte associé au lien (préfixé par "LIEN CASSÉ :" si non valide) |
| URL | Adresse du lien (double-clic pour ouvrir dans le navigateur) |
| Statut | État du lien avec code HTTP (coloré en rouge si cassé) |

## 📝 Utilisation

### Analyse des Liens

1. Cliquez sur "Charger un fichier HTML"
2. Sélectionnez votre fichier
3. L'analyse démarre automatiquement
4. Suivez la progression via la barre d'avancement
5. Consultez les résultats dans le tableau

### Configuration SSL

- **Activé** : Vérification complète des certificats (plus sécurisé, plus lent)
- **Désactivé** : Sans vérification SSL (plus rapide, moins sécurisé)

### Codes de Statut

- **200-399** : Lien valide
- **≥400** : Lien cassé

Exemples courants :
- 200 : OK
- 301 : Redirection permanente
- 404 : Page non trouvée
- 500 : Erreur serveur

## 🔧 Dépannage

### L'application ne démarre pas

```bash
# Vérifiez l'installation en exécutant via terminal
python3 Analyzor_Url_V3.py
```

### Liens incorrectement marqués comme cassés

1. Vérifiez votre connexion Internet
2. Contrôlez les paramètres SSL
3. Certains serveurs peuvent nécessiter une vérification manuelle

### Échec d'exportation

- Vérifiez les permissions du dossier cible
- Assurez-vous que le fichier n'est pas verrouillé

## 💡 Bonnes Pratiques

1. Utilisez des fichiers HTML bien structurés
2. Surveillez la barre de progression
3. Vérifiez manuellement les liens critiques
4. Maintenez l'application à jour

## 🤝 Support et Ressources

- [Documentation PyQt5](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [Forums Python](https://www.python.org/community/forums/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/python)

## 📄 Licence

[GPL v3]

---
Développé avec ❤️ par [Dany Dubé]
