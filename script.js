document.addEventListener('DOMContentLoaded', () => {
    const menuItems = document.querySelectorAll('.sidebar ul li');
    const formTitle = document.getElementById('form-title');
    const actionForm = document.getElementById('action-form');
    const dynamicInputs = document.getElementById('dynamic-inputs');
    const executeButton = document.getElementById('execute');
    const outputDiv = document.getElementById('output');

    // Event listener for menu item clicks
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            const action = item.getAttribute('data-action');
            formTitle.textContent = `Action: ${item.textContent}`;
            actionForm.classList.remove('hidden');
            dynamicInputs.innerHTML = '';

            if (action === '1') { // Add Patient
                dynamicInputs.innerHTML = `
                    <input id="name" placeholder="Patient Name" required>
                    <input id="age" type="number" placeholder="Age" required>
                    <input id="ailment" placeholder="Ailment" required>
                `;
            } else if (action === '11') { // Show Patient
                dynamicInputs.innerHTML = `<p>No inputs required to show patients.</p>`;
            } else if (action === '2') { // Schedule Appointment
                dynamicInputs.innerHTML = `
                    <input id="name" placeholder="Patient Name" required>
                    <input id="time" placeholder="Appointment Time" required>
                `;
            } else if (action === '3') { // Add Resource
                dynamicInputs.innerHTML = `
                    <input id="resource" placeholder="Resource Name" required>
                    <input id="count" type="number" placeholder="Count" required>
                `;
            } else if (action === '5') { // Patient Check-In
                dynamicInputs.innerHTML = `
                    <input id="patient-name" placeholder="Patient Name" required>
                    <input id="check-in-time" type="datetime-local" placeholder="Check-In Time" required>
                `;
            } else { // Default case for actions without inputs
                dynamicInputs.innerHTML = `<p>No additional inputs required for this action.</p>`;
            }

            executeButton.setAttribute('data-action', action);
        });
    });

    // Execute button logic
    executeButton.addEventListener('click', async () => {
        const action = executeButton.getAttribute('data-action');
        const inputs = dynamicInputs.querySelectorAll('input');
        const args = Array.from(inputs).map(input => input.value.trim());
        const command = `${action} ${args.join(' ')}`;

        try {
            const response = await fetch('http://127.0.0.1:5000/execute', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command })
            });
            const result = await response.json();
            outputDiv.textContent = result.output || result.error || 'No output returned.';
        } catch (error) {
            outputDiv.textContent = 'Error connecting to the backend.';
            console.error(error);
        }
    });
});

