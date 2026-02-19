from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.employee import Employee


def get_by_employee_id(db: Session, employee_id: str) -> Employee | None:
    return db.scalar(select(Employee).where(Employee.employee_id == employee_id))


def get_by_email(db: Session, email: str) -> Employee | None:
    return db.scalar(select(Employee).where(Employee.email == email))


def list_all(db: Session) -> list[Employee]:
    return list(db.scalars(select(Employee).order_by(Employee.id.desc())).all())


def create(db: Session, employee_id: str, full_name: str, email: str, department: str) -> Employee:
    employee = Employee(
        employee_id=employee_id,
        full_name=full_name,
        email=email,
        department=department,
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def delete(db: Session, employee: Employee) -> None:
    db.delete(employee)
    db.commit()
