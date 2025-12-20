// app.js
const API_BASE = "http://127.0.0.1:8000"; // leave empty for same origin, or e.g. "http://127.0.0.1:8000"

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("predict-form");
  const locationSelect = document.getElementById("location");
  const resultWrap = document.getElementById("result");
  const spinner = document.getElementById("spinner");
  const estimated = document.getElementById("estimated");
  const errorEl = document.getElementById("error");
  const resetBtn = document.getElementById("reset-btn");

  // Load locations into select
  async function loadLocations() {
    try {
      const res = await fetch(`${API_BASE}/get_location_names`);
      if (!res.ok) throw new Error(`Status ${res.status}`);
      const data = await res.json();
      // server returns { "message": [locations...] }
      const locations = data?.message ?? [];
      locationSelect.innerHTML = "";
      if (!locations.length) {
        const opt = document.createElement("option");
        opt.value = "";
        opt.textContent = "No locations available";
        locationSelect.appendChild(opt);
        return;
      }
      const defaultOpt = document.createElement("option");
      defaultOpt.value = "";
      defaultOpt.textContent = "Select location";
      defaultOpt.disabled = true;
      defaultOpt.selected = true;
      locationSelect.appendChild(defaultOpt);

      // Sort (case-insensitive)
      locations.sort((a, b) =>
        a.toString().toLowerCase().localeCompare(b.toString().toLowerCase())
      );

      for (const loc of locations) {
        const opt = document.createElement("option");
        opt.value = loc;
        opt.textContent = loc;
        locationSelect.appendChild(opt);
      }
    } catch (err) {
      console.error("Failed to load locations:", err);
      locationSelect.innerHTML = "";
      const opt = document.createElement("option");
      opt.value = "";
      opt.textContent = "Could not load locations";
      locationSelect.appendChild(opt);
    }
  }

  loadLocations();

  function showSpinner() {
    resultWrap.classList.remove("hidden");
    spinner.classList.remove("hidden");
    estimated.classList.add("hidden");
    errorEl.classList.add("hidden");
  }
  function showResult(text) {
    spinner.classList.add("hidden");
    estimated.classList.remove("hidden");
    estimated.textContent = text;
    errorEl.classList.add("hidden");
  }
  function showError(msg) {
    spinner.classList.add("hidden");
    errorEl.classList.remove("hidden");
    errorEl.textContent = msg;
    estimated.classList.add("hidden");
  }

  form.addEventListener("submit", async (ev) => {
    ev.preventDefault();
    errorEl.textContent = "";
    estimated.textContent = "";

    // gather form values
    const total_sqft = document.getElementById("total_sqft").value.trim();
    const bath = document.getElementById("bath").value.trim();
    const balcony = document.getElementById("balcony").value.trim();
    const bedroom = document.getElementById("bedroom").value.trim();
    const location = document.getElementById("location").value;

    // basic client validation
    if (!total_sqft || !bath || !balcony || !bedroom || !location) {
      showError("Please fill out all fields.");
      resultWrap.classList.remove("hidden");
      return;
    }

    const payload = {
      total_sqft: Number(total_sqft),
      bath: Number(bath),
      balcony: Number(balcony),
      bedroom: Number(bedroom),
      location: location
    };

    showSpinner();

    try {
      const res = await fetch(`${API_BASE}/predict_home_price`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        // try to read error message from response
        let errText = `Server returned ${res.status}`;
        try {
          const errJson = await res.json();
          errText = errJson.detail ?? JSON.stringify(errJson);
        } catch (e) { /* ignore parse error */ }
        showError(errText);
        return;
      }

      const data = await res.json();
      const price = data?.estimated_price;

      if (price == null) {
        showError("No price returned from server.");
        return;
      }

      // Format price nicely (you can change locale/currency)
      const formatted = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        maximumFractionDigits: 2
      }).format(price*100000*0.011);

      showResult(`Estimated Price: ${formatted}`);

    } catch (err) {
      console.error("Request failed", err);
      showError("Network error: could not reach server.");
    }
  });

  resetBtn.addEventListener("click", () => {
    form.reset();
    locationSelect.selectedIndex = 0;
    resultWrap.classList.add("hidden");
    errorEl.textContent = "";
    estimated.textContent = "";
  });
});
