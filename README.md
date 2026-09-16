# Application bancaire

Application de gestion financière personnelle développée en Python avec PySide6. Elle permet d'importer des relevés bancaires au format CSV, d'organiser les transactions, de visualiser les tendances par mois et par catégorie, et de configurer des exclusions personnalisées.

## Fonctionnalités

- Import de fichiers CSV de transactions bancaires
- Stockage local des données avec SQLite via SQLAlchemy
- Tableau de bord financier mensuel
- Analyse des revenus et des dépenses par catégorie
- Suivi de l'épargne avec graphiques
- Recherche et filtrage des transactions par période
- Gestion des exclusions de catégories ou de libellés
- Interface graphique simple et rapide

## Prérequis

- Python 3.10 ou plus récent
- PySide6
- SQLAlchemy

## Installation

1. Cloner le dépôt :

   ```bash
   git clone https://github.com/Stragon24/Application_bancaire.git
   cd Application_bancaire
   ```

2. Créer un environnement virtuel (recommandé) :

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Installer les dépendances :

   ```bash
   pip install PySide6 SQLAlchemy
   ```

## Lancement

Depuis la racine du projet :

```bash
python main.py
```

L'application crée automatiquement la base de données locale au démarrage si elle n'existe pas.

## Utilisation

### Importer des transactions

- Cliquer sur le bouton Importer CSV dans la barre d'outils.
- Sélectionner un fichier CSV comportant les données bancaires.
- Les transactions sont importées dans la base SQLite.
- Les mois déjà présents ne sont pas réimportés.

### Consulter le tableau de bord

- Sélectionner une année et un mois.
- Visualiser le solde, les revenus, les dépenses et les répartitions par catégorie.
- Masquer ou configurer les éléments exclus selon vos besoins.

### Gérer les exclusions

- Ouvrir la configuration des exclusions.
- Ajouter une catégorie ou un libellé à exclure des calculs.
- Les exclusions s'appliquent aux statistiques et aux graphiques.

## Structure du projet

```text
Application_bancaire/
├── database/
│   ├── database.py
│   └── models.py
├── services/
│   ├── csv_importer.py
│   ├── database_service.py
│   └── file_service.py
├── ui/
│   ├── dialogs/
│   ├── pages/
│   └── widgets/
├── main.py
├── README.md
└── .gitignore
```

## Notes

- La base de données est stockée localement sur l'ordinateur.
- Le projet est orienté gestion personnelle et analyse budgétaire.
- Les règles d'exclusion sont entièrement personnalisables.

## Développement

Le projet suit une architecture simple orientée interface graphique :

- `main.py` : point d'entrée de l'application
- `database/` : modèles SQLAlchemy et connexion SQLite
- `services/` : import, stockage et calculs financiers
- `ui/` : pages, widgets et dialogues de l'interface

## Licence

Aucune licence spécifique n'est définie pour le moment. Le projet est destiné à un usage personnel ou interne selon les besoins du développeur.
