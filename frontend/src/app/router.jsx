import { createBrowserRouter } from "react-router-dom";

import AttendancePage from "../pages/AttendancePage";
import EmployeesPage from "../pages/EmployeesPage";

export const router = createBrowserRouter([
  { path: "/", element: <EmployeesPage /> },
  { path: "/attendance", element: <AttendancePage /> },
]);
