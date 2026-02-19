import { useEffect, useState } from "react";
import { NavLink } from "react-router-dom";

import AttendanceForm from "../components/attendance/AttendanceForm";
import AttendanceTable from "../components/attendance/AttendanceTable";
import ErrorState from "../components/common/ErrorState";
import Loader from "../components/common/Loader";
import { api, getErrorMessage } from "../services/api";

function navClass({ isActive }) {
  return isActive ? "nav-link active" : "nav-link";
}

export default function AttendancePage() {
  const [records, setRecords] = useState([]);
  const [employeeId, setEmployeeId] = useState("");
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  async function loadAttendance(targetEmployeeId) {
    const normalizedEmployeeId = targetEmployeeId.trim().toUpperCase();
    if (!normalizedEmployeeId) {
      setRecords([]);
      return;
    }

    setLoading(true);
    setError("");
    try {
      const res = await api.getAttendanceByEmployee(normalizedEmployeeId);
      setRecords(res.data || []);
    } catch (err) {
      setRecords([]);
      setError(getErrorMessage(err, "Failed to fetch attendance"));
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
    setSubmitting(true);
    try {
      await api.markAttendance(payload);
      await loadAttendance(payload.employeeId);
    } catch (err) {
      window.alert(getErrorMessage(err, "Unable to mark attendance."));
      throw err;
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="container">
      <header className="page-header">
        <div>
          <p className="eyebrow">Attendance Tracking</p>
          <h1>Daily Punch Register</h1>
          <p className="subtitle">Mark daily status with punch-in and punch-out times for each employee.</p>
        </div>
        <div className="stat-pill">
          <span>Visible Records</span>
          <strong>{records.length}</strong>
        </div>
      </header>

      <nav className="nav-strip" aria-label="Primary navigation">
        <NavLink to="/" className={navClass}>Employees</NavLink>
        <NavLink to="/attendance" className={navClass}>Daily Attendance</NavLink>
        <NavLink to="/attendance/monthly" className={navClass}>Monthly Attendance</NavLink>
      </nav>

      <AttendanceForm onSubmit={handleMark} onEmployeeChange={setEmployeeId} loading={submitting} />
      {loading ? <Loader /> : null}
      {error ? <ErrorState message={error} onRetry={() => loadAttendance(employeeId)} /> : null}
      {!loading && !error ? <AttendanceTable records={records} /> : null}
    </main>
  );
}