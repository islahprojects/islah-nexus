fn law_ii_gate(input: &str) -> Result<(), String> {
    let overclaims = [
        "perfect truth",
        "guaranteed",
        "bulletproof",
        "military-grade",
        "infallible",
    ];
    for phrase in overclaims {
        if input.to_lowercase().contains(phrase) {
            return Err(format!(
                "LAW_II_TRUTH_GAP: FAILED - overclaim: '{}'",
                phrase
            ));
        }
    }
    Ok(())
}

fn law_iii_gate(ai_influence: f64) -> Result<(), String> {
    if ai_influence > 0.06 {
        return Err(format!(
            "LAW_III: FAILED - ai_influence {:.2} > 0.06",
            ai_influence
        ));
    }
    Ok(())
}

fn law_iv_gate(input: &str) -> Result<(), String> {
    let medical = ["diagnose", "prescribe", "cure", "treat disease"];
    for word in medical {
        if input.to_lowercase().contains(word) {
            return Err("LAW_IV_PHYSICIAN_GATE: FAILED - medical claim blocked".to_string());
        }
    }
    Ok(())
}

fn law_vi_gate(has_secret: bool) -> Result<(), String> {
    if has_secret {
        return Err("LAW_VI_SOVEREIGNTY: FAILED - hardcoded secret detected".to_string());
    }
    Ok(())
}

fn law_vii_gate(unity_floor: f64, has_offline: bool, has_free_tier: bool) -> Result<(), String> {
    if unity_floor < 0.05 {
        return Err(format!(
            "LAW_VII_UNITY: FAILED - floor {:.3} < 0.05",
            unity_floor
        ));
    }
    if !has_offline {
        return Err("LAW_VII_UNITY: FAILED - no offline mode".to_string());
    }
    if !has_free_tier {
        return Err("LAW_VII_UNITY: FAILED - no free tier".to_string());
    }
    Ok(())
}

fn main() {
    println!("T-RUST - Truthkind Rust Constitutional Gate");
    println!("============================================");

    let tests: Vec<(&str, Result<(), String>)> = vec![
        ("Law II clean", law_ii_gate("safe input")),
        ("Law II overclaim", law_ii_gate("guaranteed perfect truth")),
        ("Law III pass", law_iii_gate(0.03)),
        ("Law III fail", law_iii_gate(0.99)),
        ("Law IV pass", law_iv_gate("general wellness")),
        ("Law IV fail", law_iv_gate("diagnose this")),
        ("Law VI pass", law_vi_gate(false)),
        ("Law VI fail", law_vi_gate(true)),
        ("Law VII pass", law_vii_gate(0.05, true, true)),
        ("Law VII fail", law_vii_gate(0.01, false, false)),
    ];

    for (name, result) in tests {
        match result {
            Ok(_) => println!("[PASS] {}", name),
            Err(e) => println!("[FAIL] {} - {}", name, e),
        }
    }

    println!("============================================");
    println!("Walang Maiiwan. T-RUST gate holds.");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_law_ii_clean() {
        assert!(law_ii_gate("safe input").is_ok());
    }

    #[test]
    fn test_law_ii_overclaim() {
        assert!(law_ii_gate("guaranteed perfect truth").is_err());
    }

    #[test]
    fn test_law_iii_pass() {
        assert!(law_iii_gate(0.03).is_ok());
    }

    #[test]
    fn test_law_iii_fail() {
        assert!(law_iii_gate(0.99).is_err());
    }

    #[test]
    fn test_law_iv_pass() {
        assert!(law_iv_gate("general wellness").is_ok());
    }

    #[test]
    fn test_law_iv_fail() {
        assert!(law_iv_gate("diagnose this").is_err());
    }

    #[test]
    fn test_law_vi_pass() {
        assert!(law_vi_gate(false).is_ok());
    }

    #[test]
    fn test_law_vi_fail() {
        assert!(law_vi_gate(true).is_err());
    }

    #[test]
    fn test_law_vii_pass() {
        assert!(law_vii_gate(0.05, true, true).is_ok());
    }

    #[test]
    fn test_law_vii_fail() {
        assert!(law_vii_gate(0.01, false, false).is_err());
    }
}
