import { useMemo, useState } from "react";

const initialForm = {
  employeeId: "",
  date: "",
  status: "Present",
  punchInTime: "",
  punchOutTime: "",
};

export default function AttendanceForm({ onSubmit, onEmployeeChange, loading }) {
  const [form, setForm] = useState(initialForm);

  const today = useMemo(() => new Date().toISOString().split("T")[0], []);

  function updateField(event) {
    const { name, value } = event.target;
    const normalized = name === "employeeId" ? value.toUpperCase() : value;

    setForm((prev) => ({ ...prev, [name]: normalized }));

    if (name === "employeeId") {
      onEmployeeChange(normalized);
    }
  }

  async function submit(event) {
    event.preventDefault();

    const payload = {
      employeeId: form.employeeId.trim().toUpperCase(),
      date: form.date,
      status: form.status,
      punchInTime: form.punchInTime || null,
      punchOutTime: form.punchOutTime || null,
    };

    if (!payload.employeeId || !payload.date) {
      window.alert("Employee ID and Date are required.");
      return;
    }

    if (payload.punchOutTime && !payload.punchInTime) {
      window.alert("Punch-out time requires punch-in time.");
      return;
    }

    if (payload.punchInTime && payload.punchOutTime && payload.punchOutTime < payload.punchInTime) {
      window.alert("Punch-out time cannot be earlier than punch-in time.");
      return;
    }

    if (payload.status === "Absent" && (payload.punchInTime || payload.punchOutTime)) {
      window.alert("Absent status cannot include punch times.");
      return;
    }

    try {
      await onSubmit(payload);
    } catch {
      // Error popup is shown by parent page.
    }
  }

  return (
    <form onSubmit={submit} className="card form-card">
      <div className="form-grid form-grid-3">
        <label className="field">
          <span>Employee ID</span>
          <input name="employeeId" placeholder="EMP001" value={form.employeeId} onChange={updateField} required />
        </label>

        <label className="field">
          <span>Date</span>
          <input name="date" type="date" max={today} value={form.date} onChange={updateField} required />
        </label>

        <label className="field">
          <span>Status</span>
          <select name="status" value={form.status} onChange={updateField}>
            <option value="Present">Present</option>
            <option value="Absent">Absent</option>
          </select>
        </label>

        <label className="field">
          <span>Punch In</span>
          <input name="punchInTime" type="time" value={form.punchInTime} onChange={updateField} />
        </label>

        <label className="field">
          <span>Punch Out</span>
          <input name="punchOutTime" type="time" value={form.punchOutTime} onChange={updateField} />
        </label>
      </div>

      <div className="form-actions">
        <button className="btn btn-primary" disabled={loading} type="submit">{loading ? "Marking..." : "Mark Attendance"}</button>
      </div>
    </form>
  );
}