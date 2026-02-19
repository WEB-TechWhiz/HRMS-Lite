import { useMemo, useState } from "react";
import { NavLink } from "react-router-dom";

import AttendanceTable from "../components/attendance/AttendanceTable";
import ErrorState from "../components/common/ErrorState";
import Loader from "../components/common/Loader";
import { api, getErrorMessage } from "../services/api";

function escapeCsv(value) {
  if (value === null || value === undefined) {
    return "";
  }

  const text = String(value);
  if (/[",\n]/.test(text)) {
    return `"${text.replace(/"/g, '""')}"`;
  }
  return text;
}

function downloadCsv(rows, filename) {
  const csvContent = rows.map((row) => row.map(escapeCsv).join(",")).join("\n");
  const blob = new Blob([`\uFEFF${csvContent}`], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();

  URL.revokeObjectURL(url);
}

function getCurrentMonthValue() {
  const date = new Date();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  return `${date.getFullYear()}-${month}`;
}

function navClass({ isActive }) {
  return isActive ? "nav-link active" : "nav-link";
}

export default function MonthlyAttendancePage() {
  const [employeeId, setEmployeeId] = useState("");
  const [monthValue, setMonthValue] = useState(getCurrentMonthValue());
  const [records, setRecords] = useState([]);
  const [meta, setMeta] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const maxMonth = useMemo(() => getCurrentMonthValue(), []);

  async function loadMonthlyAttendance() {
    const normalizedEmployeeId = employeeId.trim().toUpperCase();
    if (!normalizedEmployeeId) {
      window.alert("Employee ID is required.");
      return;
    }

    if (!monthValue) {
      window.alert("Month is required.");
      return;
    }

    const [year, month] = monthValue.split("-").map((value) => Number(value));

    setLoading(true);
    setError("");
    try {
      const response = await api.getMonthlyAttendance(normalizedEmployeeId, year, month);
      setRecords(response.data || []);
      setMeta(response.meta || null);
    } catch (err) {
      setRecords([]);
      setMeta(null);
      setError(getErrorMessage(err, "Unable to load monthly attendance."));
    } finally {
      setLoading(false);
    }
  }

  function exportMonthlyCsv() {
    if (!records.length) {
      window.alert("No monthly attendance data available to export.");
      return;
    }

    const normalizedEmployeeId = employeeId.trim().toUpperCase();
    const rows = [
      ["Employee ID", "Date", "Status", "Punch In", "Punch Out"],
      ...records.map((record) => [
        normalizedEmployeeId || record.employeeId,
        record.date,
        record.status,
        record.punchInTime || "",
        record.punchOutTime || "",
      ]),
    ];

    const safeEmployeeId = (normalizedEmployeeId || "employee").replace(/[^A-Z0-9_-]/gi, "_");
    const safeMonth = (monthValue || "month").replace(/[^0-9-]/g, "_");
    downloadCsv(rows, `attendance_${safeEmployeeId}_${safeMonth}.csv`);
  }

  return (
    <main className="container">
      <header className="page-header">
        <div>
          <p className="eyebrow">Analytics View</p>
          <h1>Monthly Attendance Sheet</h1>
          <p className="subtitle">Review complete month-level attendance and export as CSV for reporting.</p>
        </div>
        <div className="stat-pill">
          <span>Marked Days</span>
          <strong>{meta ? meta.totalMarked : 0}</strong>
        </div>
      </header>

      <nav className="nav-strip" aria-label="Primary navigation">
        <NavLink to="/" className={navClass}>Employees</NavLink>
        <NavLink to="/attendance" className={navClass}>Daily Attendance</NavLink>
        <NavLink to="/attendance/monthly" className={navClass}>Monthly Attendance</NavLink>
      </nav>

      <form
        className="card form-card"
        onSubmit={(event) => {
          event.preventDefault();
          loadMonthlyAttendance();
        }}
      >
        <div className="form-grid form-grid-3">
          <label className="field">
            <span>Employee ID</span>
            <input
              placeholder="EMP001"
              value={employeeId}
              onChange={(event) => setEmployeeId(event.target.value.toUpperCase())}
              required
            />
          </label>
          <label className="field">
            <span>Month</span>
            <input type="month" value={monthValue} max={maxMonth} onChange={(event) => setMonthValue(event.target.value)} required />
          </label>
        </div>
        <div className="form-actions">
          <button className="btn btn-primary" type="submit" disabled={loading}>{loading ? "Loading..." : "Load Monthly Attendance"}</button>
          <button className="btn btn-soft" type="button" onClick={exportMonthlyCsv} disabled={loading || !records.length}>Export CSV</button>
        </div>
      </form>

      {meta ? <p className="summary-text">Month Summary: {meta.totalMarked} marked days out of {meta.totalDays}</p> : null}

      {loading ? <Loader /> : null}
      {error ? <ErrorState message={error} onRetry={loadMonthlyAttendance} /> : null}
      {!loading && !error ? <AttendanceTable records={records} /> : null}
    </main>
  );
}