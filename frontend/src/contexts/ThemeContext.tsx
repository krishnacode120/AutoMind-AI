import { createContext, type ReactNode, useContext } from "react";

type ThemeContextValue = {
  theme: "dark";
};

const ThemeContext = createContext<ThemeContextValue>({ theme: "dark" });

type ThemeProviderProps = {
  children: ReactNode;
};

export function ThemeProvider({ children }: ThemeProviderProps) {
  return (
    <ThemeContext.Provider value={{ theme: "dark" }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  return useContext(ThemeContext);
}
