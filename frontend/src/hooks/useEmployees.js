import { useCallback, useState } from "react";

import { api } from "../services/api";

export function useEmployees() {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchEmployees = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const res = await api.getEmployees();
      setEmployees(res.data || []);
    } catch (err) {
      setError(err.message || "Failed to fetch employees");
    } finally {
      setLoading(false);
    }
  }, []);

  const createEmployee = useCallback(
    async (payload) => {
      await api.createEmployee(payload);
      await fetchEmployees();
    },
    [fetchEmployees]
  );

  const deleteEmployee = useCallback(
    async (employeeId) => {
      await api.deleteEmployee(employeeId);
      await fetchEmployees();
    },
    [fetchEmployees]
  );

  return { employees, loading, error, fetchEmployees, createEmployee, deleteEmployee };
}
