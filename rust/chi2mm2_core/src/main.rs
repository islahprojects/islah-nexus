use chi2mm2_core::{process_payload, OraclePayload};

fn main() {
    let payload = OraclePayload {
        intent: "Chi2MM2 local Rust dry run".to_string(),
        content: "local first offline first uncertainty preserved walang maiiwan".to_string(),
        citation_count: 3,
        sigma: 0.93,
        noise_ratio: 0.0,
    };

    let qubit = process_payload(&payload);

    println!("STATUS: {}", qubit.status);
    println!("VERDICT: {:?}", qubit.verdict);
    println!("SIGMA: {:.2}", qubit.sigma);
    println!("EPSILON: {:.2}", qubit.epsilon);
    println!("INTEGRITY: {:.4}", qubit.integrity);
    println!("PHI_ALIGNMENT: {:.12}", qubit.phi_alignment);
    println!("HASH: {}", qubit.truth_hash);
    println!("SCOPE: LOCAL_DRY_RUN_ONLY");
    println!("WALANG MAIIWAN");
}
