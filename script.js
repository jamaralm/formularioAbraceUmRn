const form = document.getElementById("formulario");
const steps = document.querySelectorAll(".form-step");
let currentStep = 0;
let formData = {};

function showStep(index) {
  steps.forEach((step, i) => {
    step.classList.toggle("active", i === index);
  });
}

document.querySelectorAll(".next").forEach(btn => {
  btn.addEventListener("click", () => {
    const inputs = steps[currentStep].querySelectorAll("input, select, textarea");
    inputs.forEach(input => {
      formData[input.name] = input.value;
    });
    currentStep++;
    if (currentStep < steps.length) showStep(currentStep);
    if (steps[currentStep].dataset.step === "final") {
      gerarResumo();
    }
  });
});

document.querySelectorAll(".prev").forEach(btn => {
  btn.addEventListener("click", () => {
    if (currentStep > 0) {
      currentStep--;
      showStep(currentStep);
    }
  });
});

function gerarResumo() {
  let texto = "🩷 *Resumo do Cadastro:*\n\n";
  for (let campo in formData) {
    texto += `• ${campo.replace("_", " ")}: ${formData[campo]}\n`;
  }
  document.getElementById("resumo").textContent = texto;
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  alert("Formulário enviado com sucesso!");
  console.log("Dados finais:", formData);
});

document.getElementById("fonte_renda").addEventListener("change", (e) => {
  const tutorial = document.getElementById("bolsa_familia_tutorial");
  if (e.target.value === "Benefício social") {
    tutorial.style.display = "block";
  } else {
    tutorial.style.display = "none";
  }
});

const medSelect = document.getElementById("medicamento_continuo");
const qualMed = document.getElementById("qual_medicamento");
if (medSelect) {
  medSelect.addEventListener("change", () => {
    qualMed.style.display = medSelect.value === "Sim" ? "block" : "none";
  });
}

const progSelect = document.getElementById("programa_social");
const qualProg = document.getElementById("qual_programa");
if (progSelect) {
  progSelect.addEventListener("change", () => {
    qualProg.style.display = progSelect.value === "Sim" ? "block" : "none";
  });
}
