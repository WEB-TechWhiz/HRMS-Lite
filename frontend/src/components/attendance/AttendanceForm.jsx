import { useState } from "react";

const initialForm = {
  employeeId: "",
  date: "",
  status: "Present",
};

export default function AttendanceForm({ onSubmit, onEmployeeChange }) {
  const [form, setForm] = useState(initialForm);

  function updateField(event) {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    if (name === "employeeId") {
      onEmployeeChange(value);
    }
  }

  async function submit(event) {
    event.preventDefault();
    await onSubmit(form);
  }

  return (
    <form onSubmit={submit} className="card">
      <input name="employeeId" placeholder="Employee ID" value={form.employeeId} onChange={updateField} required />
      <input name="date" type="date" value={form.date} onChange={updateField} required />
      <select name="status" value={form.status} onChange={updateField}>
        <option value="Present">Present</option>
        <option value="Absent">Absent</option>
      </select>
      <button type="submit">Mark Attendance</button>
    </form>
  );
}
