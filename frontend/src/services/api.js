import axios from "axios";

import { API_BASE_URL } from "../utils/constants";

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export class ApiError extends Error {
  constructor(message, options = {}) {
    super(message);
    this.name = "ApiError";
    this.code = options.code || null;
    this.status = options.status || null;
    this.details = options.details || null;
    this.isNetwork = Boolean(options.isNetwork);
  }
}

function normalizePayloadError(payload, status) {
  return new ApiError(payload?.message || "Request failed", {
    code: payload?.error?.code,
    status,
    details: payload?.error?.details,
  });
}

function toApiError(error) {
  if (error instanceof ApiError) {
    return error;
  }

  if (axios.isAxiosError(error)) {
    if (!error.response) {
      return new ApiError("Network error. Please check backend/server connection.", {
        isNetwork: true,
      });
    }

    const payload = error.response.data;
    if (payload && typeof payload === "object") {
      return normalizePayloadError(payload, error.response.status);
    }

    return new ApiError(`Request failed with status ${error.response.status}`, {
      status: error.response.status,
    });
  }

  return new ApiError(error?.message || "Unexpected error");
}

function unwrap(response) {
  const payload = response.data;
  if (!payload?.success) {
    throw normalizePayloadError(payload, response.status);
  }
  return payload;
}

async function request(promise) {
  try {
    const response = await promise;
    return unwrap(response);
  } catch (error) {
    throw toApiError(error);
  }
}

function hasValidationField(error, fieldName) {
  if (!(error instanceof ApiError)) {
    return false;
  }

  const issues = error.details?.errors;
  if (!Array.isArray(issues)) {
    return false;
  }

  return issues.some((issue) => Array.isArray(issue?.loc) && issue.loc.includes(fieldName));
}

export function getErrorMessage(error, fallback = "Something went wrong") {
  if (!(error instanceof ApiError)) {
    return error?.message || fallback;
  }

  if (error.isNetwork) {
    return "Network error: backend may be down or API URL is unreachable.";
  }

  if (error.code === "DUPLICATE_EMPLOYEE") {
    return "Duplicate employee: Employee ID or email already exists.";
  }

  if (error.code === "DUPLICATE_ATTENDANCE") {
    return "Attendance already marked for this employee on this date.";
  }

  if (error.code === "VALIDATION_ERROR" && hasValidationField(error, "email")) {
    return "Invalid email format. Enter a valid email like name@example.com.";
  }

  if (error.code === "VALIDATION_ERROR") {
    return "Invalid input data. Please check all fields and try again.";
  }

  if (error.code === "NOT_FOUND") {
    return "Employee not found. Please use a valid Employee ID.";
  }

  return error.message || fallback;
}

export const api = {
  async getEmployees() {
    return request(client.get("/employees"));
  },
  async createEmployee(payload) {
    return request(client.post("/employees", payload));
  },
  async deleteEmployee(employeeId) {
    return request(client.delete(`/employees/${employeeId}`));
  },
  async markAttendance(payload) {
    return request(client.post("/attendance", payload));
  },
  async getAttendanceByEmployee(employeeId) {
    return request(client.get(`/attendance/${employeeId}`));
  },
  async getMonthlyAttendance(employeeId, year, month) {
    return request(client.get(`/attendance/monthly/${employeeId}?year=${year}&month=${month}`));
  },
};