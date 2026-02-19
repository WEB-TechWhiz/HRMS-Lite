import { useEffect, useState } from "react";

import AttendanceForm from "../components/attendance/AttendanceForm";
import AttendanceTable from "../components/attendance/AttendanceTable";
import ErrorState from "../components/common/ErrorState";
import Loader from "../components/common/Loader";
import { api } from "../services/api";

export default function AttendancePage() {
  const [records, setRecords] = useState([]);
  const [employeeId, setEmployeeId] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function loadAttendance(targetEmployeeId) {
    if (!targetEmployeeId) return;
    setLoading(true);
    setError("");
    try {
      const res = await api.getAttendanceByEmployee(targetEmployeeId);
      setRecords(res.data || []);
    } catch (err) {
      setError(err.message || "Failed to fetch attendance");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (employeeId) {
      loadAttendance(employeeId);
    }
  }, [employeeId]);

  async function handleMark(payload) {
    await api.markAttendance(payload);
    await loadAttendance(payload.employeeId);
  }

  return (
    <main className="container">
      <h1>HRMS Lite - Attendance</h1>
      <AttendanceForm onSubmit={handleMark} onEmployeeChange={setEmployeeId} />
      {loading ? <Loader /> : null}
      {error ? <ErrorState message={error} onRetry={() => loadAttendance(employeeId)} /> : null}
      {!loading && !error ? <AttendanceTable records={records} /> : null}
    </main>
  );
}
