#!/usr/bin/env python3
"""
SecOps-AI-Framework 主入口
完整告警处理流程：采集 → AI研判 → 处置 → 闭环
"""

import time
from datetime import datetime
from src.adapters.models.alert import UnifiedAlert
from src.adapters.registry.adapter_registry import AdapterRegistry
from src.adapters.impl.siem.splunk_adapter import SplunkAdapter
from src.adapters.impl.firewall.aliyun_waf import AliyunWAFAdapter
from src.adapters.impl.notify.feishu import FeishuAdapter
from src.intelligence.agents.alert_triage import AlertTriageAgent
from src.orchestration.playbooks.mining_playbook import MiningPlaybook

def register_adapters():
    """注册所有产品适配器"""
    AdapterRegistry.register("siem", "splunk", SplunkAdapter)
    AdapterRegistry.register("firewall", "aliyun_waf", AliyunWAFAdapter)
    AdapterRegistry.register("notify", "feishu", FeishuAdapter)
    print("✅ 适配器注册完成\n")

def get_playbook(alert_type: str):
    """根据告警类型获取对应的响应剧本"""
    playbooks = {
        "mining": MiningPlaybook(),
        "ransomware": MiningPlaybook(),  # TODO: 实现勒索剧本
        "phishing": MiningPlaybook(),    # TODO: 实现钓鱼剧本
    }
    return playbooks.get(alert_type, MiningPlaybook())

def process_alert(alert: UnifiedAlert):
    """处理单条告警的核心流程"""
    print(f"\n📨 收到告警: {alert.title}")
    print(f"   来源: {alert.source}")
    print(f"   类型: {alert.alert_type}")
    print(f"   严重等级: {alert.severity}")
    
    # 阶段1：AI 研判
    print("\n🧠 阶段1: AI 研判中...")
    triage_agent = AlertTriageAgent()
    ai_result = triage_agent.triage(alert)
    print(f"   置信度: {ai_result['confidence']}")
    print(f"   建议动作: {ai_result['suggested_action']}")
    print(f"   研判理由: {ai_result['reason']}")
    
    # 阶段2：根据置信度决策
    print("\n⚙️ 阶段2: 决策与处置...")
    
    if ai_result['confidence'] >= 0.9:
        print(f"   ✅ 高置信度 ({ai_result['confidence']})，自动处置")
        playbook = get_playbook(ai_result.get('attack_type', alert.alert_type))
        playbook.execute(alert, ai_result)
    
    elif ai_result['confidence'] >= 0.6:
        print(f"   ⚠️ 中置信度 ({ai_result['confidence']})，创建工单待人工确认")
        # TODO: 创建待确认工单
    
    else:
        print(f"   ❌ 低置信度 ({ai_result['confidence']})，标记为误报")
        # TODO: 归档处理
    
    # 阶段3：记录处理结果
    print("\n📊 阶段3: 闭环记录")
    print(f"   告警ID: {alert.id}")
    print(f"   处理状态: {'已处置' if ai_result['confidence'] >= 0.9 else '待处理'}")
    
    return ai_result

def main():
    """主函数 - 模拟告警处理流程"""
    print("=" * 60)
    print("SecOps-AI-Framework 告警处理系统启动")
    print("=" * 60)
    
    # 注册适配器
    register_adapters()
    
    # 获取 Splunk 适配器并拉取告警
    splunk = AdapterRegistry.get("siem", "splunk", {
        "base_url": "https://splunk.example.com",
        "token": "xxx"
    })
    
    # 拉取告警（模拟）
    print("📡 从 Splunk 拉取告警...")
    alerts = splunk.fetch_alerts(since=datetime.now())
    print(f"   共拉取 {len(alerts)} 条告警")
    
    # 逐条处理告警
    for alert in alerts:
        process_alert(alert)
    
    print("\n" + "=" * 60)
    print("✅ 所有告警处理完成")
    print("=" * 60)

if __name__ == "__main__":
    main()