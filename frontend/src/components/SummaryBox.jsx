function SummaryBox({ summary }) {
  if (!summary) return null;

  return (
    <div className="summary-box">
      <h3>Summary</h3>
      <p>{summary}</p>
    </div>
  );
}

export default SummaryBox;