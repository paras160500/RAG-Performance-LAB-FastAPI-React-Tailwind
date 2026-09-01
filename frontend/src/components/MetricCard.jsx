function MetricCard({
  title,
  value,
  description,
}) {
  return (
    <div className="metric-card">
      <div className="metric-title">
        {title}
      </div>

      <div className="metric-value">
        {value}
      </div>

      <div className="metric-description">
        {description}
      </div>
    </div>
  );
}


export default MetricCard;