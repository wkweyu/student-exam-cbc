import { createContext, useState, useEffect } from "react";
import api, { setAuthToken } from "../api/axios";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem("token"));

  useEffect(() => {
    setAuthToken(token);
  }, [token]);

  const login = async (username, password) => {
    const response = await api.post("/auth/login/", { username, password });
    localStorage.setItem("token", response.data.key);
    setToken(response.data.key);
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  return (
    <AuthContext.Provider value={{ token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
