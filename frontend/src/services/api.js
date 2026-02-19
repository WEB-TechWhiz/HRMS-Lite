import axios from "axios";

import { API_BASE_URL } from "../utils/constants";

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

function unwrap(response) {
  const payload = response.data;
  if (!payload?.success) {
    throw new Error(payload?.message || "Request failed");
  }
  return payload;
}

export const api = {
  async getEmployees() {
    return unwrap(await client.get("/employees"));
  },
  async createEmployee(payload) {
    return unwrap(await client.post("/employees", payload));
  },
  async deleteEmployee(employeeId) {
    return unwrap(await client.delete(`/employees/${employeeId}`));
  },
  async markAttendance(payload) {
    return unwrap(await client.post("/attendance", payload));
  },
  async getAttendanceByEmployee(employeeId) {
    return unwrap(await client.get(`/attendance/${employeeId}`));
  },
};
