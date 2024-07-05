import { createContext, useContext, useState, ReactNode } from "react";
import { Navigate } from "react-router-dom";

interface AuthContextType {
  isLoggedIn: boolean;
  userName: string;
  login: (name: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(
    !!localStorage.getItem("user")
  );
  const [userName, setUserName] = useState<string>(
    localStorage.getItem("user") || ""
  );

  const login = (name: string) => {
    setIsLoggedIn(true);
    localStorage.setItem("user", name);
    setUserName(name);
  };

  const logout = () => {
    setIsLoggedIn(false);
    localStorage.setItem("user", "");
    setUserName("");
  };

  return (
    <AuthContext.Provider value={{ isLoggedIn, userName, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// eslint-disable-next-line react-refresh/only-export-components
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}

export function ProtectedRoute({ children }: { children: JSX.Element }) {
  const { isLoggedIn } = useAuth();

  if (!isLoggedIn) {
    return <Navigate to="/login" replace />;
  }

  return children;
}
