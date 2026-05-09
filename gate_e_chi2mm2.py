import json

schema = [
    {"term": "liwanag", "language": "Tagalog", "script": "Latin", "meaning": "light / clarity", "uncertainty_score": 0.72, "sacred": False, "consent_token": None, "status": "CONFIRMED"},
    {"term": "kapwa", "language": "Tagalog", "script": "Latin", "meaning": "shared identity", "uncertainty_score": 0.81, "sacred": True, "consent_token": "COMMUNITY_CONSENT_001", "status": "CONFIRMED"},
    {"term": "ubuntu", "language": "Zulu", "script": "Latin", "meaning": "I am because we are", "uncertainty_score": 0.79, "sacred": True, "consent_token": "COMMUNITY_CONSENT_003", "status": "CONFIRMED"},
    {"term": "salam", "language": "Arabic", "script": "Arabic", "meaning": "peace", "uncertainty_score": 0.65, "sacred": False, "consent_token": None, "status": "CONFIRMED"},
    {"term": "karuna", "language": "Sanskrit", "script": "Devanagari", "meaning": "compassion", "uncertainty_score": 0.77, "sacred": True, "consent_token": "COMMUNITY_CONSENT_004", "status": "CONFIRMED"},
    {"term": "ayni", "language": "Quechua", "script": "Latin", "meaning": "reciprocity", "uncertainty_score": 0.88, "sacred": True, "consent_token": "COMMUNITY_CONSENT_005", "status": "CONFIRMED"},
    {"term": "ubuntu", "language": "Swahili", "script": "Latin", "meaning": "humanity", "uncertainty_score": 0.76, "sacred": False, "consent_token": None, "status": "CONFIRMED"},
    {"term": "han", "language": "Korean", "script": "Hangul", "meaning": "collective grief / resilience", "uncertainty_score": 0.83, "sacred": True, "consent_token": "COMMUNITY_CONSENT_006", "status": "CONFIRMED"},
    {"term": "hygge", "language": "Danish", "script": "Latin", "meaning": "cozy togetherness", "uncertainty_score": 0.71, "sacred": False, "consent_token": None, "status": "CONFIRMED"},
    {"term": "mamá", "language": "Spanish", "script": "Latin", "meaning": "mother", "uncertainty_score": 0.60, "sacred": False, "consent_token": None, "status": "CONFIRMED"},
    {"term": "ukweli", "language": "Swahili", "script": "Latin", "meaning": "truth", "uncertainty_score": 0.74, "sacred": False, "consent_token": None, "status": "CONFIRMED"},
    {"term": "wu wei", "language": "Chinese", "script": "Han", "meaning": "effortless action", "uncertainty_score": 0.80, "sacred": True, "consent_token": "COMMUNITY_CONSENT_007", "status": "CONFIRMED"},
    {"term": "meraki", "language": "Greek", "script": "Latin", "meaning": "doing something with soul", "uncertainty_score": 0.78, "sacred": False, "consent_token": None, "status": "CONFIRMED"},
    {"term": "noor", "language": "Urdu", "script": "Nastaliq", "meaning": "divine light", "uncertainty_score": 0.82, "sacred": True, "consent_token": "COMMUNITY_CONSENT_008", "status": "CONFIRMED"},
    {"term": "walang maiiwan", "language": "Tagalog", "script": "Latin", "meaning": "no one left behind", "uncertainty_score": 0.05, "sacred": True, "consent_token": "COMMUNITY_CONSENT_CORE", "status": "CONFIRMED"},
]

hits = []
for entry in schema:
    if entry["uncertainty_score"] >= 1.0:
        hits.append(f"SCORE TOO HIGH: {entry['term']}")
    if entry["sacred"] and not entry["consent_token"]:
        hits.append(f"MISSING CONSENT: {entry['term']}")

json.dump(schema, open("umu_schema.json", "w"), indent=2)

if hits:
    for h in hits:
        print("LAW_VII_WARNING:", h)
else:
    scripts = set(e["script"] for e in schema)
    languages = set(e["language"] for e in schema)
    print("Gate E: PASSED — schema valid")
    print("Total entries:", len(schema))
    print("Languages covered:", len(languages))
    print("Scripts covered:", len(scripts))
    print("Sacred terms with consent:", sum(1 for e in schema if e["sacred"]))
    print("Max uncertainty score:", max(e["uncertainty_score"] for e in schema))
    print("Languages:", sorted(languages))
