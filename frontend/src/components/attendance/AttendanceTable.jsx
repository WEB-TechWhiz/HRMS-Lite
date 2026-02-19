import EmptyState from "../common/EmptyState";

function formatTime(value) {
  if (!value) {
    return "--";
  }

  return value.slice(0, 5);
}

function statusClass(status) {
  return status === "Present" ? "status-badge status-present" : "status-badge status-absent";
}

export default function AttendanceTable({ records }) {
  if (!records.length) {
    return <EmptyState message="No attendance records yet." />;
  }

  return (
    <section className="table-card">
      <table className="table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Status</th>
            <th>Punch In</th>
            <th>Punch Out</th>
          </tr>
        </thead>
        <tbody>
          {records.map((record, index) => (
            <tr key={record.id ?? `${record.employeeId}-${record.date}-${index}`}>
              <td>{record.date}</td>
              <td><span className={statusClass(record.status)}>{record.status}</span></td>
              <td><span className="mono">{formatTime(record.punchInTime)}</span></td>
              <td><span className="mono">{formatTime(record.punchOutTime)}</span></td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}