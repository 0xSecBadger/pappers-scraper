# Pappers Scraper

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> Un outil d'extraction d'informations sur les entreprises françaises depuis Pappers.fr

## Fonctionnalités

- Recherche d'entreprises via l'interface web de Pappers
- Affichage des résultats en tableau ou en vue détaillée
- Interface en ligne de commande avec sortie colorée
- Informations détaillées : SIREN, statut, dirigeants, etc.
- Pagination automatique des résultats
- Navigation headless avec Pyppeteer

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Connexion Internet stable

## Installation

1. Clonez le repository :
```bash
git clone https://github.com/0xSecBadger/pappers-scraper.git
cd pappers-scraper
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

### Recherche simple avec affichage détaillé
```bash
python pappers_scraper.py "Nom de l'entreprise"
```

### Affichage en tableau
```bash
python pappers_scraper.py "Nom de l'entreprise" --tab
```

## Exemple de sortie

### Mode tableau
```
+----+------------------+----------+---------+-----------+------------+
| №  | Nom             | SIREN    | Statut  | Création  | Dirigeants |
+----+------------------+----------+---------+-----------+------------+
| 1  | Example SARL    | 123456789| Active  |01/01/2020| John Doe   |
+----+------------------+----------+---------+-----------+------------+
```

### Mode détaillé
```
=== Example SARL ===
État & Identité
├─ SIREN: 123456789
├─ Statut: Active
└─ Création: 01/01/2020
```

## Fonctionnement technique

Le script utilise Pyppeteer pour :
- Lancer un navigateur Chrome en mode headless
- Naviguer sur le site Pappers.fr
- Extraire les informations via des requêtes JavaScript
- Gérer la pagination automatiquement

Note : Cette version n'utilise pas l'API REST de Pappers directement, mais simule la navigation web.

## Limitations

- Dépend de la structure du site web Pappers.fr
- Nécessite une connexion Internet stable
- Performance limitée par la navigation web simulée
- Pas d'utilisation de l'API REST officielle

## Contribution

Les contributions sont les bienvenues :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push sur la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## Améliorations possibles

1. Intégration de l'API REST officielle de Pappers
2. Ajout d'export en différents formats (CSV, JSON, Excel)
3. Cache des résultats pour éviter les requêtes répétées
4. Gestion des erreurs plus robuste
5. Tests unitaires et d'intégration

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Remerciements

- Pappers.fr pour leur service
- La communauté Python pour les packages utilisés

---
<p align="center">
  Développé pour la communauté Python française
</p>