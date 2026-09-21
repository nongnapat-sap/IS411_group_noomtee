from fastapi import FastAPI, HTTPException, status
from sqlmodel import Session, select
from database import engine, init_db
from models import (
    thai_now,
    CPU, CPUOut, CPUDB,
    Mainboard, MainboardOut, MainboardDB,
    RAM, RAMOut, RAMDB,
    GPU, GPUOut, GPUDB,
    Storage, StorageOut, StorageDB,
    PSU, PSUOut, PSUDB,
    Case, CaseOut, CaseDB,
    Customer, CustomerOut, CustomerDB,
    PCSet, PCSetOut, PCSetDB, CopySet,
)


init_db()
app = FastAPI()


# =========================================================
# CPU
# =========================================================
@app.get("/cpus/", status_code=status.HTTP_200_OK)
def read_cpus() -> list[CPUOut]:
    with Session(engine) as session:
        return session.exec(select(CPUDB)).all()


@app.get("/cpus/{cpu_id}", status_code=status.HTTP_200_OK)
def read_cpu(cpu_id: int) -> CPUOut:
    with Session(engine) as session:
        cpu = session.get(CPUDB, cpu_id)
        if cpu is not None:
            return cpu
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="ไม่พบ CPU นี้ในระบบค่ะ"
    )


@app.post("/cpus/", status_code=status.HTTP_201_CREATED)
def create_cpu(cpu: CPU) -> CPUOut:
    new_cpu = CPUDB(**cpu.model_dump())
    with Session(engine) as session:
        session.add(new_cpu)
        session.commit()
        session.refresh(new_cpu)
        return new_cpu


# =========================================================
# MAINBOARD
# =========================================================
# ถ้าส่ง cpu_id มาด้วย จะแสดงเฉพาะเมนบอร์ดที่ socket ตรงกับ CPU ตัวนั้นค่ะ
@app.get("/mainboards/", status_code=status.HTTP_200_OK)
def read_mainboards(cpu_id: int | None = None) -> list[MainboardOut]:
    with Session(engine) as session:
        statement = select(MainboardDB)
        if cpu_id is not None:
            cpu = session.get(CPUDB, cpu_id)
            if cpu is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="ไม่พบ CPU นี้ในระบบค่ะ"
                )
            statement = statement.where(MainboardDB.socket == cpu.socket)
        return session.exec(statement).all()


@app.get("/mainboards/{mainboard_id}", status_code=status.HTTP_200_OK)
def read_mainboard(mainboard_id: int) -> MainboardOut:
    with Session(engine) as session:
        mainboard = session.get(MainboardDB, mainboard_id)
        if mainboard is not None:
            return mainboard
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="ไม่พบ Mainboard นี้ในระบบค่ะ"
    )


@app.post("/mainboards/", status_code=status.HTTP_201_CREATED)
def create_mainboard(mainboard: Mainboard) -> MainboardOut:
    new_mainboard = MainboardDB(**mainboard.model_dump())
    with Session(engine) as session:
        session.add(new_mainboard)
        session.commit()
        session.refresh(new_mainboard)
        return new_mainboard


# =========================================================
# RAM
# =========================================================
# ถ้าส่ง mainboard_id มาด้วย จะแสดงเฉพาะแรมชนิดเดียวกับที่เมนบอร์ดรองรับค่ะ
@app.get("/rams/", status_code=status.HTTP_200_OK)
def read_rams(mainboard_id: int | None = None) -> list[RAMOut]:
    with Session(engine) as session:
        statement = select(RAMDB)
        if mainboard_id is not None:
            mainboard = session.get(MainboardDB, mainboard_id)
            if mainboard is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="ไม่พบ Mainboard นี้ในระบบค่ะ"
                )
            statement = statement.where(RAMDB.memory_type == mainboard.memory_type)
        return session.exec(statement).all()


@app.get("/rams/{ram_id}", status_code=status.HTTP_200_OK)
def read_ram(ram_id: int) -> RAMOut:
    with Session(engine) as session:
        ram = session.get(RAMDB, ram_id)
        if ram is not None:
            return ram
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="ไม่พบ RAM นี้ในระบบค่ะ"
    )


@app.post("/rams/", status_code=status.HTTP_201_CREATED)
def create_ram(ram: RAM) -> RAMOut:
    new_ram = RAMDB(**ram.model_dump())
    with Session(engine) as session:
        session.add(new_ram)
        session.commit()
        session.refresh(new_ram)
        return new_ram


