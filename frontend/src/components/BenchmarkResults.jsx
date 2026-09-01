import React from "react";

function BenchmarkResults({ data }) {
  if (!data) {
    return (
      <div className="benchmark-empty">
        <div className="benchmark-empty-icon">⚡</div>

        <strong>No benchmark results yet</strong>

        <span>
          Configure your experiment and run the benchmark
          to see performance metrics here.
        </span>
      </div>
    );
  }

  // ---------------------------------------
  // API RESPONSE
  // ---------------------------------------

  const results = data.results || [];

  const numpy =
    results.find(
      (item) => item.algorithm?.toLowerCase() === "numpy"
    ) || {};

  const faiss =
    results.find(
      (item) => item.algorithm?.toLowerCase() === "faiss"
    ) || {};

  // ---------------------------------------
  // METRICS
  // ---------------------------------------

  const numpyLatency = Number(
    numpy.average_latency_ms || 0
  );

  const faissLatency = Number(
    faiss.average_latency_ms || 0
  );

  const numpyMin = Number(
    numpy.min_latency_ms || 0
  );

  const faissMin = Number(
    faiss.min_latency_ms || 0
  );

  const numpyMax = Number(
    numpy.max_latency_ms || 0
  );

  const faissMax = Number(
    faiss.max_latency_ms || 0
  );

  const numpyQps = Number(
    numpy.queries_per_second || 0
  );

  const faissQps = Number(
    faiss.queries_per_second || 0
  );

  const speedup = Number(
    data.speedup || 0
  );

  // ---------------------------------------
  // BAR CALCULATION
  // ---------------------------------------

  const maxLatency = Math.max(
    numpyLatency,
    faissLatency,
    1
  );

  const numpyWidth =
    (numpyLatency / maxLatency) * 100;

  const faissWidth =
    (faissLatency / maxLatency) * 100;

  return (
    <div className="benchmark-dashboard">

      {/* =====================================
          TOP METRICS
      ===================================== */}

      <div className="benchmark-metrics">

        {/* NUMPY */}

        <div className="benchmark-metric">

          <div className="metric-top">

            <span className="metric-icon numpy-icon">
              ◌
            </span>

            <span className="metric-label">
              NUMPY
            </span>

          </div>

          <div className="metric-value">
            {numpyLatency.toFixed(4)}
            <small> ms</small>
          </div>

          <div className="metric-description">
            Average query latency
          </div>

        </div>


        {/* FAISS */}

        <div className="benchmark-metric">

          <div className="metric-top">

            <span className="metric-icon faiss-icon">
              ✦
            </span>

            <span className="metric-label">
              FAISS
            </span>

          </div>

          <div className="metric-value">
            {faissLatency.toFixed(4)}
            <small> ms</small>
          </div>

          <div className="metric-description">
            Average query latency
          </div>

        </div>


        {/* SPEEDUP */}

        <div className="benchmark-metric">

          <div className="metric-top">

            <span className="metric-icon speedup-icon">
              ⚡
            </span>

            <span className="metric-label">
              SPEEDUP
            </span>

          </div>

          <div className="metric-value gradient-number">
            {speedup.toFixed(4)}
            <small>×</small>
          </div>

          <div className="metric-description">
            Compared with NumPy
          </div>

        </div>


        {/* QPS */}

        <div className="benchmark-metric">

          <div className="metric-top">

            <span className="metric-icon qps-icon">
              ↗
            </span>

            <span className="metric-label">
              FAISS QPS
            </span>

          </div>

          <div className="metric-value">
            {faissQps.toFixed(2)}
          </div>

          <div className="metric-description">
            Queries per second
          </div>

        </div>

      </div>


      {/* =====================================
          DIVIDER
      ===================================== */}

      <div className="benchmark-divider" />


      {/* =====================================
          LATENCY COMPARISON
      ===================================== */}

      <div className="latency-section">

        <div className="latency-header">

          <div>

            <h3>
              Latency comparison
            </h3>

            <p>
              Lower latency means faster retrieval.
            </p>

          </div>

          <div className="chart-unit">
            milliseconds
          </div>

        </div>


        <div className="latency-chart">

          {/* NUMPY */}

          <div className="latency-row">

            <div className="latency-label">

              <span className="legend-dot numpy-dot" />

              <strong>
                NumPy
              </strong>

            </div>


            <div className="latency-track">

              <div
                className="latency-bar numpy-bar"
                style={{
                  width: `${numpyWidth}%`,
                }}
              />

            </div>


            <div className="latency-number">

              {numpyLatency.toFixed(4)}

              <span>
                {" "}ms
              </span>

            </div>

          </div>


          {/* FAISS */}

          <div className="latency-row">

            <div className="latency-label">

              <span className="legend-dot faiss-dot" />

              <strong>
                FAISS
              </strong>

            </div>


            <div className="latency-track">

              <div
                className="latency-bar faiss-bar"
                style={{
                  width: `${faissWidth}%`,
                }}
              />

            </div>


            <div className="latency-number">

              {faissLatency.toFixed(4)}

              <span>
                {" "}ms
              </span>

            </div>

          </div>

        </div>

      </div>


      {/* =====================================
          DETAILS TABLE
      ===================================== */}

      <div className="benchmark-table-wrapper">

        <table className="benchmark-table">

          <thead>

            <tr>

              <th>
                Algorithm
              </th>

              <th>
                Average
              </th>

              <th>
                Minimum
              </th>

              <th>
                Maximum
              </th>

              <th>
                QPS
              </th>

            </tr>

          </thead>


          <tbody>

            {/* NUMPY */}

            <tr>

              <td>

                <div className="algorithm-name">

                  <span className="legend-dot numpy-dot" />

                  NUMPY

                </div>

              </td>

              <td>
                {numpyLatency.toFixed(4)} ms
              </td>

              <td>
                {numpyMin.toFixed(4)} ms
              </td>

              <td>
                {numpyMax.toFixed(4)} ms
              </td>

              <td>
                {numpyQps.toFixed(4)}
              </td>

            </tr>


            {/* FAISS */}

            <tr>

              <td>

                <div className="algorithm-name">

                  <span className="legend-dot faiss-dot" />

                  FAISS

                </div>

              </td>

              <td>
                {faissLatency.toFixed(4)} ms
              </td>

              <td>
                {faissMin.toFixed(4)} ms
              </td>

              <td>
                {faissMax.toFixed(4)} ms
              </td>

              <td>
                {faissQps.toFixed(4)}
              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </div>
  );
}

export default BenchmarkResults;