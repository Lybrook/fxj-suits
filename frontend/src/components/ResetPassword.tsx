import { useState, type FormEvent } from "react";
import { ArrowLeft, ArrowRight, LockKeyhole } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { supabase } from "../lib/supabaseClient";
import { BRAND } from "../config/brand";

export default function ResetPassword() {
  const [newPassword, setNewPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleUpdatePassword = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    const authClient = supabase.auth as typeof supabase.auth & {
      updateUser: (payload: { password: string }) => Promise<{ error: { message: string } | null }>;
    };
    const { error } = await authClient.updateUser({ password: newPassword });
    if (error) {
      window.alert(error.message);
    } else {
      window.alert("Password updated successfully. You can now sign in.");
      navigate("/");
    }
    setLoading(false);
  };

  return (
    <main className="fxj-login-page" style={{ gridTemplateColumns: "minmax(0, 0.8fr) minmax(430px, 1.2fr)" }}>
      <section className="fxj-login-visual" aria-labelledby="reset-hero-title">
        <a href={BRAND.poweredByUrl} target="_blank" rel="noopener noreferrer" className="fxj-login-visual__brand">
          <span className="fxj-brand-mark" aria-hidden="true">FXJ</span>
          <span className="fxj-login-visual__brand-copy">
            <strong>{BRAND.product}</strong>
            <small>Powered by {BRAND.poweredBy}</small>
          </span>
        </a>
        <div className="fxj-login-visual__content">
          <p className="fxj-login-visual__eyebrow">Secure access · Kenya</p>
          <h1 id="reset-hero-title">Keep your workspace <em>protected.</em></h1>
          <p className="fxj-login-visual__copy">Your firm’s records deserve a considered, private place to work. Set a new password and return to the matters that need you.</p>
        </div>
        <div className="fxj-login-visual__footer"><LockKeyhole size={13} aria-hidden="true" /> Private to your firm</div>
      </section>

      <section className="fxj-login-form-panel" aria-label="Set a new password">
        <div className="fxj-login-card">
          <button type="button" className="fxj-reset-back" onClick={() => navigate("/")}><ArrowLeft size={15} /> Back to sign in</button>
          <p className="fxj-login-card__eyebrow">Account security</p>
          <h2>Set a new password.</h2>
          <p className="fxj-login-card__intro">Choose a secure password for your {BRAND.product} workspace.</p>
          <div className="fxj-login-divider" />
          <form onSubmit={handleUpdatePassword}>
            <div className="fxj-login-field">
              <label htmlFor="new-password">New password</label>
              <input
                id="new-password"
                type="password"
                placeholder="Enter a secure password"
                className="fxj-login-input"
                value={newPassword}
                required
                minLength={8}
                autoComplete="new-password"
                onChange={(event) => setNewPassword(event.target.value)}
              />
            </div>
            <button type="submit" disabled={loading} className="fxj-login-submit">
              {loading ? "Updating…" : <>Update password <ArrowRight size={16} /></>}
            </button>
          </form>
          <p className="fxj-login-card__footer">Powered by <a href={BRAND.poweredByUrl} target="_blank" rel="noopener noreferrer">{BRAND.poweredBy}</a>.</p>
        </div>
      </section>
    </main>
  );
}