# =========================================================
# GPU
# =========================================================
@app.get("/gpus/", status_code=status.HTTP_200_OK)
def read_gpus() -> list[GPUOut]:
    with Session(engine) as session:
        return session.exec(select(GPUDB)).all()


@app.get("/gpus/{gpu_id}", status_code=status.HTTP_200_OK)
def read_gpu(gpu_id: int) -> GPUOut:
    with Session(engine) as session:
        gpu = session.get(GPUDB, gpu_id)
        if gpu is not None:
            return gpu
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="ไม่พบ GPU นี้ในระบบค่ะ"
    )


@app.post("/gpus/", status_code=status.HTTP_201_CREATED)
def create_gpu(gpu: GPU) -> GPUOut:
    new_gpu = GPUDB(**gpu.model_dump())
    with Session(engine) as session:
        session.add(new_gpu)
        session.commit()
        session.refresh(new_gpu)
        return new_gpu


# =========================================================
# STORAGE
# =========================================================
@app.get("/storages/", status_code=status.HTTP_200_OK)
def read_storages() -> list[StorageOut]:
    with Session(engine) as session:
        return session.exec(select(StorageDB)).all()


@app.get("/storages/{storage_id}", status_code=status.HTTP_200_OK)
def read_storage(storage_id: int) -> StorageOut:
    with Session(engine) as session:
        storage = session.get(StorageDB, storage_id)
        if storage is not None:
            return storage
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="ไม่พบ Storage นี้ในระบบค่ะ"
    )


@app.post("/storages/", status_code=status.HTTP_201_CREATED)
def create_storage(storage: Storage) -> StorageOut:
    new_storage = StorageDB(**storage.model_dump())
    with Session(engine) as session:
        session.add(new_storage)
        session.commit()
        session.refresh(new_storage)
        return new_storage


# =========================================================
# PSU
# =========================================================
# ถ้าส่ง cpu_id (และ gpu_id ถ้ามีการ์ดจอ) มา จะแสดงเฉพาะ PSU ที่จ่ายไฟพอ
@app.get("/psus/", status_code=status.HTTP_200_OK)
def read_psus(cpu_id: int | None = None, gpu_id: int | None = None) -> list[PSUOut]:
    with Session(engine) as session:
        statement = select(PSUDB)
        if cpu_id is not None:
            cpu = session.get(CPUDB, cpu_id)
            if cpu is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="ไม่พบ CPU นี้ในระบบค่ะ"
                )
            need_watt = cpu.tdp_w + 100

            if gpu_id is not None:
                gpu = session.get(GPUDB, gpu_id)
                if gpu is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="ไม่พบ GPU นี้ในระบบค่ะ"
                    )
                need_watt = need_watt + gpu.tdp_w

            statement = statement.where(PSUDB.wattage_w >= need_watt)
        return session.exec(statement).all()


@app.get("/psus/{psu_id}", status_code=status.HTTP_200_OK)
def read_psu(psu_id: int) -> PSUOut:
    with Session(engine) as session:
        psu = session.get(PSUDB, psu_id)
        if psu is not None:
            return psu
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="ไม่พบ PSU นี้ในระบบค่ะ"
    )


@app.post("/psus/", status_code=status.HTTP_201_CREATED)
def create_psu(psu: PSU) -> PSUOut:
    new_psu = PSUDB(**psu.model_dump())
    with Session(engine) as session:
        session.add(new_psu)
        session.commit()
        session.refresh(new_psu)
        return new_psu


# =========================================================
# CASE
# =========================================================
# ถ้าส่ง mainboard_id มา จะแสดงเฉพาะเคสที่ใส่เมนบอร์ดขนาดนั้นได้
# ถ้าส่ง gpu_id มา จะแสดงเฉพาะเคสที่ใส่การ์ดจอตัวนั้นได้ (ความยาวไม่เกิน) 
@app.get("/cases/", status_code=status.HTTP_200_OK)
def read_cases(mainboard_id: int | None = None, gpu_id: int | None = None) -> list[CaseOut]:
    with Session(engine) as session:
        statement = select(CaseDB)

        if gpu_id is not None:
            gpu = session.get(GPUDB, gpu_id)
            if gpu is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="ไม่พบ GPU นี้ในระบบค่ะ"
                )
            statement = statement.where(CaseDB.max_gpu_length_mm >= gpu.length_mm)

        cases = session.exec(statement).all()
        if mainboard_id is None:
            return cases

        mainboard = session.get(MainboardDB, mainboard_id)
        if mainboard is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="ไม่พบ Mainboard นี้ในระบบค่ะ"
            )
        # ใช้ .where() ไม่ได้ เพราะคำว่า "ATX" ไปตรงกับ "Micro-ATX" ด้วย เลยต้องแยกคำแล้วเช็กทีละเคสค่ะ
        result = []
        for case in cases:
            if mainboard.form_factor in case.supported_form_factors.split(","):
                result.append(case)
        return result


