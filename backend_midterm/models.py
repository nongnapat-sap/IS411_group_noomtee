from typing import Optional
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from sqlmodel import Field, SQLModel


# เวลาประเทศไทยเร็วกว่าเวลาสากล(UTC) 7 ชั่วโมง
def thai_now():
    return datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None)


# =========================================================
# CPU
# =========================================================
class CPU(BaseModel):
    brand: str
    cpu_name: str
    socket: str  # เช่น LGA1700 (Intel), AM5 (AMD)
    cores: int
    threads: int
    base_clock_ghz: float
    boost_clock_ghz: float
    tdp_w: int  # กินไฟกี่วัตต์
    integrated_graphics: bool  # มีกราฟิกในตัวไหม
    price: float


class CPUOut(CPU):
    cpu_id: int


class CPUDB(SQLModel, table=True):
    __tablename__ = "cpus"
    cpu_id: Optional[int] = Field(default=None, primary_key=True)
    brand: str
    cpu_name: str
    socket: str
    cores: int
    threads: int
    base_clock_ghz: float
    boost_clock_ghz: float
    tdp_w: int
    integrated_graphics: bool
    price: float


# =========================================================
# MAINBOARD
# =========================================================
class Mainboard(BaseModel):
    brand: str
    mainboard_name: str
    socket: str
    chipset: str
    form_factor: str  # ATX, Micro-ATX, Mini-ITX
    memory_type: str  # DDR4 หรือ DDR5
    memory_slots: int
    m2_slots: int
    price: float


class MainboardOut(Mainboard):
    mainboard_id: int


class MainboardDB(SQLModel, table=True):
    __tablename__ = "mainboards"
    mainboard_id: Optional[int] = Field(default=None, primary_key=True)
    brand: str
    mainboard_name: str
    socket: str
    chipset: str
    form_factor: str
    memory_type: str
    memory_slots: int
    m2_slots: int
    price: float


# =========================================================
# RAM
# =========================================================
class RAM(BaseModel):
    brand: str
    ram_name: str
    memory_type: str
    capacity_gb: int
    modules: int  # จำนวนแถวในชุด เช่น 8GBx2 = 2 แถว
    speed_mhz: int
    price: float


class RAMOut(RAM):
    ram_id: int


class RAMDB(SQLModel, table=True):
    __tablename__ = "rams"
    ram_id: Optional[int] = Field(default=None, primary_key=True)
    brand: str
    ram_name: str
    memory_type: str
    capacity_gb: int
    modules: int
    speed_mhz: int
    price: float


# =========================================================
# GPU
# =========================================================
class GPU(BaseModel):
    brand: str
    gpu_name: str
    chipset: str  # เช่น GeForce RTX 4060
    vram_gb: int
    tdp_w: int
    length_mm: int  # ความยาวการ์ด ใช้เช็กว่าใส่เคสได้ไหม
    price: float


class GPUOut(GPU):
    gpu_id: int


class GPUDB(SQLModel, table=True):
    __tablename__ = "gpus"
    gpu_id: Optional[int] = Field(default=None, primary_key=True)
    brand: str
    gpu_name: str
    chipset: str
    vram_gb: int
    tdp_w: int
    length_mm: int
    price: float


# =========================================================
# STORAGE
# =========================================================
class Storage(BaseModel):
    brand: str
    storage_name: str
    storage_type: str  # SSD หรือ HDD
    interface: str  # M.2 NVMe หรือ SATA
    capacity_gb: int
    read_speed_mbps: int
    price: float


class StorageOut(Storage):
    storage_id: int


class StorageDB(SQLModel, table=True):
    __tablename__ = "storages"
    storage_id: Optional[int] = Field(default=None, primary_key=True)
    brand: str
    storage_name: str
    storage_type: str
    interface: str
    capacity_gb: int
    read_speed_mbps: int
    price: float


# =========================================================
# PSU
# =========================================================
class PSU(BaseModel):
    brand: str
    psu_name: str
    wattage_w: int
    efficiency: str  # เช่น 80 Plus Bronze
    price: float


class PSUOut(PSU):
    psu_id: int


class PSUDB(SQLModel, table=True):
    __tablename__ = "psus"
    psu_id: Optional[int] = Field(default=None, primary_key=True)
    brand: str
    psu_name: str
    wattage_w: int
    efficiency: str
    price: float


# =========================================================
# CASE
# =========================================================
class Case(BaseModel):
    brand: str
    case_name: str
    supported_form_factors: str  # เช่น "ATX,Micro-ATX,Mini-ITX"
    max_gpu_length_mm: int
    price: float


class CaseOut(Case):
    case_id: int


class CaseDB(SQLModel, table=True):
    __tablename__ = "cases"
    case_id: Optional[int] = Field(default=None, primary_key=True)
    brand: str
    case_name: str
    supported_form_factors: str
    max_gpu_length_mm: int
    price: float


# =========================================================
# CUSTOMER
# =========================================================
class Customer(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None


class CustomerOut(Customer):
    customer_id: int
    created_at: datetime


class CustomerDB(SQLModel, table=True):
    __tablename__ = "customers"
    customer_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    created_at: datetime = Field(default_factory=thai_now)


# =========================================================
# PC SET (คอมพิวเตอร์ 1 ชุดของลูกค้า)
# =========================================================
class PCSet(BaseModel):
    customer_id: int
    set_name: str
    cpu_id: int
    mainboard_id: int
    ram_id: int
    gpu_id: Optional[int] = None  # ไม่ใส่ก็ได้ ถ้า CPU มีกราฟิกในตัว
    storage_id: int
    psu_id: int
    case_id: int


class PCSetOut(PCSet):
    set_id: int
    total_price: float
    copied_from: Optional[int] = None  # ถ้าคัดลอกมา จะบอกว่ามาจาก set ไหน
    created_at: datetime
    updated_at: datetime


class PCSetDB(SQLModel, table=True):
    __tablename__ = "pc_sets"
    set_id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int
    set_name: str
    cpu_id: int
    mainboard_id: int
    ram_id: int
    gpu_id: Optional[int] = None
    storage_id: int
    psu_id: int
    case_id: int
    total_price: float = 0
    copied_from: Optional[int] = None
    created_at: datetime = Field(default_factory=thai_now)
    updated_at: datetime = Field(default_factory=thai_now)


# ใช้ตอนคัดลอก set ไปให้ลูกค้าคนอื่น
class CopySet(BaseModel):
    customer_id: int
    set_name: str