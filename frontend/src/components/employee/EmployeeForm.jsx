import { useState } from "react";

const initialForm = {
  employeeId: "",
  fullName: "",
  email: "",
  department: "",
};

export default function EmployeeForm({ onSubmit, loading }) {
  const [form, setForm] = useState(initialForm);

  function updateField(event) {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  }

  async function submit(event) {
    event.preventDefault();
    await onSubmit(form);
    setForm(initialForm);
  }

  return (
    <form onSubmit={submit} className="card">
      <input name="employeeId" placeholder="Employee ID" value={form.employeeId} onChange={updateField} required />
      <input name="fullName" placeholder="Full Name" value={form.fullName} onChange={updateField} required />
      <input name="email" type="email" placeholder="Email" value={form.email} onChange={updateField} required />
      <input name="department" placeholder="Department" value={form.department} onChange={updateField} required />
      <button disabled={loading} type="submit">{loading ? "Adding..." : "Add Employee"}</button>
    </form>
  );
}
