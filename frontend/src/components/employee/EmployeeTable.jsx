import EmptyState from "../common/EmptyState";

export default function EmployeeTable({ employees, onDelete }) {
  if (!employees.length) {
    return <EmptyState message="No employees added yet." />;
  }

  return (
    <section className="table-card">
      <table className="table">
        <thead>
          <tr>
            <th>Employee ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Department</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {employees.map((employee) => (
            <tr key={employee.employeeId}>
              <td><span className="mono">{employee.employeeId}</span></td>
              <td>{employee.fullName}</td>
              <td>{employee.email}</td>
              <td>{employee.department}</td>
              <td>
                <button className="btn btn-danger btn-sm" type="button" onClick={() => onDelete(employee.employeeId)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}