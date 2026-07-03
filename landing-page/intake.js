(function () {
  const form = document.getElementById("intake-form");
  if (!form) return;

  const steps = Array.from(form.querySelectorAll("[data-step]"));
  const progressFill = document.querySelector("[data-progress-fill]");
  const indicators = Array.from(document.querySelectorAll("[data-step-indicator]"));
  const backButton = form.querySelector("[data-step-back]");
  const nextButton = form.querySelector("[data-step-next]");
  const submitButton = form.querySelector("[data-step-submit]");
  const successBox = document.getElementById("intake-success");
  const errorBox = document.getElementById("intake-error");
  const nextField = document.getElementById("intake-next");
  const summaryField = document.getElementById("intake-summary-field");
  const requestTypeField = document.getElementById("request-type-field");
  const summaryBox = document.getElementById("intake-summary");
  const contactSection = document.getElementById("contatto");
  const mobileCta = document.querySelector(".mobile-cta");
  const startingModeInputs = Array.from(form.querySelectorAll('input[name="Come vuoi partire"]'));
  let currentStep = 0;

  const fieldGroups = [
    ["name", "website", "sector", "webmaster"],
    ["goal", "priority"],
    ["email", "contact-name", "timing", "consent"],
  ];

  nextField.value = `${window.location.origin}${window.location.pathname}?sent=1#contatto`;

  function updateStep() {
    steps.forEach((step, index) => {
      const isCurrent = index === currentStep;
      step.hidden = !isCurrent;
      step.classList.toggle("is-active", isCurrent);
    });

    indicators.forEach((indicator, index) => {
      indicator.classList.toggle("is-active", index === currentStep);
    });

    if (progressFill) {
      progressFill.style.width = `${((currentStep + 1) / steps.length) * 100}%`;
    }

    backButton.hidden = currentStep === 0;
    nextButton.hidden = currentStep === steps.length - 1;
    submitButton.hidden = currentStep !== steps.length - 1;

    if (currentStep === steps.length - 1) {
      updateSummary();
    }
  }

  function validateStep(index) {
    const ids = fieldGroups[index];
    for (const id of ids) {
      const field = document.getElementById(id);
      if (!field) continue;
      if (!field.reportValidity()) {
        return false;
      }
    }
    return true;
  }

  function getChosenMode() {
    const checked = startingModeInputs.find((input) => input.checked);
    return checked ? checked.value : "Da valutare";
  }

  function updateSummary() {
    const summaryItems = [
      `Attività: ${document.getElementById("name").value || "-"}`,
      `Sito: ${document.getElementById("website").value || "-"}`,
      `Obiettivo: ${document.getElementById("goal").value || "-"}`,
      `Come vuole partire: ${getChosenMode()}`,
      `Tempistica: ${document.getElementById("timing").value || "-"}`,
    ];

    requestTypeField.value = getChosenMode();
    summaryField.value = summaryItems.join(" | ");

    summaryBox.innerHTML = `
      <strong>Riepilogo richiesta</strong>
      <ul>
        ${summaryItems.map((item) => `<li>${item}</li>`).join("")}
      </ul>
    `;
  }

  function showSuccess() {
    form.hidden = true;
    errorBox.hidden = true;
    successBox.hidden = false;
    successBox.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function showError() {
    errorBox.hidden = false;
    successBox.hidden = true;
  }

  nextButton.addEventListener("click", function () {
    if (!validateStep(currentStep)) return;
    currentStep += 1;
    updateStep();
  });

  backButton.addEventListener("click", function () {
    currentStep -= 1;
    updateStep();
  });

  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    if (!validateStep(currentStep)) return;

    updateSummary();
    errorBox.hidden = true;
    submitButton.disabled = true;
    submitButton.textContent = "Invio in corso...";

    const formData = new FormData(form);

    try {
      const response = await fetch("https://formsubmit.co/ajax/e8ec857b0d8bfe719a8a391d716536b2", {
        method: "POST",
        headers: {
          Accept: "application/json",
        },
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Submission failed");
      }

      const result = await response.json();
      if (result.success === "true" || result.message || response.ok) {
        showSuccess();
        window.history.replaceState({}, "", `${window.location.pathname}?sent=1#contatto`);
      } else {
        throw new Error("Unexpected response");
      }
    } catch (error) {
      showError();
      form.submit();
    } finally {
      submitButton.disabled = false;
      submitButton.textContent = "Invia richiesta";
    }
  });

  if (window.location.search.includes("sent=1")) {
    showSuccess();
  } else {
    updateStep();
  }

  if (mobileCta && contactSection) {
    const updateMobileCta = function () {
      const rect = contactSection.getBoundingClientRect();
      const isInContactViewport = rect.top < window.innerHeight * 0.8 && rect.bottom > 120;
      mobileCta.classList.toggle("is-hidden", isInContactViewport);
    };

    updateMobileCta();
    window.addEventListener("scroll", updateMobileCta, { passive: true });
    window.addEventListener("resize", updateMobileCta);
  }
})();
