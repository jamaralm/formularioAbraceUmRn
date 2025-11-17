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
    const addConditionalListener = (radioName, conditionalDivId, showOnValue = 'sim') => {
        document.querySelectorAll(`input[name="${radioName}"]`).forEach(radio => {
            radio.addEventListener('change', (e) => {
                const div = document.getElementById(conditionalDivId);
                div.classList.toggle('hidden', e.target.value !== showOnValue);
            });
        });
    };
    
    // 3. Gestação ou Bebê
    addConditionalListener('statusGestacao', 'divGravida', 'gravida');
    addConditionalListener('statusGestacao', 'divBebe', 'bebe');
    addConditionalListener('preNatal', 'divLocalPreNatal');
    
    // 6. Saúde e Apoio
    addConditionalListener('medicamento', 'divQualMedicamento');
    addConditionalListener('programaSocial', 'divQualPrograma');
    
    // --- LÓGICA DE ENVIO ---
    const fonteRendaSelect = document.getElementById('fonteRenda');
    form.addEventListener('submit', (event) => {
        event.preventDefault(); 
        
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
});

function sendFormDataToApi() {
    try {
        fetch('http://localhost/api/formSubmit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(ANSWERS)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    } catch (error) {
        console.error('Unexpected Error:', error
        )
    }
}