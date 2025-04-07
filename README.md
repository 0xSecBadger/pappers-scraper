# 🔍 Pappers Scraper

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> Un outil puissant pour rechercher et extraire des informations sur les entreprises françaises depuis Pappers.fr

## ✨ Fonctionnalités

- 🚀 Recherche rapide d'entreprises
- 📊 Affichage des résultats en tableau ou en détail
- 🎨 Interface en ligne de commande colorée
- 📝 Informations détaillées (SIREN, statut, dirigeants, etc.)
- 🔄 Pagination automatique des résultats

## 📋 Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

## 🚀 Installation

1. Clonez le repository :
```bash
git clone https://github.com/0xSecBadger/pappers-scraper.git
cd pappers-scraper
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## 💻 Utilisation

### Recherche simple
```bash
python pappers_scraper.py "Nom de l'entreprise"
```

### Affichage en tableau
```bash
python pappers_scraper.py "Nom de l'entreprise" --tab
```

## 📝 Exemple de sortie

### Mode tableau
```
┌────┬──────────────────┬────────────┬─────────┬─────────────┬────────────┐
│ №  │ Nom             │ SIREN      │ Statut  │ Création    │ Dirigeants │
├────┼──────────────────┼────────────┼─────────┼─────────────┼────────────┤
│ 1  │ Example SARL    │ 123456789  │ 🟢 Active│ 01/01/2020 │ John Doe   │
└────┴──────────────────┴────────────┴─────────┴─────────────┴────────────┘
```

### Mode détaillé
```
═══ Example SARL ═══
📊 Informations principales
├─ SIREN: 123456789
├─ Statut: Active
└─ Création: 01/01/2020
```

## 🛠️ Configuration

Le script utilise l'API Pappers.fr. Un token API est inclus par défaut, mais vous pouvez le modifier dans le fichier `pappers_scraper.py` :

```python
self.api_token = "votre_token_api"
```

## 📚 Documentation de l'API

Pour plus d'informations sur l'API Pappers, consultez la [documentation officielle](https://api.pappers.fr/documentation).

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push sur la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- [Pappers.fr](https://www.pappers.fr) pour leur excellente API
- La communauté Python pour les packages utilisés

---
<p align="center">
  Développé avec ❤️ pour la communauté
</p>