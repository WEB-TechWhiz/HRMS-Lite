import { useEffect, useState } from "react";

import EmployeeForm from "../components/employee/EmployeeForm";
import EmployeeTable from "../components/employee/EmployeeTable";
import ErrorState from "../components/common/ErrorState";
import Loader from "../components/common/Loader";
import { useEmployees } from "../hooks/useEmployees";

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
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="container">
      <h1>HRMS Lite - Employees</h1>
      <EmployeeForm onSubmit={handleCreate} loading={submitting} />
      {loading ? <Loader /> : null}
      {error ? <ErrorState message={error} onRetry={fetchEmployees} /> : null}
      {!loading && !error ? <EmployeeTable employees={employees} onDelete={deleteEmployee} /> : null}
    </main>
  );
}
