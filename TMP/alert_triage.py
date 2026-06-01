import json
from typing import Dict, Any
from src.adapters.models.alert import UnifiedAlert

class AlertTriageAgent:
    """AI 告警研判 Agent - 使用大模型分析安全告警"""
    
    def __init__(self, llm_client=None):
        self.llm_client = llm_client  # OpenAI/Claude/通义等
    
    def triage(self, alert: UnifiedAlert) -> Dict[str, Any]:
        """研判告警，返回置信度和建议"""
        
        # 方式1：调用真实大模型 API
        if self.llm_client:
            return self._triage_with_llm(alert)
        
        # 方式2：基于规则的本地研判（降级方案）
        return self._triage_with_rules(alert)
    
    def _triage_with_llm(self, alert: UnifiedAlert) -> Dict[str, Any]:
        """调用大模型 API 研判"""
        prompt = f"""
你是一个安全运营专家。请分析以下安全告警：

- 告警类型: {alert.alert_type}
- 标题: {alert.title}
- 描述: {alert.description}
- 源IP: {alert.src_ip}
- 严重等级: {alert.severity}
- 进程: {alert.process_name}

请输出 JSON 格式：
{{"confidence": 0.95, "is_attack": true, "attack_type": "mining", "suggested_action": "isolate", "reason": "..."}}
"""
        # 实际调用 LLM API
        # response = self.llm_client.chat(prompt)
        # return json.loads(response)
        
        # 模拟返回
        return {
            "confidence": 0.95,
            "is_attack": True,
            "attack_type": "mining",
            "suggested_action": "isolate",
            "reason": "进程 xmrig 是典型的挖矿木马，CPU 使用率异常"
        }
    
    def _triage_with_rules(self, alert: UnifiedAlert) -> Dict[str, Any]:
        """基于规则的本地研判"""
        confidence = 0.5
        suggested_action = "manual"
        attack_type = "unknown"
        
        # 挖矿检测规则
        if alert.alert_type == "mining" or "xmrig" in alert.process_name.lower():
            confidence = 0.95
            suggested_action = "isolate"
            attack_type = "mining"
        
        # 勒索软件检测规则
        elif "ransom" in alert.alert_type.lower():
            confidence = 0.90
            suggested_action = "isolate"
            attack_type = "ransomware"
        
        # 扫描检测规则
        elif alert.alert_type == "scan":
            confidence = 0.60
            suggested_action = "block"
            attack_type = "scan"
        
        return {
            "confidence": confidence,
            "is_attack": confidence > 0.5,
            "attack_type": attack_type,
            "suggested_action": suggested_action,
            "reason": f"基于规则引擎判定为 {attack_type}"
        }