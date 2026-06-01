class AlertTriageAgent:
    def __init__(self, llm_client): self.llm_client = llm_client
    def triage(self, alert):
        return {"confidence": 0.95, "action": "isolate", "reason": "高风险行为"}
