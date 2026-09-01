import {
  useEffect,
  useState,
} from "react";

import {
  healthCheck,
  getDataset,
  searchVectors,
  runBenchmark,
  getBenchmarkHistory,
} from "../services/api";

import {
  generateQueryVector,
} from "../utils/vectorGenerator";

import RetrievalResults from "../components/RetrievalResults";
import BenchmarkResults from "../components/BenchmarkResults";


const DATASET_ID =
  import.meta.env.VITE_DATASET_ID ||
  "";

const DIMENSION = 1536;


function Dashboard() {

  const [backend, setBackend] =
    useState("checking");

  const [dataset, setDataset] =
    useState(null);

  const [seed, setSeed] =
    useState(123);

  const [topK, setTopK] =
    useState(5);

  const [iterations, setIterations] =
    useState(10);

  const [algorithm, setAlgorithm] =
    useState("faiss");

  const [queryVector, setQueryVector] =
    useState([]);

  const [searchResult, setSearchResult] =
    useState(null);

  const [benchmarkResult, setBenchmarkResult] =
    useState(null);

  const [history, setHistory] =
    useState([]);

  const [loading, setLoading] =
    useState(false);

  const [activeAction, setActiveAction] =
    useState("");

  const [error, setError] =
    useState("");


  useEffect(() => {
    checkBackend();
    loadDataset();
    createVector();
    loadHistory();
  }, []);


  async function checkBackend() {
    try {
      await healthCheck();
      setBackend("online");
    } catch {
      setBackend("offline");
    }
  }


  async function loadDataset() {

    if (!DATASET_ID) return;

    try {

      const data =
        await getDataset(DATASET_ID);

      setDataset(data);

    } catch (err) {

      console.error(err);

    }
  }


  async function loadHistory() {

    try {

      const data =
        await getBenchmarkHistory();

      setHistory(
        Array.isArray(data)
          ? data
          : []
      );

    } catch (err) {

      console.error(err);

    }
  }


  function createVector() {

    const vector =
      generateQueryVector(
        DIMENSION,
        seed
      );

    setQueryVector(vector);
    setSearchResult(null);
    setBenchmarkResult(null);
    setError("");
  }


  async function handleSearch() {

    if (!queryVector.length) return;

    try {

      setLoading(true);
      setActiveAction("search");
      setError("");

      const data =
        await searchVectors({
          query_vector:
            queryVector,

          algorithm,

          top_k:
            Number(topK),
        });

      setSearchResult(data);

    } catch (err) {

      setError(err.message);

    } finally {

      setLoading(false);
      setActiveAction("");

    }
  }


  async function handleBenchmark() {

    if (!queryVector.length) return;

    try {

      setLoading(true);
      setActiveAction("benchmark");
      setError("");

      const data =
        await runBenchmark({

          query_vector:
            queryVector,

          top_k:
            Number(topK),

          iterations:
            Number(iterations),

          seed:
            Number(seed),

        });

      setBenchmarkResult(data);

      await loadHistory();

    } catch (err) {

      setError(err.message);

    } finally {

      setLoading(false);
      setActiveAction("");

    }
  }


  const vectorCount =
    dataset?.vector_count ?? 10000;

  const dimension =
    dataset?.dimension ?? DIMENSION;

  const speedup =
    benchmarkResult?.speedup;


  return (
    <main className="dashboard">

      <div className="ambient ambient-one" />
      <div className="ambient ambient-two" />
      <div className="ambient ambient-three" />


      {/* NAVBAR */}

      <nav className="navbar">

        <div className="brand">

          <div className="brand-mark">
            <span />
            <span />
            <span />
          </div>

          <div>
            <div className="brand-name">
              VectorLab
            </div>

            <div className="brand-subtitle">
              Retrieval Performance
            </div>
          </div>

        </div>


        <div className="nav-status">

          <span
            className={`status-dot ${backend}`}
          />

          <span>
            API
          </span>

          <strong>
            {backend === "online"
              ? "Operational"
              : backend === "offline"
                ? "Offline"
                : "Checking"}
          </strong>

        </div>

      </nav>


      {/* HERO */}

      <section className="hero">

        <div className="hero-copy">

          <div className="hero-badge">
            <span className="pulse" />
            RAG PERFORMANCE LAB
          </div>


          <h1>

            Measure your

            <span className="gradient-text">
              {" "}vector search.
            </span>

          </h1>


          <p>

            Benchmark exact NumPy retrieval
            against FAISS and understand
            the performance difference
            behind modern RAG systems.

          </p>


          <div className="hero-actions">

            <button
              className="gradient-button"
              onClick={
                handleBenchmark
              }
              disabled={
                loading ||
                backend !== "online"
              }
            >

              {activeAction === "benchmark"
                ? "Running benchmark..."
                : "Run benchmark"}

              <span>
                →
              </span>

            </button>


            <button
              className="ghost-button"
              onClick={
                createVector
              }
            >
              Generate new query
            </button>

          </div>

        </div>


        {/* HERO VISUAL */}

        <div className="hero-visual">

          <div className="orb orb-one" />
          <div className="orb orb-two" />

          <div className="floating-card card-top">

            <span>
              SEARCH ENGINE
            </span>

            <strong>
              FAISS
            </strong>

            <div className="mini-bars">
              <i />
              <i />
              <i />
              <i />
              <i />
            </div>

          </div>


          <div className="hero-center-card">

            <div className="center-icon">
              ⚡
            </div>

            <div className="center-number">
              {speedup
                ? `${speedup}×`
                : "—"}
            </div>

            <div className="center-label">
              FAISS SPEEDUP
            </div>

            <div className="center-line">
              <span />
            </div>

          </div>


          <div className="floating-card card-bottom">

            <div>
              <span>
                VECTOR SPACE
              </span>

              <strong>
                {dimension}D
              </strong>
            </div>

            <div className="vector-dots">
              {Array.from({
                length: 18,
              }).map(
                (_, index) => (
                  <i key={index} />
                )
              )}
            </div>

          </div>

        </div>

      </section>


      {/* DATASET STRIP */}

      <section className="dataset-strip">

        <div className="dataset-item">

          <span className="dataset-icon">
            ◈
          </span>

          <div>
            <small>
              DATASET
            </small>

            <strong>
              {vectorCount.toLocaleString()}
              {" "}vectors
            </strong>
          </div>

        </div>


        <div className="dataset-divider" />


        <div className="dataset-item">

          <span className="dataset-icon">
            ⌁
          </span>

          <div>
            <small>
              DIMENSION
            </small>

            <strong>
              {dimension}D embeddings
            </strong>
          </div>

        </div>


        <div className="dataset-divider" />


        <div className="dataset-item">

          <span className="dataset-icon">
            ◉
          </span>

          <div>
            <small>
              INDEX
            </small>

            <strong>
              FAISS IndexFlatL2
            </strong>
          </div>

        </div>


        <div className="dataset-divider" />


        <div className="dataset-item">

          <span className="dataset-icon">
            ☁
          </span>

          <div>
            <small>
              STORAGE
            </small>

            <strong>
              Supabase
            </strong>
          </div>

        </div>

      </section>


      {/* EXPERIMENT */}

      <section className="section">

        <div className="section-heading">

          <div>

            <span className="section-number">
              01
            </span>

            <div>

              <h2>
                Configure experiment
              </h2>

              <p>
                Create a reproducible
                vector retrieval workload.
              </p>

            </div>

          </div>

        </div>


        <div className="experiment-card">

          <div className="control-group">

            <label>
              Query seed
            </label>

            <input
              type="number"
              value={seed}
              onChange={(event) =>
                setSeed(
                  Number(
                    event.target.value
                  )
                )
              }
            />

          </div>


          <div className="control-group">

            <label>
              Algorithm
            </label>

            <select
              value={algorithm}
              onChange={(event) =>
                setAlgorithm(
                  event.target.value
                )
              }
            >

              <option value="faiss">
                FAISS
              </option>

              <option value="numpy">
                NumPy
              </option>

            </select>

          </div>


          <div className="control-group">

            <label>
              Top K
            </label>

            <select
              value={topK}
              onChange={(event) =>
                setTopK(
                  Number(
                    event.target.value
                  )
                )
              }
            >

              <option value={1}>
                1
              </option>

              <option value={5}>
                5
              </option>

              <option value={10}>
                10
              </option>

              <option value={20}>
                20
              </option>

            </select>

          </div>


          <div className="control-group">

            <label>
              Iterations
            </label>

            <select
              value={iterations}
              onChange={(event) =>
                setIterations(
                  Number(
                    event.target.value
                  )
                )
              }
            >

              <option value={5}>
                5
              </option>

              <option value={10}>
                10
              </option>

              <option value={25}>
                25
              </option>

              <option value={50}>
                50
              </option>

              <option value={100}>
                100
              </option>

            </select>

          </div>


          <div className="vector-preview">

            <div className="vector-preview-icon">
              ✦
            </div>

            <div>

              <span>
                QUERY VECTOR
              </span>

              <strong>
                {queryVector.length}
                {" "}dimensions
              </strong>

            </div>


            <button
              onClick={
                createVector
              }
            >
              Regenerate
            </button>

          </div>


          <div className="experiment-actions">

            <button
              className="search-button"
              onClick={
                handleSearch
              }
              disabled={
                loading ||
                backend !==
                  "online"
              }
            >

              {activeAction === "search"
                ? "Searching..."
                : "Run vector search"}

              <span>
                →
              </span>

            </button>


            <button
              className="benchmark-large-button"
              onClick={
                handleBenchmark
              }
              disabled={
                loading ||
                backend !==
                  "online"
              }
            >

              {activeAction === "benchmark"
                ? "Benchmarking..."
                : "Run full benchmark"}

              <span>
                ⚡
              </span>

            </button>

          </div>


          {error && (
            <div className="error-message">
              <strong>
                Something went wrong
              </strong>

              <span>
                {error}
              </span>
            </div>
          )}

        </div>

      </section>


      {/* RETRIEVAL */}

      <section className="section">

        <div className="section-heading">

          <div>

            <span className="section-number">
              02
            </span>

            <div>

              <h2>
                Nearest vectors
              </h2>

              <p>
                Inspect the top-K vectors
                returned by the index.
              </p>

            </div>

          </div>

        </div>


        <div className="results-card">

          <RetrievalResults
            data={searchResult}
          />

        </div>

      </section>


      {/* BENCHMARK */}

      <section className="section">

        <div className="section-heading">

          <div>

            <span className="section-number">
              03
            </span>

            <div>

              <h2>
                Performance analysis
              </h2>

              <p>
                See how FAISS performs
                against exact NumPy search.
              </p>

            </div>

          </div>


          {speedup && (
            <div className="speedup-pill">

              <span>
                ⚡
              </span>

              FAISS is{" "}
              <strong>
                {speedup}× faster
              </strong>

            </div>
          )}

        </div>


        <div className="results-card benchmark-card">

          <BenchmarkResults
            data={benchmarkResult}
          />

        </div>

      </section>


      {/* HISTORY */}

      <section className="section history-section">

        <div className="section-heading">

          <div>

            <span className="section-number">
              04
            </span>

            <div>

              <h2>
                Experiment history
              </h2>

              <p>
                Every benchmark is persisted
                to your Supabase database.
              </p>

            </div>

          </div>

        </div>


        <div className="history-card">

          {history.length === 0 ? (

            <div className="history-empty">

              <div>
                ◌
              </div>

              <strong>
                No experiments yet
              </strong>

              <span>
                Run your first benchmark
                to start building history.
              </span>

            </div>

          ) : (

            <div className="history-list">

              {history
                .slice(0, 8)
                .map((item) => (

                  <div
                    className="history-row"
                    key={item.id}
                  >

                    <div className="history-engine">

                      <span
                        className={
                          item.algorithm ===
                          "faiss"
                            ? "engine-dot faiss"
                            : "engine-dot numpy"
                        }
                      />

                      <strong>
                        {
                          item.algorithm.toUpperCase()
                        }
                      </strong>

                    </div>


                    <div>

                      <span>
                        LATENCY
                      </span>

                      <strong>
                        {
                          item.average_latency_ms
                        }{" "}
                        ms
                      </strong>

                    </div>


                    <div>

                      <span>
                        QPS
                      </span>

                      <strong>
                        {
                          item.queries_per_second
                        }
                      </strong>

                    </div>


                    <div>

                      <span>
                        SPEEDUP
                      </span>

                      <strong>
                        {item.speedup
                          ? `${item.speedup}×`
                          : "—"}
                      </strong>

                    </div>


                    <div className="history-date">

                      {new Date(
                        item.created_at
                      ).toLocaleDateString()}

                    </div>

                  </div>

                ))}

            </div>

          )}

        </div>

      </section>


      <footer className="footer">

        <div className="footer-brand">
          VectorLab
        </div>

        <span>
          Built with React · FastAPI ·
          FAISS · NumPy · Supabase
        </span>

      </footer>

    </main>
  );
}


export default Dashboard;