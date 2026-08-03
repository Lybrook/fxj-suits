#!/usr/bin/env python3
"""Write the new FXJ Suits Login.tsx"""

content = '''import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAppContext } from "../context/AppContext";

/* =============================================
   FXJ SUITS — Login Page
   Gen Z-aligned: mobile-first, bold, authentic
   Brand: Fikia × Jenga Tech
============================================= */

export default function Login() {
  const { setCurrentUser, firmName } = useAppContext();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    document.title = `${firmName} — Login`;
  }, [firmName]);

  const handleRequestReset = () => navigate("/reset-password");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const { supabase } = await import("../lib/supabaseClient");
      const { data: authData, error: authError } = await supabase.auth.signInWithPassword({ email, password });
      if (authError) throw authError;
      const userId = authData.user?.id;
      if (!userId) throw new Error("No user ID returned.");
      const { data: userData, error: userError } = await supabase
        .from("users")
        .select("*")
        .eq("id", userId)
        .single();
      if (userError || !userData) throw new Error("User profile not found.");
      setCurrentUser(userData);
      const redirectMap: Record<string, string> = {
        admin: "/",
        manager: "/",
        managing_partner: "/",
        accountant: "/accountant-dashboard",
        lawyer: "/lawyer-dashboard",
        clerk: "/clerk-dashboard",
      };
      navigate(redirectMap[userData.role] || "/");
    } catch (err: any) {
      setError(err.message || "Invalid credentials. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.page}>
      {/* Background pattern */}
      <div style={styles.bgPattern} aria-hidden="true" />

      <div style={styles.card}>
        {/* Logo mark */}
        <div style={styles.logoWrap}>
          <div style={styles.logoMark}>
            <span style={styles.logoInitials}>FXJ</span>
          </div>
        </div>

        {/* Heading */}
        <h1 style={styles.title}>FXJ Suits</h1>
        <p style={styles.subtitle}>{firmName}</p>
        <p style={styles.tagline}>Law Firm Management System</p>

        {/* Divider */}
        <div style={styles.divider} />

        {/* Error */}
        {error && <div style={styles.error} role="alert">{error}</div>}

        {/* Form */}
        <form onSubmit={handleSubmit} noValidate>
          <div style={styles.field}>
            <label style={styles.label} htmlFor="email">Email Address</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="advocate@lawfirm.co.ke"
              required
              autoComplete="email"
              style={styles.input}
            />
          </div>

          <div style={styles.field}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
              <label style={styles.label} htmlFor="password">Password</label>
              <span onClick={handleRequestReset} style={styles.forgotLink} role="button" tabIndex={0}>
                Forgot Password?
              </span>
            </div>
            <div style={{ position: "relative" }}>
              <input
                id="password"
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                autoComplete="current-password"
                style={{ ...styles.input, paddingRight: 44 }}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                aria-label={showPassword ? "Hide password" : "Show password"}
                style={styles.eyeBtn}
              >
                {showPassword ? (
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                    <line x1="1" y1="1" x2="23" y2="23"/>
                  </svg>
                ) : (
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                    <circle cx="12" cy="12" r="3"/>
                  </svg>
                )}
              </button>
            </div>
          </div>

          <button type="submit" style={styles.button} disabled={loading}>
            {loading ? (
              <span style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 8 }}>
                <span style={styles.spinner} /> Signing In...
              </span>
            ) : (
              "Sign In →"
            )}
          </button>
        </form>

        {/* Footer */}
        <p style={styles.footer}>
          © {new Date().getFullYear()} FXJ Suits · Powered by{" "}
          <a href="https://fikiaxjenga.co.ke" target="_blank" rel="noopener noreferrer" style={styles.footerLink}>
            Fikia × Jenga Tech
          </a>
        </p>
      </div>
    </div>
  );
}

/* =============================================
   STYLES
============================================= */
const styles: { [key: string]: React.CSSProperties } = {
  page: {
    minHeight: "100vh",
    background: "linear-gradient(135deg, #403301 0%, #856A00 60%, #403301 100%)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    padding: "20px",
    position: "relative",
    overflow: "hidden",
  },
  bgPattern: {
    position: "absolute",
    inset: 0,
    backgroundImage: `radial-gradient(circle at 20% 20%, rgba(239,191,4,0.08) 0%, transparent 50%),
                      radial-gradient(circle at 80% 80%, rgba(239,191,4,0.06) 0%, transparent 50%)`,
    pointerEvents: "none",
  },
  card: {
    width: "100%",
    maxWidth: 400,
    backgroundColor: "#FFF9E6",
    padding: "40px 36px",
    borderRadius: 20,
    boxShadow: "0 24px 60px rgba(64,51,1,0.35), 0 0 0 1px rgba(239,191,4,0.15)",
    textAlign: "center",
    position: "relative",
    zIndex: 1,
  },
  logoWrap: {
    display: "flex",
    justifyContent: "center",
    marginBottom: 16,
  },
  logoMark: {
    width: 64,
    height: 64,
    borderRadius: 18,
    background: "linear-gradient(135deg, #EFBF04 0%, #C2B067 100%)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    boxShadow: "0 4px 20px rgba(239,191,4,0.4)",
  },
  logoInitials: {
    fontSize: 22,
    fontWeight: 900,
    color: "#403301",
    letterSpacing: "-0.5px",
    fontFamily: "'Playfair Display', serif",
  },
  title: {
    margin: "0 0 4px",
    fontSize: 26,
    fontWeight: 900,
    color: "#403301",
    fontFamily: "'Playfair Display', serif",
    letterSpacing: "-0.5px",
  },
  subtitle: {
    margin: "0 0 2px",
    fontSize: 14,
    fontWeight: 600,
    color: "#856A00",
  },
  tagline: {
    margin: 0,
    fontSize: 11,
    color: "#C2B067",
    letterSpacing: "0.08em",
    textTransform: "uppercase" as const,
    fontWeight: 600,
  },
  divider: {
    height: 1,
    background: "linear-gradient(90deg, transparent, #E8D98A, transparent)",
    margin: "24px 0",
  },
  field: {
    marginBottom: 18,
    textAlign: "left",
  },
  label: {
    display: "block",
    fontSize: 12,
    fontWeight: 700,
    color: "#403301",
    letterSpacing: "0.04em",
    textTransform: "uppercase" as const,
  },
  forgotLink: {
    fontSize: 11,
    fontWeight: 700,
    color: "#856A00",
    cursor: "pointer",
    textTransform: "uppercase" as const,
    letterSpacing: "0.05em",
    textDecoration: "underline",
    textDecorationColor: "transparent",
  },
  input: {
    width: "100%",
    padding: "12px 14px",
    fontSize: 14,
    borderRadius: 10,
    border: "1.5px solid #E8D98A",
    outline: "none",
    boxSizing: "border-box" as const,
    backgroundColor: "#FFFDF0",
    color: "#1A1200",
    transition: "border-color 0.2s ease, box-shadow 0.2s ease",
    marginTop: 6,
  },
  eyeBtn: {
    position: "absolute",
    right: 12,
    top: "50%",
    transform: "translateY(-50%)",
    background: "none",
    border: "none",
    cursor: "pointer",
    color: "#856A00",
    display: "flex",
    alignItems: "center",
    padding: 0,
  },
  button: {
    width: "100%",
    padding: "14px",
    marginTop: 8,
    background: "linear-gradient(135deg, #403301 0%, #856A00 100%)",
    color: "#EFBF04",
    border: "none",
    borderRadius: 10,
    fontSize: 15,
    fontWeight: 800,
    cursor: "pointer",
    transition: "opacity 0.2s, transform 0.15s",
    letterSpacing: "0.04em",
  },
  error: {
    backgroundColor: "#FEE2E2",
    color: "#991B1B",
    padding: "10px 14px",
    borderRadius: 8,
    fontSize: 13,
    marginBottom: 16,
    textAlign: "left",
    border: "1px solid #FECACA",
  },
  spinner: {
    display: "inline-block",
    width: 14,
    height: 14,
    border: "2px solid rgba(239,191,4,0.3)",
    borderTopColor: "#EFBF04",
    borderRadius: "50%",
    animation: "spin 0.7s linear infinite",
  },
  footer: {
    marginTop: 28,
    fontSize: 11,
    color: "#C2B067",
  },
  footerLink: {
    color: "#856A00",
    fontWeight: 700,
    textDecoration: "none",
  },
};
'''

with open("/home/ubuntu/fxj-suits/src/pages/Login.tsx", "w", encoding="utf-8") as f:
    f.write(content)
print("Login.tsx written successfully")
