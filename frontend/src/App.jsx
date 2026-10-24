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
    catch (err) { setError(err?.message || "Could not reach the YOLO backend. Start Flask on port 5000 and check its terminal for errors."); }
    finally { setBusy(false); }
  }

  function demo() {
    setError("");
    setResult({ mode: "demo", detections: [] });
  }

  return <div className="app-shell">
    <header className="topbar"><a className="brand" href="#"><span className="brand-mark"><Activity size={20}/></span>TrafficVision<span className="brand-ai">AI</span></a><span className="status"><i/> YOLO · Computer vision</span></header>
    <main>
      <section className="hero"><div className="eyebrow"><Zap size={14}/> COMPUTER VISION FOR THE ROAD</div><h1>See the road.<br/><span>Understand the signs.</span></h1><p className="hero-copy">An academic prototype using YOLO object detection to analyze traffic images.</p><div className="hero-tags"><span><ShieldCheck size={15}/> Real model inference</span><span><Camera size={15}/> Image analysis</span></div></section>
      <section className="workspace">
        <div className="panel upload-panel"><div className="panel-heading"><div><div className="eyebrow">01 / INPUT</div><h2>Analyze an image</h2></div><span className="step-icon"><Upload size={18}/></span></div>
          <label className="dropzone"><input type="file" accept="image/png,image/jpeg,image/webp" onChange={e=>{setFile(e.target.files?.[0]||null);setResult(null);setError("");}}/><span className="upload-icon"><Upload size={22}/></span><strong>{file ? file.name : "Choose a traffic image"}</strong><span>{file ? "Image selected — ready to analyze" : "PNG, JPG or WEBP · up to 10 MB"}</span><span className="choose-button">Browse files</span></label>
          {file && <div className="preview"><img src={URL.createObjectURL(file)} alt="Selected upload preview"/></div>}
          <button className="primary-button" disabled={!file||busy} onClick={analyze}>{busy ? "Running YOLO…" : "Analyze with YOLO"} <span>↗</span></button><button className="secondary-button" onClick={demo}>Show empty report example</button>
          {error && <p className="error"><CircleAlert size={15}/>{error}</p>}
        </div>
        <div className="panel results-panel"><div className="panel-heading"><div><div className="eyebrow">02 / RESULTS</div><h2>Detection report</h2></div><span className="live-label"><i/> YOLO OUTPUT</span></div>
          {!result ? <div className="empty-state"><div className="radar"><div/><Camera size={28}/></div><h3>Waiting for an image</h3><p>Upload a traffic image and run YOLO inference to view detected objects, confidence scores and bounding boxes.</p><div className="empty-lines"><span/><span/><span/></div></div> : <div className="result-content"><div className="result-banner"><span className="result-check">✓</span><div><strong>{result.mode === "demo" ? "Example report only" : `${result.detections?.length || 0} object(s) detected`}</strong><small>{result.mode === "demo" ? "No inference performed" : "Mode: " + result.mode + (result.model ? " · " + result.model : "")}</small></div></div>{(result.detections||[]).map((d,i)=><div className="detection" key={i}><div className="sign-chip">⚠</div><div className="detection-info"><strong>{d.class}</strong><small>Bounding box · {d.width} × {d.height} px · x:{d.x}, y:{d.y}</small><div className="confidence"><span style={{width:(d.confidence*100)+"%"}}/></div></div><strong className="percent">{Math.round(d.confidence*100)}%</strong></div>)}{result.mode !== "demo" && !(result.detections||[]).length && <p>No objects detected above the confidence threshold. Try a clearer or closer image.</p>}<p className="result-disclaimer">{result.mode === "demo" ? "This is an empty example only. Upload an image and use Analyze with YOLO for actual model inference." : "The default COCO model detects general objects, including traffic lights, but is not trained to recognize speed-limit signs or signal colors. A custom traffic-sign model is needed for those classes."}</p></div>}
        </div>
      </section>
      <section className="sign-section"><div className="section-intro"><div className="eyebrow">REFERENCE LIBRARY</div><h2>Know your signs</h2><p>A few common sign categories relevant to traffic awareness.</p></div><div className="sign-grid">{signs.map(s=><article className="sign-card" key={s.name}><div className={"traffic-sign "+s.shape} style={{"--sign-color":s.color}}><span>{s.shape==="octagon"?"STOP":s.shape==="triangle"?"!":s.name==="No entry"?"−":"50"}</span></div><h3>{s.name}</h3><p>{s.note}</p></article>)}</div></section>
      <section className="notice"><ShieldCheck size={19}/><div><strong>Academic prototype — not for safety-critical use</strong><p>YOLO inference is connected. The default pretrained model has class limitations; use a suitable custom-trained model for speed-limit signs and traffic-signal state recognition.</p></div></section>
    </main><footer><span>TRAFFICVISION AI</span><span>YOLO object detection · Computer vision prototype</span></footer>
  </div>;
}
