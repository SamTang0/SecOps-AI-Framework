from src.orchestration.actions.atomic_actions import AtomicActions
from src.adapters.models.alert import UnifiedAlert

class MiningPlaybook:
    """挖矿攻击响应剧本"""
    
    def __init__(self):
        self.name = "挖矿响应剧本"
        self.steps = [
            self.isolate_affected_host,
            self.kill_mining_process,
            self.block_c2_ip,
            self.create_incident_ticket,
            self.send_alert_notification
        ]
    
    def execute(self, alert: UnifiedAlert, ai_result: dict):
        """执行响应剧本"""
        print(f"\n🚨 执行剧本: {self.name}")
        print(f"   置信度: {ai_result['confidence']}")
        print(f"   原因: {ai_result['reason']}")
        print("-" * 50)
        
        for step in self.steps:
            step(alert, ai_result)
        
        print("-" * 50)
        print(f"✅ 剧本执行完成")
    
    def isolate_affected_host(self, alert: UnifiedAlert, ai_result: dict):
        """隔离受感染主机"""
        if alert.hostname:
            AtomicActions.isolate_host(alert.hostname)
        elif alert.src_ip:
            AtomicActions.isolate_host(alert.src_ip)
    
    def kill_mining_process(self, alert: UnifiedAlert, ai_result: dict):
        """杀死挖矿进程"""
        if alert.process_id and alert.hostname:
            AtomicActions.kill_process(alert.hostname, alert.process_id)
    
    def block_c2_ip(self, alert: UnifiedAlert, ai_result: dict):
        """封禁 C2 服务器 IP"""
        # 实际场景中需要从威胁情报或告警中提取 C2 IP
        if alert.dst_ip:
            AtomicActions.block_ip(alert.dst_ip)
    
    def create_incident_ticket(self, alert: UnifiedAlert, ai_result: dict):
        """创建工单"""
        title = f"[自动处置] 挖矿攻击 - {alert.hostname or alert.src_ip}"
        content = f"""
告警ID: {alert.id}
告警类型: {alert.alert_type}
受影响主机: {alert.hostname or alert.src_ip}
进程: {alert.process_name} (PID: {alert.process_id})
AI 置信度: {ai_result['confidence']}
AI 研判理由: {ai_result['reason']}
处置动作: 已自动隔离主机并杀死进程
"""
        AtomicActions.create_ticket(title, content, priority="high")
    
    def send_alert_notification(self, alert: UnifiedAlert, ai_result: dict):
        """发送告警通知"""
        message = f"""
🚨 【安全告警】挖矿攻击已自动处置

受影响主机: {alert.hostname or alert.src_ip}
攻击类型: {alert.alert_type}
进程: {alert.process_name}
置信度: {ai_result['confidence']}
处置状态: 已隔离 + 已杀进程
"""
        AtomicActions.send_alert("security-team", message)