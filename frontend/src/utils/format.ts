export function formatKSh(amount: number): string {
  return new Intl.NumberFormat("en-KE", {
    style: "currency",
    currency: "KSh",
    minimumFractionDigits: 0,
  }).format(amount);
}
