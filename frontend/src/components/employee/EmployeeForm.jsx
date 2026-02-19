import { useState } from "react";

const initialForm = {
  employeeId: "",
  fullName: "",
  email: "",
  department: "",
};

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email);
}

export default function EmployeeForm({ onSubmit, loading }) {
  const [form, setForm] = useState(initialForm);

  function updateField(event) {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  }

  async function submit(event) {
    event.preventDefault();

    const payload = {
      employeeId: form.employeeId.trim().toUpperCase(),
      fullName: form.fullName.trim(),
      email: form.email.trim().toLowerCase(),
      department: form.department.trim(),
    };

    if (!/^[A-Z0-9_-]+$/.test(payload.employeeId)) {
      window.alert("Employee ID can only contain letters, numbers, underscore, and hyphen.");
      return;
    }

    if (payload.fullName.length < 2 || payload.department.length < 2) {
      window.alert("Full Name and Department must be at least 2 characters.");
      return;
    }

    if (!isValidEmail(payload.email)) {
      window.alert("Invalid email format. Enter a valid email like name@example.com.");
      return;
    }

    try {
      await onSubmit(payload);
      setForm(initialForm);
    } catch {
      // Error popup is shown by parent page.
    }
  }

  return (
    <form onSubmit={submit} className="card form-card">
      <div className="form-grid">
        <label className="field">
          <span>Employee ID</span>
          <input name="employeeId" placeholder="EMP001" value={form.employeeId} onChange={updateField} required />
        </label>

        <label className="field">
          <span>Full Name</span>
          <input name="fullName" placeholder="John Doe" value={form.fullName} onChange={updateField} required />
        </label>

        <label className="field">
          <span>Email</span>
          <input name="email" type="email" placeholder="john@example.com" value={form.email} onChange={updateField} required />
        </label>

        <label className="field">
          <span>Department</span>
          <input name="department" placeholder="Engineering" value={form.department} onChange={updateField} required />
        </label>
      </div>

      <div className="form-actions">
        <button className="btn btn-primary" disabled={loading} type="submit">{loading ? "Adding..." : "Add Employee"}</button>
      </div>
    </form>
  );
}