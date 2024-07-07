import {
  createContext,
  ReactNode,
  useContext,
  useEffect,
  useState,
} from "react";
import { Repository } from "./schema";
import { useAuth } from "./auth";

interface RepoContextType {
  repositories: Repository[];
  fetchRepositories: () => Promise<void>;
}

const RepoContext = createContext<RepoContextType | null>(null);

// Context provider component
export const RepoProvider = ({ children }: { children: ReactNode }) => {
  const { userName } = useAuth();
  const [repositories, setRepositories] = useState<Repository[]>([]);

  useEffect(() => {
    async function fetchRepositories() {
      try {
        const response = await fetch(`/api/getAllRepo?username=${userName}`, {
          headers: {
            "Content-Type": "application/json",
          },
          method: "GET",
        });
        const data = await response.json();
        if (response.ok) {
          setRepositories(data);
        } else {
          console.error(data);
        }
      } catch (error) {
        console.error(error);
      }
    }
    fetchRepositories();
  }, [userName]);

  const fetchRepositories = async () => {
    try {
      const response = await fetch(`/api/getAllRepo?username=${userName}`, {
        headers: {
          "Content-Type": "application/json",
        },
        method: "GET",
      });
      const data = await response.json();
      if (response.ok) {
        setRepositories(data);
      } else {
        console.error(data);
      }
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <RepoContext.Provider value={{ repositories, fetchRepositories }}>
      {children}
    </RepoContext.Provider>
  );
};

// eslint-disable-next-line react-refresh/only-export-components
export function useRepo() {
  const context = useContext(RepoContext);
  if (!context) {
    throw new Error("useRepo must be used within an RepoProvider");
  }
  return context;
}