@app.get("/cases/{case_id}", status_code=status.HTTP_200_OK)
def read_case(case_id: int) -> CaseOut:
    with Session(engine) as session:
        case = session.get(CaseDB, case_id)
        if case is not None:
            return case
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="ไม่พบ Case นี้ในระบบค่ะ"
    )


@app.post("/cases/", status_code=status.HTTP_201_CREATED)
def create_case(case: Case) -> CaseOut:
    new_case = CaseDB(**case.model_dump())
    with Session(engine) as session:
        session.add(new_case)
        session.commit()
        session.refresh(new_case)
        return new_case


# =========================================================
# CUSTOMER
# =========================================================
@app.get("/customers/", status_code=status.HTTP_200_OK)
def read_customers() -> list[CustomerOut]:
    with Session(engine) as session:
        return session.exec(select(CustomerDB)).all()


@app.get("/customers/{customer_id}", status_code=status.HTTP_200_OK)
def read_customer(customer_id: int) -> CustomerOut:
    with Session(engine) as session:
        customer = session.get(CustomerDB, customer_id)
        if customer is not None:
            return customer
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="ไม่พบลูกค้าคนนี้ในระบบค่ะ"
    )


@app.post("/customers/", status_code=status.HTTP_201_CREATED)
def create_customer(customer: Customer) -> CustomerOut:
    new_customer = CustomerDB(**customer.model_dump())
    with Session(engine) as session:
        session.add(new_customer)
        session.commit()
        session.refresh(new_customer)
        return new_customer


# ดูว่าลูกค้าคนนี้มีคอมพิวเตอร์ set อะไรบ้าง
@app.get("/customers/{customer_id}/pc-sets", status_code=status.HTTP_200_OK)
def read_sets_of_customer(customer_id: int) -> list[PCSetOut]:
    with Session(engine) as session:
        customer = session.get(CustomerDB, customer_id)
        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="ไม่พบลูกค้าคนนี้ในระบบค่ะ"
            )
        statement = select(PCSetDB).where(PCSetDB.customer_id == customer_id)
        return session.exec(statement).all()


