document.getElementById('calculateBtn').addEventListener('click', calculate);
document.getElementById('printBtn').addEventListener('click', () => window.print());


function formatCurrency(value) {
    return value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

function calculate() {
    const assetValue = parseFloat(document.getElementById('assetValue').value);
    const interestRate = parseFloat(document.getElementById('interestRate').value) / 100;
    const n = parseInt(document.getElementById('installments').value);
    const system = document.getElementById('system').value;

    if (isNaN(assetValue) || isNaN(interestRate) || isNaN(n) || n <= 0) {
        alert("Por favor, preencha todos os campos corretamente.");
        return;
    }

    const resultsSection = document.getElementById('resultsSection');
    const tableBody = document.querySelector('#installmentsTable tbody');
    tableBody.innerHTML = '';

    let balance = assetValue;
    let totalInterest = 0;
    let installments = [];

    if (system === 'price') {
        // Tabela Price Formula: PMT = PV * [i * (1+i)^n] / [(1+i)^n - 1]
        const pmt = assetValue * (interestRate * Math.pow(1 + interestRate, n)) / (Math.pow(1 + interestRate, n) - 1);
        
        for (let i = 1; i <= n; i++) {
            const interest = balance * interestRate;
            const amortization = pmt - interest;
            const discount = pmt - (pmt / Math.pow(1 + interestRate, i));
            
            installments.push({
                num: i,
                pmt: pmt,
                amortization: amortization,
                interest: interest,
                balance: Math.max(0, balance - amortization),
                discount: discount
            });
            
            balance -= amortization;
            totalInterest += interest;
        }
    } else {
        // SAC Formula: Amortization = PV / n
        const amortization = assetValue / n;
        
        for (let i = 1; i <= n; i++) {
            const interest = balance * interestRate;
            const pmt = amortization + interest;
            const discount = pmt - (pmt / Math.pow(1 + interestRate, i));
            
            installments.push({
                num: i,
                pmt: pmt,
                amortization: amortization,
                interest: interest,
                balance: Math.max(0, balance - amortization),
                discount: discount
            });
            
            balance -= amortization;
            totalInterest += interest;
        }
    }

    // Update Summary
    document.getElementById('detailValue').innerText = formatCurrency(assetValue);
    document.getElementById('detailRate').innerText = (interestRate * 100).toFixed(2) + "% a.m.";
    document.getElementById('detailInstallments').innerText = n + "x (" + (system === 'price' ? 'Price' : 'SAC') + ")";

    document.getElementById('totalFinanced').innerText = formatCurrency(assetValue + totalInterest);
    document.getElementById('totalInterest').innerText = formatCurrency(totalInterest);
    document.getElementById('firstInstallment').innerText = formatCurrency(installments[0].pmt);
    document.getElementById('lastInstallment').innerText = formatCurrency(installments[installments.length - 1].pmt);

    // Populate Table
    installments.forEach(inst => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${inst.num}</td>
            <td class="highlight">${formatCurrency(inst.pmt)}</td>
            <td>${formatCurrency(inst.amortization)}</td>
            <td>${formatCurrency(inst.interest)}</td>
            <td>${formatCurrency(inst.balance)}</td>
            <td><span class="discount-badge">-${formatCurrency(inst.discount)}</span></td>
        `;
        tableBody.appendChild(row);
    });

    resultsSection.classList.remove('hidden');
    resultsSection.classList.add('animate-fade-in');
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}
