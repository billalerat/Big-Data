# 🏥 Projet Big-Data : Monitoring de Pression Artérielle

Architecture complète pour la surveillance des patients basée sur des données médicales structurées en FHIR (Fast Healthcare Interoperability Resources).

## 📋 Vue d'ensemble du projet

Ce projet vise à concevoir et déployer une architecture permettant :
- ✅ Recevoir des données médicales structurées (format FHIR)
- ✅ Les traiter en temps réel via Kafka
- ✅ Analyser ces données grâce à un module de classification
- ✅ Identifier les anomalies et niveaux de risque
- ✅ Indexer les cas critiques dans Elasticsearch
- ✅ Visualiser avec Kibana
- ✅ Stocker les cas normaux en fichiers JSON locaux

---

## 🚀 Étapes du projet

### **ÉTAPE 1 : Génération des Messages FHIR** ✅ EN COURS

#### Objectif
Implémenter un module Python pour générer des messages FHIR au format JSON, contenant des observations de pression artérielle (systolique et diastolique) pour différents patients.

#### Fichiers concernés
- `step1_fhir_generation/fhir_generator.py` : Module principal de génération FHIR
- `step1_fhir_generation/requirements.txt` : Dépendances Python
- `output/observations.json` : Fichier de sortie avec les observations générées

#### Installation

1. **Créer un environnement virtuel**
```bash
python3.14 -m venv venv
source venv/bin/activate  # Sur Windows: venv\\Scripts\\activate
```

2. **Installer les dépendances**
```bash
cd step1_fhir_generation
pip install -r requirements.txt
```

3. **Exécuter le générateur**
```bash
python fhir_generator.py
```

#### Sortie attendue
```
🏥 Génération des observations FHIR pour pression artérielle...
Veuillez patienter...

============================================================
📊 STATISTIQUES DES OBSERVATIONS GÉNÉRÉES
============================================================
Total observations: 30
Observations normales: 18 (60.0%)
Observations anormales: 12 (40.0%)

📋 Détail des anomalies:
   - HYPERTENSION_DIASTOLIC: 3
   - HYPERTENSION_SYSTOLIC: 5
   - HYPOTENSION_SYSTOLIC: 4

👥 Patients uniques: 10
============================================================

✅ 30 observations sauvegardées dans output/observations.json

📝 Exemple d'observation FHIR générée:
------------------------------------------------------------
{
  "resourceType": "Observation",
  "id": "OBS-ABC123DE",
  ...
}
```

---

## 📚 Concepts FHIR utilisés

### Ressource Observation
La ressource FHIR **Observation** est utilisée pour capturer les mesures et assertions cliniques.

**Code LOINC utilisé :**
- `85354-9` : Blood pressure panel with all children optional
- `8480-6` : Systolic blood pressure
- `8462-4` : Diastolic blood pressure

### Structure des données
```json
{
  "resourceType": "Observation",
  "id": "OBS-ABC123DE",
  "status": "final",
  "code": {
    "coding": [{
      "system": "http://loinc.org",
      "code": "85354-9",
      "display": "Blood pressure panel"
    }]
  },
  "subject": {
    "reference": "Patient/PAT-ABC123DE"
  },
  "component": [
    {
      "code": { "coding": [{ "code": "8480-6", "display": "Systolic" }] },
      "valueQuantity": { "value": 120, "unit": "mmHg" }
    },
    {
      "code": { "coding": [{ "code": "8462-4", "display": "Diastolic" }] },
      "valueQuantity": { "value": 80, "unit": "mmHg" }
    }
  ]
}
```

---

## 🏥 Seuils médicaux de pression artérielle

| Catégorie | Systolique | Diastolique | Statut |
|-----------|-----------|-----------|--------|
| **Hypotension** | < 90 mmHg | < 60 mmHg | ⚠️ Anormale |
| **Normal** | 90-140 mmHg | 60-90 mmHg | ✅ Normal |
| **Hypertension** | > 140 mmHg | > 90 mmHg | ⚠️ Anormale |

---

## 🔧 Technologie utilisée - Étape 1

| Outil | Version | Usage |
|-------|---------|-------|
| Python | 3.14 | Langage principal |
| fhir.resources | >= 6.4.0 | Modélisation FHIR |
| Faker | >= 18.0.0 | Génération de données réalistes |

---

## 📁 Structure du répertoire

```
Big-Data/
├── step1_fhir_generation/
│   ├── fhir_generator.py       # Module de génération FHIR
│   └── requirements.txt         # Dépendances Python
├── output/
│   └── observations.json        # Observations générées (créé à l'exécution)
├── README.md                    # Documentation
└── .gitignore                   # Fichiers à ignorer
```

---

## ✨ Caractéristiques de la génération

### Données réalistes
- ✅ Identifiants de patients uniques (UUID)
- ✅ Identifiants d'observations uniques
- ✅ Dates réalistes (dernières 72h)
- ✅ Mesures réalistes de pression artérielle

### Anomalies détectées
- ✅ **Hypertension systolique** : systolique > 140 mmHg
- ✅ **Hypertension diastolique** : diastolique > 90 mmHg
- ✅ **Hypotension systolique** : systolique < 90 mmHg
- ✅ **Hypotension diastolique** : diastolique < 60 mmHg

### Format FHIR standard
- ✅ Conforme à la spécification HL7 FHIR R4
- ✅ Codes LOINC standardisés
- ✅ Métadonnées d'anomalies personnalisées

---

## 📞 Prochaines étapes

### **ÉTAPE 2** : Configuration de Kafka
- Setup Kafka avec Docker
- Création des topics
- Configuration Producer/Consumer

### **ÉTAPE 3** : Transmission avec Kafka
- Script Producer Python
- Script Consumer Python

### **ÉTAPE 4** : Analyse et détection d'anomalies
- Machine Learning (classification)
- Règles métier avancées

### **ÉTAPE 5** : Elasticsearch & Kibana
- Index Elasticsearch
- Dashboards Kibana
- Alertes

---

## 📖 Références

- **HL7 FHIR Standard** : https://www.hl7.org/fhir/overview.html
- **LOINC Codes** : https://loinc.org/
- **FHIR Observation** : https://www.hl7.org/fhir/observation.html

---

## 👤 Auteur
Projet Big-Data - Monitoring Pression Artérielle
Date: 2026

---

## ✅ Validation de l'ÉTAPE 1

**À valider :**
- [ ] Script génère des observations FHIR valides
- [ ] Détection des anomalies correcte
- [ ] Format JSON conforme à FHIR
- [ ] Sortie dans output/observations.json
- [ ] Statistiques affichées correctement

**Puis passer à l'ÉTAPE 2 :**
Configuration de Kafka et Docker Compose
