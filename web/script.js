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

        // --- Exemplo de envio da data para o backend (opcional) ---
        // Aqui você pode enviar junto com os outros dados:
        const formData = new FormData(form);
        const dados = Object.fromEntries(formData.entries()); // transforma tudo em objeto

        // remover depois
        console.log("Dados enviados:", dados);

        // Caso você use fetch pra mandar pro backend da Oracle:
        /*
        fetch('https://seu-endpoint.oraclecloud.com/receber-dados', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        })
        .then(response => response.json())
        .then(data => console.log('Enviado com sucesso:', data))
        .catch(error => console.error('Erro:', error));
        */

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

    $(document).ready(function(){
    $('#cpf').mask('000.000.000-00');
    $('#telefone').mask('(00) 00000-0000');
    $('#rg').mask('0000000000'); 
    });
});