# =========================================================
# PC SET
# =========================================================
# function ใช้ตรวจว่าชิ้นส่วนใน set ใช้ร่วมกันได้ไหม
# ถ้าผ่านทุกข้อจะคืนราคารวมของ set กลับไป
def check_pc_set(session: Session, pc_set: PCSet) -> float:
    customer = session.get(CustomerDB, pc_set.customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="ไม่พบลูกค้าคนนี้ในระบบค่ะ")

    cpu = session.get(CPUDB, pc_set.cpu_id)
    if cpu is None:
        raise HTTPException(status_code=404, detail="ไม่พบ CPU นี้ในระบบค่ะ")

    mainboard = session.get(MainboardDB, pc_set.mainboard_id)
    if mainboard is None:
        raise HTTPException(status_code=404, detail="ไม่พบ Mainboard นี้ในระบบค่ะ")

    ram = session.get(RAMDB, pc_set.ram_id)
    if ram is None:
        raise HTTPException(status_code=404, detail="ไม่พบ RAM นี้ในระบบค่ะ")

    # การ์ดจอไม่บังคับ ถ้าไม่ได้เลือกมา gpu จะเป็น None
    gpu = None
    if pc_set.gpu_id is not None:
        gpu = session.get(GPUDB, pc_set.gpu_id)
        if gpu is None:
            raise HTTPException(status_code=404, detail="ไม่พบ GPU นี้ในระบบค่ะ")

    storage = session.get(StorageDB, pc_set.storage_id)
    if storage is None:
        raise HTTPException(status_code=404, detail="ไม่พบ Storage นี้ในระบบค่ะ")

    psu = session.get(PSUDB, pc_set.psu_id)
    if psu is None:
        raise HTTPException(status_code=404, detail="ไม่พบ PSU นี้ในระบบค่ะ")

    case = session.get(CaseDB, pc_set.case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="ไม่พบ Case นี้ในระบบค่ะ")

    # 1. CPU กับเมนบอร์ดต้องใช้ socket เดียวกัน
    if cpu.socket != mainboard.socket:
        raise HTTPException(
            status_code=400,
            detail=f"CPU ใช้ socket {cpu.socket} แต่ Mainboard เป็น socket {mainboard.socket} ใช้ด้วยกันไม่ได้ค่ะ"
        )

    # 2. แรมต้องเป็นชนิดเดียวกับที่เมนบอร์ดรองรับ (DDR4 / DDR5)
    if ram.memory_type != mainboard.memory_type:
        raise HTTPException(
            status_code=400,
            detail=f"RAM เป็น {ram.memory_type} แต่ Mainboard รองรับ {mainboard.memory_type} ใช้ด้วยกันไม่ได้ค่ะ"
        )

    # 3. ขนาดเมนบอร์ดต้องใส่ในเคสได้
    if mainboard.form_factor not in case.supported_form_factors.split(","):
        raise HTTPException(
            status_code=400,
            detail=f"Mainboard ขนาด {mainboard.form_factor} ใส่ในเคสนี้ไม่ได้ค่ะ (เคสรองรับ {case.supported_form_factors})"
        )

    # 4. ถ้าไม่ใส่การ์ดจอ CPU ต้องมีกราฟิกในตัว ไม่อย่างนั้นจอจะไม่ติด
    if gpu is None and cpu.integrated_graphics is False:
        raise HTTPException(
            status_code=400,
            detail="CPU รุ่นนี้ไม่มีกราฟิกในตัว ต้องเลือกการ์ดจอด้วยค่ะ"
        )

    # 5. การ์ดจอต้องไม่ยาวเกินที่เคสรับได้
    if gpu is not None and gpu.length_mm > case.max_gpu_length_mm:
        raise HTTPException(
            status_code=400,
            detail=f"การ์ดจอยาว {gpu.length_mm} มม. แต่เคสใส่ได้สูงสุด {case.max_gpu_length_mm} มม. ค่ะ"
        )

    # 6. PSU ต้องจ่ายไฟพอ คิดจาก CPU+การ์ดจอ แล้วเผื่อชิ้นส่วนอื่นอีก 100W
    need_watt = cpu.tdp_w + 100
    if gpu is not None:
        need_watt = need_watt + gpu.tdp_w
    if psu.wattage_w < need_watt:
        raise HTTPException(
            status_code=400,
            detail=f"PSU {psu.wattage_w}W ไฟไม่พอค่ะ set นี้ต้องใช้อย่างน้อย {need_watt}W"
        )

    total_price = (
        cpu.price + mainboard.price + ram.price
        + storage.price + psu.price + case.price
    )
    if gpu is not None:
        total_price = total_price + gpu.price
    return total_price


# แสดง set ทั้งหมด หรือส่ง customer_id มาเพื่อดูเฉพาะของลูกค้าคนนั้น
@app.get("/pc-sets/", status_code=status.HTTP_200_OK)
def read_pc_sets(customer_id: int | None = None) -> list[PCSetOut]:
    with Session(engine) as session:
        statement = select(PCSetDB)
        if customer_id is not None:
            statement = statement.where(PCSetDB.customer_id == customer_id)
        return session.exec(statement).all()


@app.get("/pc-sets/{set_id}", status_code=status.HTTP_200_OK)
def read_pc_set(set_id: int) -> PCSetOut:
    with Session(engine) as session:
        pc_set = session.get(PCSetDB, set_id)
        if pc_set is not None:
            return pc_set
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="ไม่พบ computer set นี้ในระบบค่ะ"
    )


