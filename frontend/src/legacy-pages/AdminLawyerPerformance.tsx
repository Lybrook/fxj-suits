import { useAppContext } from "../context/AppContext";
import { calculateLawyerMetrics } from "../utils/lawyerMetrics";

export default function AdminLawyerPerformance() {
  const { lawyers, transactions, courtCases, letters } = useAppContext();

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Lawyer Performance</h1>
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {lawyers.map((lawyer) => {
          const metrics = calculateLawyerMetrics(lawyer, transactions, courtCases, letters);
          return (
            <div key={lawyer.id} className="bg-white rounded-lg shadow p-5 border">
              <h2 className="font-semibold text-lg">{lawyer.name}</h2>
              <p className="text-sm text-gray-500 mb-3">{lawyer.email}</p>
              <div className="text-sm space-y-1">
                <p><b>Transactions:</b> {metrics.workload.transactions}</p>
                <p><b>Cases:</b> {metrics.workload.cases}</p>
                <p><b>Letters:</b> {metrics.workload.letters}</p>
                <p><b>Notes Added:</b> {metrics.productivity.notes}</p>
                <p><b>Completed Cases:</b> {metrics.productivity.completedCases}</p>
              </div>
              <hr className="my-3" />
              <div className="text-sm">
                <p><b>Billed:</b> KSh {metrics.finance.billed.toLocaleString()}</p>
                <p><b>Paid:</b> KSh {metrics.finance.paid.toLocaleString()}</p>
                <p><b>Balance:</b> KSh {metrics.finance.balance.toLocaleString()}</p>
                <p className="font-semibold">Collection Rate: {metrics.finance.collectionRate}%</p>
              </div>
              <div className="mt-3 text-xs text-gray-600">Productivity Score: {metrics.productivity.score}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
