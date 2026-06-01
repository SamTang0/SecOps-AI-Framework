from datetime import datetime
from typing import Dict, Optional
from pydantic import BaseModel

class UnifiedAlert(BaseModel):
    id: str
    timestamp: datetime
    source: str
    severity: str  # critical/high/medium/low
    src_ip: Optional[str] = None
    dst_ip: Optional[str] = None
    alert_type: str
    title: str
    description: str
    raw_data: Dict
    ai_confidence: float = 0.0
    ai_reason: str = ""
    status: str = "new"
