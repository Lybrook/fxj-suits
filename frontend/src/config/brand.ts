export const BRAND = {
  product: "FXJ Suits",
  descriptor: "Legal operations workspace",
  poweredBy: "Fikia × Jenga Tech",
  poweredByUrl: "https://www.fikiaxjenga.co.ke/",
  location: "Kenya",
  email: "omoshlybrook@gmail.com",
  phone: "+254 748 344 514",
  whatsappUrl: "https://wa.me/254748344514",
  demoEmail: "admin@fxjsuits.co.ke",
  demoPassword: "password123",
} as const;

export const FXJ_COLORS = {
  ink: "#17372C",
  forest: "#27664D",
  sage: "#8AA79B",
  gold: "#D4B65D",
  ivory: "#F7F6F1",
  white: "#FFFFFF",
} as const;

export function formatKes(value: number | null | undefined, options?: Intl.NumberFormatOptions) {
  return `KSh ${Math.round(value || 0).toLocaleString("en-KE", options)}`;
}

export function formatKesCompact(value: number | null | undefined) {
  return new Intl.NumberFormat("en-KE", {
    style: "currency",
    currency: "KES",
    maximumFractionDigits: 0,
    notation: "compact",
  }).format(value || 0);
}
