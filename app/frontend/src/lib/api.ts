import axios from "axios";

// Determine base URL based on environment
const baseURL = typeof window === "undefined" 
  ? (process.env.INTERNAL_API_URL || "http://backend:8000/api/v1") 
  : "/api/v1";

export const api = axios.create({
  baseURL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const uploadApi = axios.create({
  baseURL,
  headers: {
    "Content-Type": "multipart/form-data",
  },
});

export interface Image {
  id: number;
  filename: string;
  mimetype: string;
  size: number;
  created_at: string;
  url: string;
}

export interface Video {
  id: number;
  filename: string;
  mimetype: string;
  size: number;
  duration: number;
  created_at: string;
  url: string;
}

export interface Post {
  id: number;
  title: string | null;
  content: string;
  created_at: string;
}
