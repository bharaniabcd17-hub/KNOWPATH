/**
 * Zustand Auth store for user session management.
 */

import { create } from "zustand";
import { User } from "@/types";
import { api } from "@/lib/api";

interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  error: string | null;
  initialize: () => Promise<void>;
  checkAuth: () => Promise<void>;
  login: (email: string, password: string) => Promise<void>;
  setSession: (token: string, user: User) => void;
  register: (data: { email: string; password: string; dob: string; consent_version?: string }) => Promise<void>;
  logout: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  token: null,
  isLoading: true,
  error: null,

  initialize: async () => {
    const token = api.getToken();
    if (!token) {
      set({ user: null, token: null, isLoading: false });
      return;
    }
    try {
      const user = await api.getMe();
      set({ user, token, isLoading: false, error: null });
    } catch {
      api.setToken(null);
      set({ user: null, token: null, isLoading: false });
    }
  },

  checkAuth: async () => {
    await get().initialize();
  },

  login: async (email: string, password: string) => {
    const res = await api.login({ email, password });
    const user: User = {
      id: res.user_id,
      email: res.email,
      role: (res.role as any) || "learner",
      is_verified: true,
      created_at: new Date().toISOString(),
    };
    set({ user, token: res.access_token, isLoading: false, error: null });
  },

  setSession: (token: string, user: User) => {
    api.setToken(token);
    set({ user, token, isLoading: false, error: null });
  },

  register: async (data) => {
    const res = await api.register(data);
    const user: User = {
      id: res.user_id,
      email: res.email,
      role: (res.role as any) || "learner",
      is_verified: true,
      created_at: new Date().toISOString(),
    };
    set({ user, token: res.access_token, isLoading: false, error: null });
  },

  logout: async () => {
    await api.logout();
    set({ user: null, token: null, isLoading: false, error: null });
  },
}));
