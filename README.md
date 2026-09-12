# Dashboard Marketing — Module 8

Dashboard interactif (Streamlit) réunissant la segmentation client (M3/M4), les KPIs des
campagnes marketing (M5) et la valeur client prédite / CLV (M6).

## Contenu du dossier
- `app.py` — application Streamlit (le dashboard)
- `data/clients_dashboard.csv` — table clients fusionnée (comportement, segment, persona, CLV)
- `data/kpi_dashboard.csv` — table des campagnes marketing avec KPIs calculés (CTR, conversion, CPC, CPA, ROI)
- `requirements.txt` — dépendances Python

Ces deux fichiers CSV sont aussi régénérés directement depuis le notebook, à la fin du Module 8
(section 8.1), à partir des mêmes calculs que ceux déjà exécutés dans les Modules 3, 5 et 6 —
ainsi le dashboard reste synchronisé avec le reste du projet si les données sources changent.

## Lancer le dashboard en local
```bash
pip install -r requirements.txt
streamlit run app.py
```
Le dashboard s'ouvre automatiquement dans le navigateur sur `http://localhost:8501`.

## Lancer depuis Google Colab
Streamlit ne s'exécute pas cellule par cellule comme Jupyter : il faut lancer un petit serveur
puis exposer son port publiquement, par exemple avec `localtunnel` :
```python
!pip install streamlit -q
!npm install -g localtunnel -q
!streamlit run app.py &>/content/logs.txt &
!npx localtunnel --port 8501
```
Le lien fourni par `localtunnel` ouvre le dashboard.

## Fonctionnalités
- **Filtres interactifs** (segment/persona, canal marketing, tranche d'âge) qui recalculent tous
  les indicateurs et graphiques.
- **Onglet Segmentation** : projection ACP des clients, répartition des personas, profils moyens.
- **Onglet Performance des campagnes** : ROI et CPA par campagne, KPIs moyens par canal.
- **Onglet Valeur client (CLV)** : CLV réelle vs prédite, clients à forte valeur.
- **Onglet Explorateur** : tables complètes + export CSV des données filtrées.
