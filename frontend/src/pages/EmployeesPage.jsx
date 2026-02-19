import { useEffect, useState } from "react";
import { NavLink } from "react-router-dom";

import EmployeeForm from "../components/employee/EmployeeForm";
import EmployeeTable from "../components/employee/EmployeeTable";
import ErrorState from "../components/common/ErrorState";
import Loader from "../components/common/Loader";
import { getErrorMessage } from "../services/api";
import { useEmployees } from "../hooks/useEmployees";

function navClass({ isActive }) {
  return isActive ? "nav-link active" : "nav-link";
}

export default function EmployeesPage() {
  const { employees, loading, error, fetchEmployees, createEmployee, deleteEmployee } = useEmployees();
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchEmployees();
  }, [fetchEmployees]);

  async function handleCreate(payload) {
    setSubmitting(true);
    try {
      await createEmployee(payload);
    } catch (err) {
      window.alert(getErrorMessage(err, "Unable to create employee."));
      throw err;
    } finally {
      setSubmitting(false);
    }
  }

  async function handleDelete(employeeId) {
    const confirmed = window.confirm(`Delete employee ${employeeId}? This also removes attendance records.`);
    if (!confirmed) {
      return;
    }

    try {
      await deleteEmployee(employeeId);
    } catch (err) {
      window.alert(getErrorMessage(err, "Unable to delete employee."));
    }
  }

  return (
    <main className="container">
      <header className="page-header">
        <div>
          <p className="eyebrow">Human Resource Management</p>
          <h1>Employees Workspace</h1>
          <p className="subtitle">Create and manage employee records with clean validation and duplicate protection.</p>
        </div>
        <div className="stat-pill">
          <span>Total Employees</span>
          <strong>{employees.length}</strong>
        </div>
      </header>

      <nav className="nav-strip" aria-label="Primary navigation">
        <NavLink to="/" className={navClass}>Employees</NavLink>
        <NavLink to="/attendance" className={navClass}>Daily Attendance</NavLink>
        <NavLink to="/attendance/monthly" className={navClass}>Monthly Attendance</NavLink>
      </nav>

      <EmployeeForm onSubmit={handleCreate} loading={submitting} />
      {loading ? <Loader /> : null}
      {error ? <ErrorState message={error} onRetry={fetchEmployees} /> : null}
      {!loading && !error ? <EmployeeTable employees={employees} onDelete={handleDelete} /> : null}
    </main>
  );
}