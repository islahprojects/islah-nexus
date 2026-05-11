use sha2::{Digest, Sha256};

pub const PHI: f64 = 1.618033988749895;
pub const PHI_INV: f64 = 0.618033988749895;
pub const SIGMA_CAP: f64 = 0.93;
pub const EPSILON_MIN: f64 = 0.07;
pub const NOISE_THRESHOLD: f64 = 0.15;
pub const TRUTH_GATE: f64 = 0.93;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum GateVerdict {
    AcceptLocal,
    ReviewRequired,
    Reject,
}

#[derive(Debug, Clone)]
pub struct OraclePayload {
    pub intent: String,
    pub content: String,
    pub citation_count: u32,
    pub sigma: f64,
    pub noise_ratio: f64,
}

#[derive(Debug, Clone)]
pub struct OracleQubit {
    pub truth_hash: String,
    pub compression_ratio: f64,
    pub phi_alignment: f64,
    pub integrity: f64,
    pub sigma: f64,
    pub epsilon: f64,
    pub verdict: GateVerdict,
    pub status: &'static str,
}

pub fn clamp_sigma(value: f64) -> f64 {
    if value.is_nan() || value < 0.0 {
        0.0
    } else if value > SIGMA_CAP {
        SIGMA_CAP
    } else {
        value
    }
}

pub fn epsilon_from_sigma(sigma: f64) -> f64 {
    let eps = 1.0 - clamp_sigma(sigma);
    if eps < EPSILON_MIN {
        EPSILON_MIN
    } else {
        eps
    }
}

pub fn sha256_hex(text: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(text.as_bytes());
    format!("{:x}", hasher.finalize())
}

pub fn phi_alignment_for_ratio(compression_ratio: f64) -> f64 {
    (compression_ratio - PHI_INV).abs()
}

pub fn estimate_integrity(
    compression_ratio: f64,
    citation_count: u32,
    noise_ratio: f64,
    sigma: f64,
) -> f64 {
    if compression_ratio <= 0.0 || noise_ratio.is_nan() {
        return 0.0;
    }

    let sigma = clamp_sigma(sigma);
    let citation_boost = 1.0 + (0.02 * ((citation_count as f64) + 1.0).ln());
    let noise_penalty = (-5.0 * noise_ratio.max(0.0)).exp();
    let phi_fit = 1.0 - phi_alignment_for_ratio(compression_ratio).min(1.0);

    (phi_fit * citation_boost * noise_penalty * sigma)
        .min(SIGMA_CAP)
        .max(0.0)
}

pub fn process_payload(payload: &OraclePayload) -> OracleQubit {
    let sigma = clamp_sigma(payload.sigma);
    let epsilon = epsilon_from_sigma(sigma);

    let compression_ratio = if payload.content.is_empty() {
        0.0
    } else {
        PHI_INV
    };

    let phi_alignment = phi_alignment_for_ratio(compression_ratio);

    let integrity = estimate_integrity(
        compression_ratio,
        payload.citation_count,
        payload.noise_ratio,
        sigma,
    );

    let verdict = if payload.content.trim().is_empty() {
        GateVerdict::Reject
    } else if payload.noise_ratio > NOISE_THRESHOLD {
        GateVerdict::Reject
    } else if payload.citation_count < 3 {
        GateVerdict::ReviewRequired
    } else if integrity >= TRUTH_GATE && epsilon <= EPSILON_MIN {
        GateVerdict::AcceptLocal
    } else {
        GateVerdict::ReviewRequired
    };

    OracleQubit {
        truth_hash: sha256_hex(&payload.content),
        compression_ratio,
        phi_alignment,
        integrity,
        sigma,
        epsilon,
        verdict,
        status: "CODE_NEEDS_TEST",
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn phi_identity_holds() {
        assert!((PHI * PHI - PHI - 1.0).abs() < 1e-12);
        assert!((PHI - 1.0 - PHI_INV).abs() < 1e-12);
    }

    #[test]
    fn sigma_is_capped_below_one() {
        assert_eq!(clamp_sigma(0.99), SIGMA_CAP);
        assert_eq!(epsilon_from_sigma(0.99), EPSILON_MIN);
    }

    #[test]
    fn sha256_is_stable() {
        let a = sha256_hex("Walang Maiiwan");
        let b = sha256_hex("Walang Maiiwan");
        assert_eq!(a, b);
        assert_eq!(a.len(), 64);
    }

    #[test]
    fn phi_alignment_targets_inverse_phi() {
        let alignment = phi_alignment_for_ratio(PHI_INV);
        assert!(alignment < 1e-12);
    }

    #[test]
    fn rejects_empty_content() {
        let payload = OraclePayload {
            intent: "empty".to_string(),
            content: "".to_string(),
            citation_count: 3,
            sigma: 0.93,
            noise_ratio: 0.0,
        };

        let qubit = process_payload(&payload);
        assert_eq!(qubit.verdict, GateVerdict::Reject);
    }

    #[test]
    fn rejects_high_noise() {
        let payload = OraclePayload {
            intent: "noise".to_string(),
            content: "valid content".to_string(),
            citation_count: 3,
            sigma: 0.93,
            noise_ratio: 0.25,
        };

        let qubit = process_payload(&payload);
        assert_eq!(qubit.verdict, GateVerdict::Reject);
    }

    #[test]
    fn requires_review_when_citations_low() {
        let payload = OraclePayload {
            intent: "low citations".to_string(),
            content: "valid content".to_string(),
            citation_count: 1,
            sigma: 0.93,
            noise_ratio: 0.0,
        };

        let qubit = process_payload(&payload);
        assert_eq!(qubit.verdict, GateVerdict::ReviewRequired);
    }

    #[test]
    fn accepts_local_when_gates_pass() {
        let payload = OraclePayload {
            intent: "safe local payload".to_string(),
            content: "local first offline first uncertainty preserved".to_string(),
            citation_count: 3,
            sigma: 0.93,
            noise_ratio: 0.0,
        };

        let qubit = process_payload(&payload);
        assert_eq!(qubit.verdict, GateVerdict::AcceptLocal);
        assert_eq!(qubit.status, "CODE_NEEDS_TEST");
        assert!(qubit.integrity <= SIGMA_CAP);
    }
}
