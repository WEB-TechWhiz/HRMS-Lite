import EmptyState from "../common/EmptyState";

export default function AttendanceTable({ records }) {
  if (!records.length) {
    return <EmptyState message="No attendance records yet." />;
  }

  return (
    <table className="table">
      <thead>
        <tr>
          <th>Date</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {records.map((record) => (
          <tr key={record.id}>
            <td>{record.date}</td>
            <td>{record.status}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
