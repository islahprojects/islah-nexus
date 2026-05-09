# Local File Candidate Scan

Status: LOCAL_SCAN_ONLY
Deployment gate: CLOSED
Total items: 120

## Bucket counts

- BLOCKED_DO_NOT_STAGE: 34
- CODE_OR_VALIDATION_FUTURE_REVIEW: 17
- DOCS_FUTURE_REVIEW: 7
- FUTURE_CHAMBER_NOT_THIS_RELEASE: 7
- LOCAL_EVIDENCE_LOG_REVIEW: 2
- NEEDS_CLAIM_BOUNDARY_REVIEW: 20
- UNSORTED_LOCAL_REVIEW: 33

## Recommended current release candidates


## Blocked / do not stage

- .env.example
- archive/
- bridge_api.py
- core/logs/
- core/vault/
- dist/islah_nexus_mvp_20260505_031405.zip
- dist/islah_nexus_mvp_20260505_170829.zip
- dist/islah_nexus_mvp_20260506_004059.zip
- dist/islah_nexus_mvp_20260506_012740.zip
- dist/islah_nexus_mvp_20260506_012924.zip
- dist/islah_nexus_mvp_20260509_014159.zip
- dist/islah_nexus_mvp_20260509_014429.zip
- dist/islah_nexus_mvp_20260509_015530.zip
- dist/islah_nexus_mvp_20260509_020951.zip
- dist/islah_nexus_mvp_20260509_021934.zip
- dist/islah_nexus_mvp_20260509_022510.zip
- dist/islah_nexus_mvp_20260509_043323.zip
- dist/islah_nexus_mvp_20260509_043426.zip
- dist/islah_nexus_mvp_20260509_092613.zip
- dist/islah_nexus_mvp_20260509_120907.zip
- docs/omnisyntax_refined_v1_1.md
- docs/omnisyntax_v1_3_seil_boundary_review.md
- engine.py
- governance_log.json
- islah_nexus/cli.py.bak_20260504_162611
- islah_nexus/cloud_mirror.py
- logs/local_file_candidate_scan.json
- logs/omnisyntax_refinement_report.json
- scripts/patch_windows_bom_and_schema.py
- scripts/run_torch_validation.py
- scripts/scan_local_candidates.py
- scripts/seil_boundary_engine_v1_3.py
- tests/test_no_production_activation.py
- tests/test_objective_function_constraints.py

## Needs review

- Modelfile [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- PROJECT_CHARTER.md [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- boot_islah.ps1 [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- chief_omega.py [??] bucket=NEEDS_CLAIM_BOUNDARY_REVIEW risks=FORBIDDEN_PROMOTION
- config/ [??] bucket=UNSORTED_LOCAL_REVIEW risks=MISSING_ON_DISK
- deploy_nexus.sh [??] bucket=NEEDS_CLAIM_BOUNDARY_REVIEW risks=FORBIDDEN_PROMOTION
- docs/AGI_BOUNDARY.md [??] bucket=NEEDS_CLAIM_BOUNDARY_REVIEW risks=DEPLOYMENT_WORDING
- docs/EXTERNAL_THEORY_BUNDLE_INTAKE.md [??] bucket=NEEDS_CLAIM_BOUNDARY_REVIEW risks=FORBIDDEN_PROMOTION
- docs/MIRROR_APP_V0.md [??] bucket=NEEDS_CLAIM_BOUNDARY_REVIEW risks=FORBIDDEN_PROMOTION, DEPLOYMENT_WORDING
- docs/MVP_STATUS.md [??] bucket=NEEDS_CLAIM_BOUNDARY_REVIEW risks=FORBIDDEN_PROMOTION
- docs/RELEASE_MANIFEST.md [??] bucket=NEEDS_CLAIM_BOUNDARY_REVIEW risks=FORBIDDEN_PROMOTION
- gate_d_ledger.py [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- gate_e_chi2mm2.py [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- governance_log_append.py [??] bucket=NEEDS_CLAIM_BOUNDARY_REVIEW risks=FORBIDDEN_PROMOTION
- islah_master_node.py [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- islah_nexus/__init__.py [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- islah_nexus/architect_refiner.py [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- islah_nexus/cli.py [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- islah_nexus/constitution.py [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- islah_nexus/db.py [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- islah_nexus/decision_kernel.py [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- islah_nexus/gates.py [??] bucket=NEEDS_CLAIM_BOUNDARY_REVIEW risks=FORBIDDEN_PROMOTION
- islah_nexus/main.py [??] bucket=NEEDS_CLAIM_BOUNDARY_REVIEW risks=FORBIDDEN_PROMOTION, DEPLOYMENT_WORDING
- islah_nexus/memory.py [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- islah_nexus/nexusgpt.py [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- islah_nexus/security/ [??] bucket=UNSORTED_LOCAL_REVIEW risks=MISSING_ON_DISK
- islah_nexus/unity.py [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- islah_sovereign_engine.py [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- law_vii_monitor.py [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- main.py [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- mirror_prompt.txt [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- nexus_hex_control_plane.py [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- notion_sync.py [??] bucket=NEEDS_CLAIM_BOUNDARY_REVIEW risks=FORBIDDEN_PROMOTION
- notion_sync_v2.py [??] bucket=NEEDS_CLAIM_BOUNDARY_REVIEW risks=FORBIDDEN_PROMOTION
- page.tsx [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- patch_ghost_bridge.py [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- patch_translator.py [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- patch_translator_v2.py [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- pinky_dog.py [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- requirements.txt [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- scripts/run_anna_local.ps1 [??] bucket=NEEDS_CLAIM_BOUNDARY_REVIEW risks=FORBIDDEN_PROMOTION, DEPLOYMENT_WORDING
- scripts/run_duck_security_check.ps1 [??] bucket=NEEDS_CLAIM_BOUNDARY_REVIEW risks=FORBIDDEN_PROMOTION
- scripts/run_mvp_check.ps1 [??] bucket=NEEDS_CLAIM_BOUNDARY_REVIEW risks=FORBIDDEN_PROMOTION
- scripts/run_phase1_no_pytest.py [??] bucket=NEEDS_CLAIM_BOUNDARY_REVIEW risks=FORBIDDEN_PROMOTION, DEPLOYMENT_WORDING, CONFIDENCE_GE_1
- scripts/validate_umu.py [??] bucket=NEEDS_CLAIM_BOUNDARY_REVIEW risks=FORBIDDEN_PROMOTION, DEPLOYMENT_WORDING, CONFIDENCE_GE_1
- sovereign_identity.example.json [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- test_gate.py [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- test_soog_corrigibility.py [??] bucket=NEEDS_CLAIM_BOUNDARY_REVIEW risks=FORBIDDEN_PROMOTION
- tests/test_no_runtime_sealed_claim.py [??] bucket=NEEDS_CLAIM_BOUNDARY_REVIEW risks=FORBIDDEN_PROMOTION
- tests/test_omnisyntax_status_boundaries.py [??] bucket=NEEDS_CLAIM_BOUNDARY_REVIEW risks=FORBIDDEN_PROMOTION
- truthkind_prompt.sh [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- umu_schema.json [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
- void_legend.py [??] bucket=UNSORTED_LOCAL_REVIEW risks=none
