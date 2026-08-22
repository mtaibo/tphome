from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from db.database import get_session
from db.models import DeviceLog

router = APIRouter(prefix="/logs", tags=["logs"])


@router.get("/{device_id}")
def get_logs(device_id: str, limit: int = 200, session: Session = Depends(get_session)):
    logs = session.exec(
        select(DeviceLog)
        .where(DeviceLog.device_id == device_id)
        .order_by(DeviceLog.id.desc())
        .limit(limit)
    ).all()
    return logs
