"use client";

import App from "./App";
import { AppProvider } from "./context/AppContext";

export default function LegacyApp() {
  return (
    <AppProvider>
      <App />
    </AppProvider>
  );
}
