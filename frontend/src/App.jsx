import { useState } from "react";
import { Activity, Camera, CircleAlert, ShieldCheck, Upload, Zap } from "lucide-react";
import { detectWithBackend } from "./services/api";

const signs = [
  { name: "Stop", shape: "octagon", color: "#ef4444", note: "Come to a complete stop." },
  { name: "Speed limit", shape: "circle", color: "#f8fafc", note: "Follow the posted speed limit." },
  { name: "No entry", shape: "circle", color: "#ef4444", note: "Vehicles must not enter." },
  { name: "Pedestrian crossing", shape: "triangle", color: "#facc15", note: "Watch for pedestrians." }
];

export default function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function analyze() {
    if (!file) return;
    setBusy(true); setError(""); setResult(null);
    try { setResult(await detectWithBackend(file)); }
    catch { setError("Could not reach the backend. Start the Flask API on port 5000, or use the demo panel below."); }
    finally { setBusy(false); }
  }

  function demo() {
    setError("");
    setResult({ mode: "mock", detections: [{ class: "Stop Sign", confidence: 0.964, x: 120, y: 85, width: 80, height: 95 }] });
  }

  return <div className="app-shell">
    <header className="topbar"><a className="brand" href="#"><span className="brand-mark"><Activity size={20}/></span>TrafficVision<span className="brand-ai">AI</span></a><span className="status"><i/> Prototype · Demo mode</span></header>
    <main>
      <section className="hero"><div className="eyebrow"><Zap size={14}/> COMPUTER VISION FOR THE ROAD</div><h1>See the road.<br/><span>Understand the signs.</span></h1><p className="hero-copy">An interactive academic prototype exploring how traffic-sign detection can support smarter road awareness.</p><div className="hero-tags"><span><ShieldCheck size={15}/> Explainable demo</span><span><Camera size={15}/> Image analysis</span></div></section>
      <section className="workspace">
        <div className="panel upload-panel"><div className="panel-heading"><div><div className="eyebrow">01 / INPUT</div><h2>Analyze an image</h2></div><span className="step-icon"><Upload size={18}/></span></div>
          <label className="dropzone"><input type="file" accept="image/png,image/jpeg,image/webp" onChange={e=>{setFile(e.target.files?.[0]||null);setResult(null);setError("");}}/><span className="upload-icon"><Upload size={22}/></span><strong>{file ? file.name : "Choose a traffic image"}</strong><span>{file ? "Image selected — ready to analyze" : "PNG, JPG or WEBP · up to 10 MB"}</span><span className="choose-button">Browse files</span></label>
          {file && <div className="preview"><img src={URL.createObjectURL(file)} alt="Selected upload preview"/></div>}
          <button className="primary-button" disabled={!file||busy} onClick={analyze}>{busy ? "Analyzing…" : "Analyze with API"} <span>↗</span></button><button className="secondary-button" onClick={demo}>Try sample demo instead</button>
          {error && <p className="error"><CircleAlert size={15}/>{error}</p>}
        </div>
        <div className="panel results-panel"><div className="panel-heading"><div><div className="eyebrow">02 / RESULTS</div><h2>Detection report</h2></div><span className="live-label"><i/> LIVE PREVIEW</span></div>
          {!result ? <div className="empty-state"><div className="radar"><div/><Camera size={28}/></div><h3>Waiting for an image</h3><p>Upload an image and run analysis, or try the sample demo to see a mock detection report.</p><div className="empty-lines"><span/><span/><span/></div></div> : <div className="result-content"><div className="result-banner"><span className="result-check">✓</span><div><strong>{result.detections?.length || 0} sign(s) detected</strong><small>Mode: {result.mode || "mock"} · Illustrative output</small></div></div>{(result.detections||[]).map((d,i)=><div className="detection" key={i}><div className="sign-chip">⚠</div><div className="detection-info"><strong>{d.class}</strong><small>Bounding box · {d.width} × {d.height}</small><div className="confidence"><span style={{width:(d.confidence*100)+"%"}}/></div></div><strong className="percent">{Math.round(d.confidence*100)}%</strong></div>)}<p className="result-disclaimer">These are mock results for interface demonstration, not real model predictions.</p></div>}
        </div>
      </section>
      <section className="sign-section"><div className="section-intro"><div className="eyebrow">REFERENCE LIBRARY</div><h2>Know your signs</h2><p>A few common sign categories represented in the prototype.</p></div><div className="sign-grid">{signs.map(s=><article className="sign-card" key={s.name}><div className={"traffic-sign "+s.shape} style={{"--sign-color":s.color}}><span>{s.shape==="octagon"?"STOP":s.shape==="triangle"?"!":s.name==="No entry"?"−":"50"}</span></div><h3>{s.name}</h3><p>{s.note}</p></article>)}</div></section>
      <section className="notice"><ShieldCheck size={19}/><div><strong>Academic prototype — not for safety-critical use</strong><p>Current detections are mocked. No trained model weights or real YOLO inference are included. Never use this demo for driving decisions.</p></div></section>
    </main><footer><span>TRAFFICVISION AI</span><span>Built for learning · Computer vision prototype</span></footer>
  </div>;
}
