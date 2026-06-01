from abc import ABC, abstractmethod
from typing import List, Dict, Any

class SecurityActions(ABC):
    """统一操作接口 - 所有产品适配器必须实现"""
    
    @abstractmethod
    def block_ip(self, ip: str, duration: int = 3600) -> bool:
        """封禁 IP"""
        pass
    
    @abstractmethod
    def isolate_host(self, host_id: str) -> bool:
        """隔离主机"""
        pass
    
    @abstractmethod
    def kill_process(self, host_id: str, pid: int) -> bool:
        """杀死进程"""
        pass
    
    @abstractmethod
    def create_ticket(self, title: str, content: str, priority: str) -> str:
        """创建工单，返回工单 ID"""
        pass
    
    @abstractmethod
    def send_notification(self, channel: str, message: str) -> bool:
        """发送通知"""
        pass
    
    @abstractmethod
    def query_logs(self, query: str, time_range: str) -> List[Dict]:
        """查询日志"""
        pass