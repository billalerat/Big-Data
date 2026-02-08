"""
Module de génération des messages FHIR pour observations de pression artérielle.
Conforme au standard HL7 FHIR pour les ressources Observation.

Auteur: Projet Big-Data - Monitoring Pression Artérielle
Date: 2026
"""

import json
import os
import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any
from faker import Faker

# Configuration
fake = Faker('fr_FR')
random_seed = os.getenv('FHIR_RANDOM_SEED')
if random_seed:
    Faker.seed(int(random_seed))  # Reproductibilite optionnelle via env var

# Seuils médicaux de pression artérielle (mmHg)
THRESHOLDS = {
    'systolic': {
        'normal_min': 90,
        'normal_max': 119,  # < 120
        'elevated_min': 120,
        'elevated_max': 129,
        'stage1_min': 130,
        'stage1_max': 139,
        'stage2_min': 140,
        'crisis_min': 181,
        'hypotension': 90  # < 90
    },
    'diastolic': {
        'normal_min': 60,
        'normal_max': 79,  # < 80
        'stage1_min': 80,
        'stage1_max': 89,
        'stage2_min': 90,
        'crisis_min': 121,
        'hypotension': 60  # < 60
    }
}


class FHIRObservationGenerator:
    """
    Générateur de messages FHIR pour les observations de pression artérielle.
    """
    
    @staticmethod
    def generate_patient_id() -> str:
        """Génère un identifiant unique de patient."""
        return f"PAT-{uuid.uuid4().hex[:8].upper()}"
    
    @staticmethod
    def generate_observation_id() -> str:
        """Génère un identifiant unique d'observation."""
        return f"OBS-{uuid.uuid4().hex[:12].upper()}"
    
    @staticmethod
    def generate_blood_pressure(abnormal: bool = False) -> Dict[str, int]:
        """
        Génère des valeurs de pression artérielle.
        
        Args:
            abnormal: Si True, génère une pression anormale
            
        Returns:
            Dict avec systolic et diastolic
        """
        if abnormal:
            # Génère une pression anormale selon les categories
            choice = fake.random_int(0, 4)
            if choice == 0:
                # Elevated: 120-129 et < 80
                return {
                    'systolic': fake.random_int(120, 129),
                    'diastolic': fake.random_int(60, 79)
                }
            elif choice == 1:
                # Hypertension stage 1
                return {
                    'systolic': fake.random_int(130, 139),
                    'diastolic': fake.random_int(80, 89)
                }
            elif choice == 2:
                # Hypertension stage 2
                return {
                    'systolic': fake.random_int(140, 180),
                    'diastolic': fake.random_int(90, 120)
                }
            elif choice == 3:
                # Hypertensive crisis
                return {
                    'systolic': fake.random_int(181, 220),
                    'diastolic': fake.random_int(121, 140)
                }
            else:
                # Hypotension
                return {
                    'systolic': fake.random_int(70, 89),
                    'diastolic': fake.random_int(40, 59)
                }
        else:
            # Génère une pression normale
            return {
                'systolic': fake.random_int(90, 119),
                'diastolic': fake.random_int(60, 79)
            }
    
    @staticmethod
    def detect_anomaly(systolic: int, diastolic: int) -> Dict[str, Any]:
        """
        Détecte les anomalies de pression artérielle.
        
        Args:
            systolic: Pression systolique en mmHg
            diastolic: Pression diastolique en mmHg
            
        Returns:
            Dict avec is_anomaly et anomaly_type
        """
        is_anomaly = False
        anomaly_types = []

        # Hypotension (priorite si en dessous des seuils)
        if systolic < THRESHOLDS['systolic']['hypotension'] or diastolic < THRESHOLDS['diastolic']['hypotension']:
            is_anomaly = True
            if systolic < THRESHOLDS['systolic']['hypotension']:
                anomaly_types.append('HYPOTENSION_SYSTOLIC')
            if diastolic < THRESHOLDS['diastolic']['hypotension']:
                anomaly_types.append('HYPOTENSION_DIASTOLIC')
            return {
                'is_anomaly': is_anomaly,
                'anomaly_types': anomaly_types,
                'category': 'HYPOTENSION'
            }

        # Hypertensive crisis
        if systolic >= THRESHOLDS['systolic']['crisis_min'] or diastolic >= THRESHOLDS['diastolic']['crisis_min']:
            is_anomaly = True
            anomaly_types.append('HYPERTENSIVE_CRISIS')
            return {
                'is_anomaly': is_anomaly,
                'anomaly_types': anomaly_types,
                'category': 'HYPERTENSIVE_CRISIS'
            }

        # Hypertension stage 2
        if systolic >= THRESHOLDS['systolic']['stage2_min'] or diastolic >= THRESHOLDS['diastolic']['stage2_min']:
            is_anomaly = True
            if systolic >= 140:
                anomaly_types.append('HYPERTENSION_SYSTOLIC')
            if diastolic >= 90:
                anomaly_types.append('HYPERTENSION_DIASTOLIC')
            return {
                'is_anomaly': is_anomaly,
                'anomaly_types': anomaly_types,
                'category': 'HYPERTENSION_STAGE_2'
            }

        # Hypertension stage 1
        if (
            THRESHOLDS['systolic']['stage1_min'] <= systolic <= THRESHOLDS['systolic']['stage1_max']
            or THRESHOLDS['diastolic']['stage1_min'] <= diastolic <= THRESHOLDS['diastolic']['stage1_max']
        ):
            is_anomaly = True
            if THRESHOLDS['systolic']['stage1_min'] <= systolic <= THRESHOLDS['systolic']['stage1_max']:
                anomaly_types.append('HYPERTENSION_SYSTOLIC')
            if THRESHOLDS['diastolic']['stage1_min'] <= diastolic <= THRESHOLDS['diastolic']['stage1_max']:
                anomaly_types.append('HYPERTENSION_DIASTOLIC')
            return {
                'is_anomaly': is_anomaly,
                'anomaly_types': anomaly_types,
                'category': 'HYPERTENSION_STAGE_1'
            }

        # Elevated
        if (
            THRESHOLDS['systolic']['elevated_min'] <= systolic <= THRESHOLDS['systolic']['elevated_max']
            and diastolic <= THRESHOLDS['diastolic']['normal_max']
        ):
            return {
                'is_anomaly': False,
                'anomaly_types': [],
                'category': 'ELEVATED'
            }

        # Normal
        return {
            'is_anomaly': False,
            'anomaly_types': [],
            'category': 'NORMAL'
        }
    
    @staticmethod
    def create_fhir_observation(
        patient_id: str,
        systolic: int,
        diastolic: int,
        observation_date: datetime = None
    ) -> Dict[str, Any]:
        """
        Crée une ressource FHIR Observation pour la pression artérielle.
        
        Args:
            patient_id: Identifiant du patient
            systolic: Pression systolique en mmHg
            diastolic: Pression diastolique en mmHg
            observation_date: Date de l'observation (par défaut: maintenant)
            
        Returns:
            Dict représentant la ressource FHIR Observation
        """
        if observation_date is None:
            observation_date = datetime.now(timezone.utc)
        
        observation_id = FHIRObservationGenerator.generate_observation_id()
        
        # Détection d'anomalies
        anomaly_info = FHIRObservationGenerator.detect_anomaly(systolic, diastolic)
        
        # Construction de la ressource FHIR Observation
        observation = {
            "resourceType": "Observation",
            "id": observation_id,
            "status": "final",
            "category": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                            "code": "vital-signs",
                            "display": "Vital Signs"
                        }
                    ]
                }
            ],
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "85354-9",
                        "display": "Blood pressure panel with all children optional"
                    }
                ]
            },
            "subject": {
                "reference": f"Patient/{patient_id}"
            },
            "effectiveDateTime": observation_date.isoformat().replace("+00:00", "Z"),
            "issued": observation_date.isoformat().replace("+00:00", "Z"),
            "component": [
                {
                    "code": {
                        "coding": [
                            {
                                "system": "http://loinc.org",
                                "code": "8480-6",
                                "display": "Systolic blood pressure"
                            }
                        ]
                    },
                    "valueQuantity": {
                        "value": systolic,
                        "unit": "mmHg",
                        "system": "http://unitsofmeasure.org",
                        "code": "mm[Hg]"
                    }
                },
                {
                    "code": {
                        "coding": [
                            {
                                "system": "http://loinc.org",
                                "code": "8462-4",
                                "display": "Diastolic blood pressure"
                            }
                        ]
                    },
                    "valueQuantity": {
                        "value": diastolic,
                        "unit": "mmHg",
                        "system": "http://unitsofmeasure.org",
                        "code": "mm[Hg]"
                    }
                }
            ],
            "interpretation": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                            "code": "A" if anomaly_info['is_anomaly'] else "N",
                            "display": "Abnormal" if anomaly_info['is_anomaly'] else "Normal"
                        }
                    ]
                }
            ],
            # Métadonnées personnalisées pour le projet
            "extension": [
                {
                    "url": "http://example.com/fhir/StructureDefinition/anomaly-detection",
                    "valueBoolean": anomaly_info['is_anomaly']
                },
                {
                    "url": "http://example.com/fhir/StructureDefinition/anomaly-types",
                    "valueString": ",".join(anomaly_info['anomaly_types']) if anomaly_info['anomaly_types'] else "NONE"
                },
                {
                    "url": "http://example.com/fhir/StructureDefinition/bp-category",
                    "valueString": anomaly_info['category']
                }
            ]
        }
        
        return observation


