/* Vibrant front-end JS:
   - drag & drop + file picker
   - POST multipart to /classify/
   - show status, spinner
   - parse returned CSV to preview table
   - provide download link
*/

const fileInput = document.getElementById("fileInput");
const dropzone = document.getElementById("dropzone");
const submitBtn = document.getElementById("submitBtn");
const spinner = document.getElementById("spinner");
const btnText = document.getElementById("btnText");
const statusEl = document.getElementById("status");
const downloadLink = document.getElementById("downloadLink");
const previewSection = document.getElementById("previewSection");
const previewTable = document.getElementById("previewTable");
const PREVIEW_ROWS = 200; // cap preview rows

let selectedFile = null;

// utility: simple CSV parser that handles quoted fields
function parseCSV(text) {
  const rows = [];
  let cur = [];
  let curField = "";
  let inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    const nxt = text[i + 1] ?? "";
    if (ch === '"' ) {
      if (inQuotes && nxt === '"') { // escaped quote
        curField += '"';
        i++;
      } else {
        inQuotes = !inQuotes;
      }
      continue;
    }
    if (ch === "," && !inQuotes) {
      cur.push(curField);
      curField = "";
      continue;
    }
    if ((ch === "\n" || ch === "\r") && !inQuotes) {
      if (ch === "\r" && nxt === "\n") { i++; } // windows CRLF
      cur.push(curField);
      rows.push(cur);
      cur = [];
      curField = "";
      continue;
    }
    curField += ch;
  }
  // last field
  if (curField !== "" || cur.length) {
    cur.push(curField);
    rows.push(cur);
  }
  return rows;
}

function setStatus(text, err = false){
  statusEl.textContent = text;
  statusEl.style.color = err ? "var(--danger)" : "inherit";
}

// drag & drop handlers
["dragenter","dragover"].forEach(evt=>{
  dropzone.addEventListener(evt, (e)=>{
    e.preventDefault(); e.stopPropagation();
    dropzone.classList.add("dragover");
  });
});
["dragleave","drop"].forEach(evt=>{
  dropzone.addEventListener(evt, (e)=>{
    e.preventDefault(); e.stopPropagation();
    dropzone.classList.remove("dragover");
  });
});

dropzone.addEventListener("drop", (e)=>{
  const f = e.dataTransfer.files?.[0];
  if (f) handleFileChoice(f);
});

fileInput.addEventListener("change", (e)=>{
  const f = e.target.files?.[0];
  if (f) handleFileChoice(f);
});

dropzone.addEventListener("keydown", (e)=>{
  if(e.key === "Enter" || e.key === " ") fileInput.click();
});

function handleFileChoice(file){
  selectedFile = file;
  submitBtn.disabled = false;
  setStatus(`Selected: ${file.name} — ${Math.round(file.size/1024)} KB`);
}

// UI state helpers
function startLoading(){
  submitBtn.disabled = true;
  spinner.style.display = "inline-block";
  btnText.textContent = "Processing...";
  setStatus("Uploading and classifying — please wait...");
  downloadLink.style.display = "none";
  previewSection.classList.add("hidden");
}

function stopLoading(){
  submitBtn.disabled = false;
  spinner.style.display = "none";
  btnText.textContent = "Classify Logs";
}

// submit handler
submitBtn.addEventListener("click", async (e)=>{
  e.preventDefault();
  if(!selectedFile){
    alert("Please select a CSV file first.");
    return;
  }

  startLoading();

  try {
    const form = new FormData();
    form.append("file", selectedFile);

    const resp = await fetch("http://localhost:8000/classify/", {
      method: "POST",
      body: form
    });

    if (!resp.ok) {
      // try to read JSON error
      let errText = `Server returned ${resp.status}`;
      try {
        const j = await resp.json();
        errText = j.detail || JSON.stringify(j);
      } catch(_) {
        errText = await resp.text();
      }
      setStatus(`Error: ${errText}`, true);
      stopLoading();
      return;
    }

    // Get blob (CSV), prepare download
    const blob = await resp.blob();
    const url = window.URL.createObjectURL(blob);
    downloadLink.href = url;
    downloadLink.style.display = "inline-block";
    downloadLink.download = "classified_logs.csv";

    // parse preview
    const text = await blob.text();
    const rows = parseCSV(text);
    if(rows.length===0){
      setStatus("Received empty CSV from server", true);
      stopLoading();
      return;
    }

    // populate table (limit rows for performance)
    const head = rows[0];
    const body = rows.slice(1, 1 + PREVIEW_ROWS);

    // build header
    const thead = previewTable.querySelector("thead");
    const tbody = previewTable.querySelector("tbody");
    thead.innerHTML = "";
    tbody.innerHTML = "";

    const trh = document.createElement("tr");
    head.forEach(h=>{
      const th = document.createElement("th");
      th.textContent = h || "(empty)";
      trh.appendChild(th);
    });
    thead.appendChild(trh);

    body.forEach(r=>{
      const tr = document.createElement("tr");
      head.forEach((_,i)=>{
        const td = document.createElement("td");
        td.textContent = r[i] ?? "";
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });

    previewSection.classList.remove("hidden");

    setStatus(`Success — previewing ${body.length} row(s). Download available.`);
  } catch (err) {
    console.error(err);
    setStatus("Network or server error: " + err.message, true);
  } finally {
    stopLoading();
  }

});
