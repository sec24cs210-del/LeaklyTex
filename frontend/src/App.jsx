import { useState } from 'react'
import './App.css'

const stats = [
  { label: 'Pipes Monitored', value: '128', note: 'Registered assets', icon: '◉' },
  { label: 'Healthy Pipes', value: '94', note: 'Green condition', icon: '✓' },
  { label: 'Needs Inspection', value: '23', note: 'Amber condition', icon: '!' },
  { label: 'Critical Pipes', value: '11', note: 'Red condition', icon: '⚠' },
]

const pipes = [
  { id: 'P-001', location: 'North Block', material: 'DI', age: '8 years', condition: 'Green' },
  { id: 'P-002', location: 'Basement Level 1', material: 'CI', age: '18 years', condition: 'Amber' },
  { id: 'P-003', location: 'Treatment Plant Line', material: 'DI', age: '24 years', condition: 'Red' },
  { id: 'P-004', location: 'East Wing', material: 'HDPE', age: '5 years', condition: 'Green' },
]

function App() {
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [predictionError, setPredictionError] = useState('')
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">L</div>
          <div>
            <h2>LeaklyTex</h2>
            <span>PIPELINE INTELLIGENCE</span>
          </div>
        </div>

        <p className="nav-heading">WORKSPACE</p>
        <div className="nav-item active"><span>▦</span> Dashboard</div>
        <div className="nav-item"><span>◎</span> Pipe assets</div>
        <div className="nav-item"><span>⌁</span> Predictions</div>
        <div className="nav-item"><span>◷</span> Maintenance</div>

        <div className="sidebar-bottom">
          <div className="status-dot" />
          <div>
            <strong>System overview</strong>
            <p>AI-assisted monitoring</p>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <p className="eyebrow">PIPELINE MANAGEMENT / OVERVIEW</p>
            <h1>Dashboard</h1>
          </div>
          <div className="topbar-right">
            <span className="live-indicator"><i /> Prototype mode</span>
            <div className="avatar">LT</div>
          </div>
        </header>

        <section className="welcome">
          <div>
            <p className="eyebrow light">LEAKLYTEX MONITORING SYSTEM</p>
            <h2>Know your pipes.<br />Act before failure.</h2>
            <p className="welcome-copy">
              An AI-assisted view of pipeline condition and maintenance priorities.
            </p>
          </div>
          <div className="welcome-art" aria-hidden="true">
            <div className="orbit orbit-one" />
            <div className="orbit orbit-two" />
            <div className="water-drop">⌁</div>
            <span className="art-label">PIPE HEALTH</span>
          </div>
        </section>

        <section className="section-heading">
          <div>
            <h2>Asset overview</h2>
            <p>Illustrative dashboard figures for the frontend prototype</p>
          </div>
          <span className="period-label">DEMO DATA</span>
        </section>

        <section className="stats-grid">
          {stats.map((stat, index) => (
            <article className="stat-card" key={stat.label}>
              <div className={`stat-icon icon-${index}`}>{stat.icon}</div>
              <p>{stat.label}</p>
              <div className="stat-value">{stat.value}</div>
              <span className="stat-note">{stat.note}</span>
            </article>
          ))}
        </section>

        <section className="panel prediction-panel">
          <div className="panel-heading">
            <div>
              <h2>Pipe condition prediction</h2>
              <p>Enter pipe details to request an ML prediction</p>
            </div>
          </div>

          <form
            onSubmit={async (event) => {
              event.preventDefault()
              const formData = new FormData(event.currentTarget)

              const payload = {
                region: formData.get('region'),
                diameter_mm: Number(formData.get('diameter_mm')),
                material: formData.get('material'),
                age_years: Number(formData.get('age_years')),
                length_m: Number(formData.get('length_m')),
              }

              setLoading(true)
              setPrediction(null)
              setPredictionError('')

              try {
                const response = await fetch(
                  'http://127.0.0.1:8000/predict/pipe-condition',
                  {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload),
                  }
                )

                const result = await response.json()

                if (!response.ok) {
                  throw new Error(result.detail || 'Prediction failed')
                }

                setPrediction(result)
              } catch (error) {
                setPredictionError(error.message || 'Could not get prediction.')
              } finally {
                setLoading(false)
              }
            }}
          >
            <div className="prediction-fields">
              <label>
                Region
                <input name="region" defaultValue="U_A" required />
              </label>

              <label>
                Pipe diameter (mm)
                <input name="diameter_mm" type="number" min="1" defaultValue="300" required />
              </label>

              <label>
                Material
                <select name="material" defaultValue="DI" required>
                  <option value="DI">Ductile iron (DI)</option>
                  <option value="CI">Cast iron (CI)</option>
                  <option value="HDPE">HDPE</option>
                </select>
              </label>

              <label>
                Pipe age (years)
                <input name="age_years" type="number" min="0" step="0.1" defaultValue="15" required />
              </label>

              <label>
                Pipe length (m)
                <input name="length_m" type="number" min="1" step="0.1" defaultValue="500" required />
              </label>
            </div>

            <button type="submit">Predict pipe condition</button>
          </form>

          {loading && <p className="prediction-status">Analysing pipe details...</p>}

          {predictionError && (
            <div className="prediction-error" role="alert">
              <strong>Prediction failed</strong>
              <p>{predictionError}</p>
              <p>Check that the backend is running and try again.</p>
            </div>
          )}

          {prediction && (
            <div className="prediction-result">
              <div className="result-heading">
                <div>
                  <span className="result-eyebrow">MODEL RESULT</span>
                  <h3>Predicted pipe condition</h3>
                </div>
                <span className={'condition-badge condition-' + String(prediction.predicted_condition).toLowerCase()}>
                  {prediction.predicted_condition}
                </span>
              </div>

              <p className="result-note">
                This model predicts pipe condition; it does not confirm an actual leak.
              </p>

              <h4>Class probabilities</h4>
              <div className="probability-list">
                {Object.entries(prediction.class_probabilities || {}).map(([condition, probability]) => {
                  const percent = Math.max(0, Math.min(100, Number(probability) * 100))
                  return (
                    <div className="probability-row" key={condition}>
                      <div className="probability-label">
                        <span>{condition}</span>
                        <strong>{percent.toFixed(1)}%</strong>
                      </div>
                      <div className="probability-track" role="progressbar"
                        aria-label={condition + ' probability'}
                        aria-valuemin={0} aria-valuemax={100}
                        aria-valuenow={Number(percent.toFixed(1))}>
                        <div className={'probability-fill condition-' + condition.toLowerCase()}
                          style={{ width: percent + '%' }} />
                      </div>
                    </div>
                  )
                })}
              </div>
              <p className="model-version">Model version: {prediction.model_version || 'Not provided'}</p>
            </div>
          )}
        </section>

        <section className="content-grid">
          <article className="panel pipe-panel">
            <div className="panel-heading">
              <div>
                <h2>Pipeline assets</h2>
                <p>Example assets and condition labels</p>
              </div>
              <span className="panel-symbol">↗</span>
            </div>

            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>PIPE ID</th>
                    <th>LOCATION</th>
                    <th>MATERIAL</th>
                    <th>AGE</th>
                    <th>CONDITION</th>
                  </tr>
                </thead>
                <tbody>
                  {pipes.map((pipe) => (
                    <tr key={pipe.id}>
                      <td className="pipe-id">{pipe.id}</td>
                      <td>{pipe.location}</td>
                      <td>{pipe.material}</td>
                      <td>{pipe.age}</td>
                      <td>
                        <span className={`condition condition-${pipe.condition.toLowerCase()}`}>
                          {pipe.condition}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <p className="demo-notice">Sample rows only — not live database records.</p>
          </article>

          <article className="panel priority-panel">
            <div className="panel-heading">
              <div>
                <h2>Priority guide</h2>
                <p>How to interpret condition labels</p>
              </div>
            </div>
            <div className="priority-item">
              <span className="priority-dot green-dot" />
              <div><strong>Green</strong><p>Lower predicted concern</p></div>
            </div>
            <div className="priority-item">
              <span className="priority-dot amber-dot" />
              <div><strong>Amber</strong><p>Review and plan inspection</p></div>
            </div>
            <div className="priority-item">
              <span className="priority-dot red-dot" />
              <div><strong>Red</strong><p>Prioritise assessment</p></div>
            </div>
            <div className="disclaimer">
              <strong>Important</strong>
              <p>Condition predictions do not independently confirm or rule out a leak.</p>
            </div>
          </article>
        </section>

        <footer>
          <span>LeaklyTex · AI-based pipeline condition prototype</span>
          <span>Dashboard preview · Demo data</span>
        </footer>
      </main>
    </div>
  )
}

export default App