def generate_batch_observations(
    num_patients: int = 10,
    observations_per_patient: int = 3,
    anomaly_percentage: float = 0.3
) -> List[Dict[str, Any]]:
    """
    Génère un lot d'observations FHIR pour plusieurs patients.
    
    Args:
        num_patients: Nombre de patients à générer
        observations_per_patient: Nombre d'observations par patient
        anomaly_percentage: Pourcentage d'observations anormales (0.0 à 1.0)
        
    Returns:
        Liste des observations FHIR générées
    """
    observations = []
    generator = FHIRObservationGenerator()
    
    for _ in range(num_patients):
        patient_id = generator.generate_patient_id()
        
        # Générer plusieurs observations pour ce patient
        for i in range(observations_per_patient):
            # Décider si cette observation doit être anormale
            is_abnormal = fake.random.random() < anomaly_percentage
            
            # Générer la pression artérielle
            bp = generator.generate_blood_pressure(abnormal=is_abnormal)
            
            # Générer la date (observations récentes)
            observation_date = datetime.now(timezone.utc) - timedelta(hours=fake.random_int(0, 72))
            
            # Créer l'observation FHIR
            observation = generator.create_fhir_observation(
                patient_id=patient_id,
                systolic=bp['systolic'],
                diastolic=bp['diastolic'],
                observation_date=observation_date
            )
            
            observations.append(observation)
    
    return observations


