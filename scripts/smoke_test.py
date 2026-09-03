"""Smoke test script executed during make journey.

Verifies end-to-end continuous intelligence audit cycle,
scoring, and evidence graph mapping.
"""

from agent_orchestrator import ContinuousIntelligenceEngine

def main():
    engine = ContinuousIntelligenceEngine(organization_name="Journey-SmokeTest-Org")
    test_assets = [
        {
            "target_control": "ISO/IEC 27001:2022 A.5.23",
            "resource_type": "gcs_bucket",
            "resource_id": "journey-smoke-test-bucket",
            "config": {
                "public_access_prevention": "enforced",
                "uniform_bucket_level_access": True,
            },
            "verification_tier": "VERIFIED",
        },
        {
            "target_control": "ISO/IEC 27001:2022 A.8.12",
            "resource_type": "vpc_sc_perimeter",
            "resource_id": "accessPolicies/0/servicePerimeters/journey_perimeter",
            "config": {
                "enforced": True,
                "restricted_services": ["storage.googleapis.com", "bigquery.googleapis.com"],
            },
            "verification_tier": "VERIFIED",
        },
    ]

    res = engine.execute_proactive_audit_cycle(
        cycle_id="journey-smoke-cycle",
        cloud_assets=test_assets,
    )

    cycle_id = res["cycle_id"]
    score = res["scorecard"]["overall_score"]
    rating = res["scorecard"]["rating"]
    nodes = res["evidence_graph_summary"]["total_evidence_nodes"]

    print(f"-> Audit Cycle ID: {cycle_id}")
    print(f"-> Compliance Score: {score}% ({rating})")
    print(f"-> Evidence Nodes Mapped: {nodes}")

    assert score == 100.0, f"Smoke test expected 100% score, got {score}%"
    print("-> Smoke test assertion verified successfully.")

if __name__ == "__main__":
    main()
