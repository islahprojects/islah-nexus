from chief_omega import ChiefOmega
from config.constants import ICF_CONSTANTS

# Initialize Gate
gate = ChiefOmega(ICF_CONSTANTS())

# Test Payload from UI
payload = {
    'sigma': 0.85,
    'ai_influence': 0.04,
    'metadata': {
        'provenance_chain': ['UI_ROOT'],
        'owner_key': 'Krimerra13',
        'consent_state': 'EXPLICIT',
        'human_override': True
    }
}

print(gate(payload))