# แสดง set แบบละเอียด มีชื่อรุ่นและราคาของแต่ละชิ้น อันนี้ดูอ่านง่ายกว่าดูแค่เลข id ค่ะ
@app.get("/pc-sets/{set_id}/detail", status_code=status.HTTP_200_OK)
def read_pc_set_detail(set_id: int):
    with Session(engine) as session:
        pc_set = session.get(PCSetDB, set_id)
        if pc_set is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="ไม่พบ computer set นี้ในระบบค่ะ"
            )
        customer = session.get(CustomerDB, pc_set.customer_id)
        cpu = session.get(CPUDB, pc_set.cpu_id)
        mainboard = session.get(MainboardDB, pc_set.mainboard_id)
        ram = session.get(RAMDB, pc_set.ram_id)
        storage = session.get(StorageDB, pc_set.storage_id)
        psu = session.get(PSUDB, pc_set.psu_id)
        case = session.get(CaseDB, pc_set.case_id)

        gpu_text = "ไม่มี (ใช้กราฟิกในตัว CPU)"
        if pc_set.gpu_id is not None:
            gpu = session.get(GPUDB, pc_set.gpu_id)
            gpu_text = f"{gpu.brand} {gpu.gpu_name} ({gpu.price:,.0f} บาท)"

        return {
            "set_id": pc_set.set_id,
            "set_name": pc_set.set_name,
            "customer": customer.name,
            "cpu": f"{cpu.brand} {cpu.cpu_name} ({cpu.price:,.0f} บาท)",
            "mainboard": f"{mainboard.brand} {mainboard.mainboard_name} ({mainboard.price:,.0f} บาท)",
            "ram": f"{ram.brand} {ram.ram_name} ({ram.price:,.0f} บาท)",
            "gpu": gpu_text,
            "storage": f"{storage.brand} {storage.storage_name} ({storage.price:,.0f} บาท)",
            "psu": f"{psu.brand} {psu.psu_name} ({psu.price:,.0f} บาท)",
            "case": f"{case.brand} {case.case_name} ({case.price:,.0f} บาท)",
            "total_price": f"{pc_set.total_price:,.0f} บาท",
            "copied_from": pc_set.copied_from,
            "created_at": pc_set.created_at,
            "updated_at": pc_set.updated_at,
        }


@app.post("/pc-sets/", status_code=status.HTTP_201_CREATED)
def create_pc_set(pc_set: PCSet) -> PCSetOut:
    with Session(engine) as session:
        total_price = check_pc_set(session, pc_set)
        new_set = PCSetDB(**pc_set.model_dump(), total_price=total_price)
        session.add(new_set)
        session.commit()
        session.refresh(new_set)
        return new_set


# อัพเดท/สับเปลี่ยนอุปกรณ์ใน set จะตรวจความเข้ากันได้ใหม่ทุกครั้ง
@app.put("/pc-sets/{set_id}", status_code=status.HTTP_200_OK)
def update_pc_set(set_id: int, new_set: PCSet) -> PCSetOut:
    with Session(engine) as session:
        pc_set = session.get(PCSetDB, set_id)
        if pc_set is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="ไม่พบ computer set นี้ในระบบค่ะ"
            )

        total_price = check_pc_set(session, new_set)

        pc_set.customer_id = new_set.customer_id
        pc_set.set_name = new_set.set_name
        pc_set.cpu_id = new_set.cpu_id
        pc_set.mainboard_id = new_set.mainboard_id
        pc_set.ram_id = new_set.ram_id
        pc_set.gpu_id = new_set.gpu_id
        pc_set.storage_id = new_set.storage_id
        pc_set.psu_id = new_set.psu_id
        pc_set.case_id = new_set.case_id
        pc_set.total_price = total_price
        pc_set.updated_at = thai_now()
        session.add(pc_set)
        session.commit()
        session.refresh(pc_set)
        return pc_set


# คัดลอก set ที่มีอยู่ ไปเป็นต้นแบบให้ลูกค้าคนอื่น
@app.post("/pc-sets/{set_id}/copy", status_code=status.HTTP_201_CREATED)
def copy_pc_set(set_id: int, copy_info: CopySet) -> PCSetOut:
    with Session(engine) as session:
        old_set = session.get(PCSetDB, set_id)
        if old_set is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="ไม่พบ computer set ที่ต้องการคัดลอกค่ะ"
            )
        customer = session.get(CustomerDB, copy_info.customer_id)
        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="ไม่พบลูกค้าคนนี้ในระบบค่ะ"
            )

        new_set = PCSetDB(
            customer_id=copy_info.customer_id,
            set_name=copy_info.set_name,
            cpu_id=old_set.cpu_id,
            mainboard_id=old_set.mainboard_id,
            ram_id=old_set.ram_id,
            gpu_id=old_set.gpu_id,
            storage_id=old_set.storage_id,
            psu_id=old_set.psu_id,
            case_id=old_set.case_id,
            total_price=old_set.total_price,
            copied_from=old_set.set_id,
        )
        session.add(new_set)
        session.commit()
        session.refresh(new_set)
        return new_set