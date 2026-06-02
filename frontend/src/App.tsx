import { FormEvent, useState } from "react";

import { type AnalyzePasswordResponse, analyzePassword } from "./api";

export function App() {
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalyzePasswordResponse | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const analysis = await analyzePassword(password);
      setResult(analysis);
    } catch {
      setResult(null);
      setError("No se pudo analizar la contrasena. Intenta de nuevo.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page-shell">
      <section className="hero-card">
        <p className="eyebrow">PassGuard CI</p>
        <h1>Analizador academico de contrasenas</h1>
        <p className="hero-copy">
          Evalua una contrasena con reglas simples y resultados explicables para
          demostrar calidad, pruebas y CI/CD.
        </p>

        <form className="analysis-form" onSubmit={handleSubmit}>
          <label className="field-label" htmlFor="password-input">
            Contrasena
          </label>
          <div className="password-row">
            <input
              id="password-input"
              name="password"
              type={showPassword ? "text" : "password"}
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="Ingresa una contrasena"
            />
            <button
              className="secondary-button"
              type="button"
              onClick={() => setShowPassword((current) => !current)}
              aria-label={showPassword ? "Ocultar contrasena" : "Mostrar contrasena"}
            >
              {showPassword ? "Ocultar" : "Mostrar"}
            </button>
          </div>
          <button className="primary-button" type="submit" disabled={loading}>
            {loading ? "Analizando..." : "Analizar"}
          </button>
        </form>

        {error ? <p className="error-banner">{error}</p> : null}
      </section>

      <section className="results-card" aria-live="polite">
        <h2>Resultado</h2>
        {!result ? (
          <p className="placeholder-copy">
            Ejecuta un analisis para ver score, nivel, tokens, advertencias y reglas.
          </p>
        ) : (
          <>
            <div className="summary-grid">
              <article>
                <span>Score</span>
                <strong>{result.score}</strong>
              </article>
              <article>
                <span>Nivel</span>
                <strong className={`level-badge level-${result.level}`}>{result.level}</strong>
              </article>
            </div>

            <ResultList
              title="Tokens detectados"
              items={result.tokens.map((token) => `${token.type}: ${token.value}`)}
            />
            <ResultList
              title="Advertencias"
              items={result.warnings.map((warning) => `${warning.code}: ${warning.message}`)}
              emptyLabel="Sin advertencias"
            />
            <ResultList title="Reglas cumplidas" items={result.passed_rules} />
            <ResultList title="Reglas incumplidas" items={result.failed_rules} />
          </>
        )}
      </section>
    </main>
  );
}

type ResultListProps = {
  title: string;
  items: string[];
  emptyLabel?: string;
};

function ResultList({ title, items, emptyLabel = "Sin datos" }: ResultListProps) {
  return (
    <section className="result-block">
      <h3>{title}</h3>
      {items.length === 0 ? (
        <p>{emptyLabel}</p>
      ) : (
        <ul>
          {items.map((item) => (
            <li key={`${title}-${item}`}>{item}</li>
          ))}
        </ul>
      )}
    </section>
  );
}
