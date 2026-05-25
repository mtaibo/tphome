from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlmodel import Session, select
from db.database import get_session
from db.models import FirmwareInfo
import os
from datetime import datetime

router = APIRouter(tags=["Firmware"])

FIRMWARE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "storage", "firmwares")
os.makedirs(FIRMWARE_DIR, exist_ok=True)


def _get_firmware(id: int, session: Session) -> FirmwareInfo:
    fw = session.get(FirmwareInfo, id)
    if not fw:
        raise HTTPException(status_code=404, detail="Firmware not found")
    return fw


@router.post("/firmware/upload")
async def upload_firmware(
    file: UploadFile = File(...),
    name: str = Form(...),
    chip: str = Form(...),
    target: str = Form(...),
    version: str = Form(...),
    notes: str = Form(""),
    session: Session = Depends(get_session),
):
    if not file.filename.endswith(".bin"):
        raise HTTPException(status_code=400, detail="Only .bin files are allowed")

    fw = FirmwareInfo(
        name=name,
        chip=chip,
        target=target,
        version=version,
        notes=notes,
        uploaded_at=datetime.now().isoformat(),
        active=False,
    )
    session.add(fw)
    session.commit()
    session.refresh(fw)

    file_path = os.path.join(FIRMWARE_DIR, f"{fw.id}.bin")
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return {
        "id": fw.id,
        "name": fw.name,
        "chip": fw.chip,
        "target": fw.target,
        "version": fw.version,
        "notes": fw.notes,
        "uploaded_at": fw.uploaded_at,
        "active": fw.active,
        "size_bytes": len(content),
    }


@router.get("/firmware/list")
def list_firmware(session: Session = Depends(get_session)):
    firmwares = session.exec(select(FirmwareInfo).order_by(FirmwareInfo.uploaded_at.desc())).all()
    return [
        {
            "id": fw.id,
            "name": fw.name,
            "chip": fw.chip,
            "target": fw.target,
            "version": fw.version,
            "notes": fw.notes,
            "uploaded_at": fw.uploaded_at,
            "active": fw.active,
        }
        for fw in firmwares
    ]


@router.post("/firmware/{fw_id}/activate")
def activate_firmware(fw_id: int, session: Session = Depends(get_session)):
    fw = _get_firmware(fw_id, session)

    session.exec(select(FirmwareInfo).where(FirmwareInfo.active == True).update({"active": False}, synchronize_session=False))
    fw.active = True
    session.add(fw)
    session.commit()

    return {"id": fw.id, "name": fw.name, "active": True}


@router.delete("/firmware/{fw_id}")
def delete_firmware(fw_id: int, session: Session = Depends(get_session)):
    fw = _get_firmware(fw_id, session)

    file_path = os.path.join(FIRMWARE_DIR, f"{fw.id}.bin")
    if os.path.exists(file_path):
        os.remove(file_path)

    session.delete(fw)
    session.commit()

    return {"deleted": fw_id}


@router.get("/firmware")
def serve_firmware(session: Session = Depends(get_session)):
    active = session.exec(select(FirmwareInfo).where(FirmwareInfo.active == True)).first()
    if not active:
        raise HTTPException(status_code=404, detail="No active firmware")

    file_path = os.path.join(FIRMWARE_DIR, f"{active.id}.bin")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Firmware file missing")

    return FileResponse(file_path, media_type="application/octet-stream", filename=f"{active.name}.bin")
