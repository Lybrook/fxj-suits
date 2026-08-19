type Props = {
  label: string;
};

export default function AutoLabelBadge({ label }: Props) {
  const base =
    "text-xs font-semibold px-2 py-1 rounded border mr-2 inline-block";

  const styles: Record<string, string> = {
    PAID: "bg-green-50 text-green-700 border-green-300",
    UNPAID: "bg-red-50 text-red-700 border-red-300",
    OVERDUE: "bg-orange-50 text-orange-700 border-orange-300",
    UPCOMING: "bg-[#FBFAF6] text-[#27664D] border-blue-300",
    "NO UPDATES": "bg-gray-50 text-gray-700 border-gray-300",
  };

  return (
    <span className={`${base} ${styles[label] || ""}`}>
      {label}
    </span>
  );
}
