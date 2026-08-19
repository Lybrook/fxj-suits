import { useEffect, useState, type FormEvent } from "react";
import { ArrowRight, Eye, EyeOff, LockKeyhole, MapPin, ShieldCheck, Sparkles } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useAppContext } from "../context/AppContext";
import { BRAND } from "../config/brand";

const audienceWords = ["practice teams", "legal teams", "Kenyan advocates"];

export default function Login() {
  const { setCurrentUser } = useAppContext();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [audienceIndex, setAudienceIndex] = useState(0);

  useEffect(() => {
    document.title = `${BRAND.product} | Kenyan legal operations`;
    const timer = window.setInterval(() => {
      setAudienceIndex((index) => (index + 1) % audienceWords.length);
    }, 4200);
    return () => window.clearInterval(timer);
  }, []);

  const handleRequestReset = () => navigate("/reset-password");

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");
    setLoading(true);
    try {
      const { supabase } = await import("../lib/supabaseClient");
      const { data: authData, error: authError } = await supabase.auth.signInWithPassword({ email, password });
      if (authError) throw authError;
      if (!authData) throw new Error("Unable to start a session.");
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
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Unable to sign in. Please check your credentials and try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="fxj-login-page">
      <section className="fxj-login-visual" aria-labelledby="login-hero-title">
        <a href={BRAND.poweredByUrl} target="_blank" rel="noopener noreferrer" className="fxj-login-visual__brand">
          <span className="fxj-brand-mark" aria-hidden="true">FXJ</span>
          <span className="fxj-login-visual__brand-copy">
            <strong>{BRAND.product}</strong>
            <small>Powered by {BRAND.poweredBy.replace(" × ", " × ")}</small>
          </span>
        </a>

        <div className="fxj-login-visual__content">
          <p className="fxj-login-visual__eyebrow">Digital operations partner · Kenya</p>
          <h1 id="login-hero-title">
            Run your practice with <em>clarity.</em>
          </h1>
          <p className="fxj-login-visual__copy">
            A calm, connected workspace for matters, clients, court activity, land records, finance, and the work that keeps a Kenyan practice moving.
          </p>

          <div className="fxj-login-proof-grid" aria-label="Workspace benefits">
            <div className="fxj-login-proof"><strong>One view</strong><span>Every matter</span></div>
            <div className="fxj-login-proof"><strong>KSh-ready</strong><span>Local workflows</span></div>
            <div className="fxj-login-proof"><strong>Built here</strong><span>For Kenya</span></div>
          </div>
        </div>

        <div className="fxj-login-visual__footer"><MapPin size={13} aria-hidden="true" /> Kitale · Nairobi · Kenya</div>

        <div className="fxj-login-float-card fxj-login-float-card--top" aria-hidden="true">
          <span className="fxj-login-float-card__icon"><Sparkles size={15} /></span>
          <span><strong>Made for {audienceWords[audienceIndex]}</strong><span>Simple, structured, ready to grow</span></span>
        </div>
        <div className="fxj-login-float-card fxj-login-float-card--bottom" aria-hidden="true">
          <span className="fxj-login-float-card__icon"><ShieldCheck size={15} /></span>
          <span><strong>Secure by design</strong><span>Roles, records, and audit trails</span></span>
        </div>
      </section>

      <section className="fxj-login-form-panel" aria-label="Sign in to FXJ Suits">
        <div className="fxj-login-card">
          <p className="fxj-login-card__eyebrow">Welcome back</p>
          <h2>Sign in.</h2>
          <p className="fxj-login-card__intro">Access your firm workspace and keep today’s legal work in motion.</p>
          <div className="fxj-login-divider" />

          {error && <div className="fxj-login-error" role="alert">{error}</div>}

          <form onSubmit={handleSubmit} noValidate>
            <div className="fxj-login-field">
              <label htmlFor="email">Work email</label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                placeholder="advocate@yourfirm.co.ke"
                required
                autoComplete="email"
                className="fxj-login-input"
              />
            </div>

            <div className="fxj-login-field">
              <div className="fxj-login-field__label-row">
                <label htmlFor="password">Password</label>
                <button type="button" onClick={handleRequestReset}>Forgot password?</button>
              </div>
              <div className="fxj-login-input-wrap">
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  placeholder="Enter your password"
                  required
                  autoComplete="current-password"
                  className="fxj-login-input"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((visible) => !visible)}
                  className="fxj-login-input__toggle"
                  aria-label={showPassword ? "Hide password" : "Show password"}
                >
                  {showPassword ? <EyeOff size={17} /> : <Eye size={17} />}
                </button>
              </div>
            </div>

            <button type="submit" className="fxj-login-submit" disabled={loading}>
              {loading ? <><span className="fxj-button-spinner" aria-hidden="true" /> Signing in…</> : <>Open workspace <ArrowRight size={16} /></>}
            </button>
          </form>

          <div className="fxj-login-trust"><LockKeyhole size={13} aria-hidden="true" /> Your workspace is private to your firm.</div>
          <p className="fxj-login-card__footer">
            © {new Date().getFullYear()} {BRAND.product}. Powered by{" "}
            <a href={BRAND.poweredByUrl} target="_blank" rel="noopener noreferrer">{BRAND.poweredBy}</a>.
          </p>
        </div>
      </section>
    </main>
  );
}
