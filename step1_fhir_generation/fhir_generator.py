"""
Module de génération des messages FHIR pour observations de pression artérielle.
Conforme au standard HL7 FHIR pour les ressources Observation.

Auteur: Projet Big-Data - Monitoring Pression Artérielle
Date: 2026
"""

import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any
from faker import Faker

# Configuration
fake = Faker('fr_FR')
Faker.seed(42)  # Pour reproductibilité

# Seuils médicaux de pression artérielle (mmHg)
THRESHOLDS = {
    'systolic': {
        'normal_min': 90,
        'normal_max': 140,
        'hypotension': 90,  # < 90
        'hypertension': 140  # > 140
    },
    'diastolic': {
        'normal_min': 60,
        'normal_max': 90,
        'hypotension': 60,  # < 60
        'hypertension': 90  # > 90
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
            # Génère une pression anormale
            choice = fake.random_int(0, 3)
            if choice == 0:
                # Hypertension (systolique élevée)
                return {
                    'systolic': fake.random_int(141, 180),
                    'diastolic': fake.random_int(60, 95)
                }
            elif choice == 1:
                # Hypertension (diastolique élevée)
                return {
                    'systolic': fake.random_int(90, 140),
                    'diastolic': fake.random_int(91, 120)
                }
            elif choice == 2:
                # Hypotension (systolique basse)
                return {
                    'systolic': fake.random_int(70, 89),
                    'diastolic': fake.random_int(40, 59)
                }
            else:
                # Hypotension (diastolique basse)
                return {
                    'systolic': fake.random_int(90, 140),
                    'diastolic': fake.random_int(40, 59)
                }
        else:
            # Génère une pression normale
            return {
                'systolic': fake.random_int(90, 140),
                'diastolic': fake.random_int(60, 90)
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
        
        # Vérification systolique
        if systolic > THRESHOLDS['systolic']['hypertension']:
            is_anomaly = True
            anomaly_types.append('HYPERTENSION_SYSTOLIC')
        elif systolic < THRESHOLDS['systolic']['hypotension']:
            is_anomaly = True
            anomaly_types.append('HYPOTENSION_SYSTOLIC')
        
        # Vérification diastolique
        if diastolic > THRESHOLDS['diastolic']['hypertension']:
            is_anomaly = True
            anomaly_types.append('HYPERTENSION_DIASTOLIC')
        elif diastolic < THRESHOLDS['diastolic']['hypotension']:
            is_anomaly = True
            anomaly_types.append('HYPOTENSION_DIASTOLIC')
        
        return {
            'is_anomaly': is_anomaly,
            'anomaly_types': anomaly_types
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
            observation_date = datetime.utcnow()
        
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
                "reference": f"Patient/{{patient_id}}"
            },
            "effectiveDateTime": observation_date.isoformat() + "Z",
            "issued": observation_date.isoformat() + "Z",
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
                    "valueString": ",".join(anomaly_info['anomaly_types']) if anomaly_info['anomaly_types'] else "NORMAL"
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
            observation_date = datetime.utcnow() - timedelta(hours=fake.random_int(0, 72))
            
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
    
    # Afficher un exemple
    print("\n📝 Exemple d'observation FHIR générée:")
    print("-" * 60)
    print(json.dumps(observations[0], indent=2, ensure_ascii=False))