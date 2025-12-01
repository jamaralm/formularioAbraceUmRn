let ANSWERS = {};

function calculateUrgencyScore() {
    const form = document.getElementById('ongForm');
    let totalScore = 0;

    const scoredElements = form.querySelectorAll('input[data-score]');

    scoredElements.forEach(element => {
        const scoreString = element.getAttribute('data-score');

        if (scordeString !== null) {
            const score = parseInt(scoreString);

            if (!isNaN(score)) {
                totalScore += score;
            }
        }
    });

    return totalScore;
}

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('ongForm');

    // Função para armazenar respostas no objeto ANSWERS
    window.store_answers = function() {
        const formData = new FormData(form);
        formData.forEach((value, key) => {
            ANSWERS[key] = value;
        });
        console.log(ANSWERS); // Para depuração
    };

    ANSWERS['urgencyScore'] = calculateUrgencyScore();
});

document.addEventListener('DOMContentLoaded', () => {
    // --- NAVEGAÇÃO EM ETAPAS ---
    const steps = Array.from(document.querySelectorAll('.form-step'));
    const progressSteps = Array.from(document.querySelectorAll('.progress-step'));
    const nextBtn = document.getElementById('nextBtn');
    const prevBtn = document.getElementById('prevBtn');
    const submitBtn = document.getElementById('submitBtn');
    const form = document.getElementById('ongForm');
    
    let currentStep = 0;

    const updateFormSteps = () => {
        steps.forEach((step, index) => {
            step.classList.toggle('active', index === currentStep);
        });
        
        progressSteps.forEach((step, index) => {
            step.classList.toggle('active', index <= currentStep);
        });

        prevBtn.style.display = currentStep === 0 ? 'none' : 'block';
        nextBtn.style.display = currentStep === steps.length - 1 ? 'none' : 'block';
        submitBtn.style.display = currentStep === steps.length - 1 ? 'block' : 'none';
    };
    
    nextBtn.addEventListener('click', () => {
        // Validate all enabled controls in the current step before advancing
        const currentEl = steps[currentStep];
        if (currentEl) {
            const controls = Array.from(currentEl.querySelectorAll('input, select, textarea'));
            for (const c of controls) {
                if (!c || c.disabled) continue; // skip disabled controls
                if (!c.checkValidity()) {
                    // report the browser validation message and don't advance
                    c.reportValidity();
                    return;
                }
            }
        }

        if (currentStep < steps.length - 1) {
            currentStep++;
            updateFormSteps();
        }
    });

    prevBtn.addEventListener('click', () => {
        if (currentStep > 0) {
            currentStep--;
            updateFormSteps();
        }
    });
    
    updateFormSteps(); // Inicializa o formulário

    // --- LÓGICA CONDICIONAL ---
    // Toggle the conditional block visibility and enable/disable form controls inside it
    const addConditionalListener = (radioName, conditionalDivId, showOnValue = 'sim') => {
        const setControlsDisabled = (div, disabled) => {
            if (!div) return;
            Array.from(div.querySelectorAll('input, select, textarea, button')).forEach(el => {
                // keep radios that control other conditionals enabled
                if (el.name === radioName) return;
                el.disabled = disabled;
            });
        };

        document.querySelectorAll(`input[name="${radioName}"]`).forEach(radio => {
            radio.addEventListener('change', (e) => {
                const div = document.getElementById(conditionalDivId);
                const shouldShow = e.target.value === showOnValue;
                div.classList.toggle('hidden', !shouldShow);
                setControlsDisabled(div, !shouldShow);
            });

            // set initial state for this conditional control
            const current = document.querySelector(`input[name="${radioName}"]:checked`);
            if (current) {
                const div = document.getElementById(conditionalDivId);
                const shouldShow = current.value === showOnValue;
                div.classList.toggle('hidden', !shouldShow);
                setControlsDisabled(div, !shouldShow);
            }
        });
    };
    
    // 3. Gestação ou Bebê
    addConditionalListener('statusGestacao', 'divGravida', 'gravida');
    addConditionalListener('statusGestacao', 'divBebe', 'bebe');
    addConditionalListener('preNatal', 'divLocalPreNatal');
    
    // 6. Saúde e Apoio
    addConditionalListener('medicamento', 'divQualMedicamento');
    addConditionalListener('programaSocial', 'divQualPrograma');

    // Lista de Itens 

    const novoItemInput = document.getElementById('novoItem');
    const listaItens = document.getElementById('listaItens');

    if (novoItemInput && listaItens) {
        novoItemInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                const texto = novoItemInput.value.trim();
                if (texto !== "") {
                    const li = document.createElement('li');
                    li.innerHTML = `${texto} <button type="button" class="remover-item">✖</button>`;
                    listaItens.appendChild(li);
                    novoItemInput.value = '';
                }
            }
        });

        listaItens.addEventListener('click', (e) => {
            if (e.target.classList.contains('remover-item')) {
                e.target.parentElement.remove();
            }
        });
    }

    // imagem upload removed — UI handled only on frontend (no preview required anymore)
    
    // --- LÓGICA DE ENVIO ---
    const fonteRendaSelect = document.getElementById('fonteRenda');
    form.addEventListener('submit', (event) => {
        if (!form.checkValidity()) {
            event.preventDefault(); 
            alert("Por favor, preencha todos os campos antes de continuar!");
            return; 
        }

        event.preventDefault(); 

        const agora = new Date();
        const dataEnvioFormatada = agora.toISOString().slice(0, 19).replace('T', ' ');
        document.getElementById('dataEnvio').value = dataEnvioFormatada;

        // (data/time stored and ready to be sent to a backend if needed)
        const formData = new FormData(form);
        const dados = Object.fromEntries(formData.entries()); // transforma tudo em objeto

        // Instagram checkbox is optional; there is no required image upload.

        console.log('Dados enviados:', dados);

        if (fonteRendaSelect.value === 'beneficio') {
            alert("Obrigado por preencher! Agora vamos te mostrar como comprovar o seu benefício.");
            window.location.href = 'comprovante.html';
        } else {
            alert("Formulário enviado com sucesso! Entraremos em contato em breve. ❤️");
            form.reset();
            currentStep = 0;
            updateFormSteps(); // Volta para a primeira etapa
        }
    });

    // Simple native input formatting helpers (no jQuery dependency)
    const onlyDigits = (value) => value.replace(/\D/g, '');

    const formatCPF = (value) => {
        const d = onlyDigits(value).slice(0, 11);
        return d.replace(/(\d{3})(\d{3})(\d{3})(\d{0,2})/, (m, a, b, c, e) => {
            return a + (b ? '.' + b : '') + (c ? '.' + c : '') + (e ? '-' + e : '');
        });
    };

    const formatPhone = (value) => {
        const d = onlyDigits(value).slice(0, 11);
        if (d.length <= 10) return d.replace(/(\d{2})(\d{4})(\d{0,4})/, (m, a, b, c) => a ? `(${a}) ${b}${c ? '-' + c : ''}` : '');
        return d.replace(/(\d{2})(\d{5})(\d{0,4})/, (m, a, b, c) => `(${a}) ${b}${c ? '-' + c : ''}`);
    };

    const formatRG = (value) => onlyDigits(value).slice(0, 10);

    const cpfEl = document.getElementById('cpf');
    const telefoneEl = document.getElementById('telefone');
    const rgEl = document.getElementById('rg');

    if (cpfEl) cpfEl.addEventListener('input', (e) => { e.target.value = formatCPF(e.target.value); });
    if (telefoneEl) telefoneEl.addEventListener('input', (e) => { e.target.value = formatPhone(e.target.value); });
    if (rgEl) rgEl.addEventListener('input', (e) => { e.target.value = formatRG(e.target.value); });
});