def save_observations_to_file(observations: List[Dict[str, Any]], filename: str = "output/observations.json"):
    """
    Sauvegarde les observations FHIR dans un fichier JSON.
    
    Args:
        observations: Liste des observations à sauvegarder
        filename: Chemin du fichier de sortie
    """
    import os
    
    # Créer le répertoire s'il n'existe pas
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(observations, f, indent=2, ensure_ascii=False)
    
    print(f"✅ {len(observations)} observations sauvegardées dans {filename}")


def print_statistics(observations: List[Dict[str, Any]]):
    """
    Affiche des statistiques sur les observations générées.
    
    Args:
        observations: Liste des observations
    """
    total = len(observations)
    anomalies = sum(1 for obs in observations if obs['interpretation'][0]['coding'][0]['code'] == 'A')
    normal = total - anomalies
    
    print("\n" + "="*60)
    print("📊 STATISTIQUES DES OBSERVATIONS GÉNÉRÉES")
    print("="*60)
    print(f"Total observations: {total}")
    print(f"Observations normales: {normal} ({normal/total*100:.1f}%)")
    print(f"Observations anormales: {anomalies} ({anomalies/total*100:.1f}%)")
    
    # Compter les types d'anomalies
    anomaly_types = {}
    for obs in observations:
        if obs['interpretation'][0]['coding'][0]['code'] == 'A':
            types = obs['extension'][1]['valueString'].split(',')
            for atype in types:
                anomaly_types[atype] = anomaly_types.get(atype, 0) + 1
    
    if anomaly_types:
        print("\n📋 Détail des anomalies:")
        for atype, count in sorted(anomaly_types.items()):
            print(f"   - {atype}: {count}")

    # Compter les categories
    category_counts = {}
    for obs in observations:
        category = obs['extension'][2]['valueString']
        category_counts[category] = category_counts.get(category, 0) + 1

    if category_counts:
        print("\n🏷️  Détail des categories:")
        for category, count in sorted(category_counts.items()):
            print(f"   - {category}: {count}")
    
    # Patients uniques
    patients = set(obs['subject']['reference'].replace('Patient/', '') for obs in observations)
    print(f"\n👥 Patients uniques: {len(patients)}")
    print("="*60 + "\n")


if __name__ == "__main__":
    print("🏥 Génération des observations FHIR pour pression artérielle...")
    print("Veuillez patienter...\n")
    
    # Générer 10 patients avec 3 observations chacun
    observations = generate_batch_observations(
        num_patients=10,
        observations_per_patient=3,
        anomaly_percentage=0.4  # 40% d'anomalies
    )
    
    # Afficher les statistiques
    print_statistics(observations)
    
    # Sauvegarder dans un fichier
    save_observations_to_file(observations)
