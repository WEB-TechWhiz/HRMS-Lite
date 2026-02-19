import EmptyState from "../common/EmptyState";

export default function EmployeeTable({ employees, onDelete }) {
  if (!employees.length) {
    return <EmptyState message="No employees added yet." />;
  }

  return (
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
            <td>{employee.employeeId}</td>
            <td>{employee.fullName}</td>
            <td>{employee.email}</td>
            <td>{employee.department}</td>
            <td>
              <button type="button" onClick={() => onDelete(employee.employeeId)}>Delete</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
