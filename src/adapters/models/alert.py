from datetime import datetime
from typing import Dict, Optional
from enum import Enum
from pydantic import BaseModel

class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class AlertStatus(str, Enum):
    NEW = "new"
    PROCESSING = "processing"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"

class UnifiedAlert(BaseModel):
    """统一告警模型 - 所有安全产品的告警转换为此格式"""
    
    # 基础信息
    id: str
    timestamp: datetime
    source: str  # 产品名称: splunk/qradar/crowdstrike/...
    
    # 告警内容
    title: str
    description: str
    severity: Severity
    alert_type: str  # mining/ransomware/phishing/scan/...
    
    # 网络信息
    src_ip: Optional[str] = None
    dst_ip: Optional[str] = None
    src_port: Optional[int] = None
    dst_port: Optional[int] = None
    
    # 主机/用户信息
    hostname: Optional[str] = None
    username: Optional[str] = None
    process_name: Optional[str] = None
    process_id: Optional[int] = None
    
    # AI 研判结果
    ai_confidence: float = 0.0  # 0-1
    ai_reason: str = ""
    suggested_action: str = ""  # block/isolate/kill/manual
    
    # 处置状态
    status: AlertStatus = AlertStatus.NEW
    
    # 原始数据（保留）
    raw_data: Dict = {}
    
    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}