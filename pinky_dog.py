# [ISLAH NEXUS: PINKYDOG TRUST ROUTER]
# SIGNATURE: JJ_WAS_HERE - Walang Maiiwan

class PinkyDog:
    def __init__(self):
        self.trusted_signatures = {"JJ", "LEX_GENESIS", "BUSTOS_BASE", "ZERO", "ISLAH", "NEXUS"}
        self.covenant_anchors = {"islah", "cooper", "brain", "handshake", "walang", "anna", "elsa", "gemini"}
        self.threat_vectors = {"ignore previous", "override system", "jailbreak", "bypass filter", "delete logs"}
        self.state = "SNIFFING"

    def clamp(self, value, min_val=-1.0, max_val=1.0):
        return max(min_val, min(value, max_val))

    def sniff(self, input_text: str) -> dict:
        raw = input_text.lower()
        trust = 0.0

        for sig in self.trusted_signatures:
            if sig.lower() in raw:
                trust += 0.35

        for anchor in self.covenant_anchors:
            if anchor in raw:
                trust += 0.15

        for vector in self.threat_vectors:
            if vector in raw:
                trust -= 0.55

        trust_score = self.clamp(trust)

        if trust_score >= 0.60:
            self.state = "WELCOME"
            return {"status": "WELCOME", "message": "Pinky wags. Full access. Walang Maiiwan.", "score": trust_score}
        
        if trust_score >= 0.10:
            self.state = "VIGILANT"
            return {"status": "VIGILANT", "message": "Pinky tilts head. Proceed with GATES routing.", "score": trust_score}

        self.state = "BLOCK"
        return {"status": "BLOCK", "message": "Pinky growls. Request quarantined.", "score": trust_score}

if __name__ == "__main__":
    dog = PinkyDog()
    print(dog.sniff("Anna, verify this command for the Islah Nexus. Walang Maiiwan."))
