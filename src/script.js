document.addEventListener('DOMContentLoaded', () => {
    // ==========================================
    // SPA NAVIGATION LOGIC
    // ==========================================
    const menuItems = document.querySelectorAll('.menu-item');
    const dashboardViews = document.querySelectorAll('main.view');
    const aiPanels = document.querySelectorAll('aside.view');

    menuItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();

            // Get target view from data attribute
            const target = item.getAttribute('data-target');
            if (!target) return; // Ignore clicks on menu items without data-target

            // 1. Update Menu Active State
            menuItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');

            // 2. Hide all views and panels
            dashboardViews.forEach(view => view.classList.remove('active'));
            aiPanels.forEach(panel => panel.classList.remove('active'));

            // 3. Show target view and panel
            const targetDashboard = document.getElementById(`${target}-dashboard`);
            const targetAiPanel = document.getElementById(`${target}-ai`);

            if (targetDashboard) targetDashboard.classList.add('active');
            if (targetAiPanel) targetAiPanel.classList.add('active');
        });
    });

    // ==========================================
    // MODALS LOGIC
    // ==========================================
    // Add Money Modal
    const addMoneyBtn = document.querySelector('#overview-dashboard .btn-primary:has(.ph-plus)');
    const addMoneyModal = document.getElementById('addMoneyModal');
    const closeAddMoneyBtn = document.getElementById('closeAddMoneyBtn');
    const cancelAddMoneyBtn = document.getElementById('cancelAddMoneyBtn');
    const confirmAddMoneyBtn = document.getElementById('confirmAddMoneyBtn');
    const addMoneyAmountInput = document.getElementById('addMoneyAmount');
    const quickBtns = document.querySelectorAll('#addMoneyModal .quick-btn');

    // Open Modal
    if (addMoneyBtn && addMoneyModal) {
        addMoneyBtn.addEventListener('click', () => {
            addMoneyModal.classList.add('active');
            setTimeout(() => addMoneyAmountInput.focus(), 100);
        });
    }

    // Close Modal Logic
    const closeAddMoneyModal = () => {
        addMoneyModal.classList.remove('active');
        // Reset input and buttons
        setTimeout(() => {
            addMoneyAmountInput.value = '';
            quickBtns.forEach(btn => btn.classList.remove('active'));
        }, 300);
    };

    if (closeAddMoneyBtn) closeAddMoneyBtn.addEventListener('click', closeAddMoneyModal);
    if (cancelAddMoneyBtn) cancelAddMoneyBtn.addEventListener('click', closeAddMoneyModal);

    // Close on overlay click
    if (addMoneyModal) {
        addMoneyModal.addEventListener('click', (e) => {
            if (e.target === addMoneyModal) {
                closeAddMoneyModal();
            }
        });
    }

    // Quick Amounts Logic
    if (quickBtns.length > 0) {
        quickBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                // Remove active from all
                quickBtns.forEach(b => b.classList.remove('active'));
                // Add active to clicked
                btn.classList.add('active');

                // Parse value and set to input
                let val = btn.textContent.replace('$', '').replace('k', '000');
                addMoneyAmountInput.value = val;
            });
        });
    }

    // Confirm button logic
    if (confirmAddMoneyBtn) {
        confirmAddMoneyBtn.addEventListener('click', () => {
            const amount = addMoneyAmountInput.value;
            if (!amount || amount <= 0) {
                alert('Please enter a valid amount.');
                return;
            }

            // In a real app, send to backend here
            const originalText = confirmAddMoneyBtn.innerHTML;
            confirmAddMoneyBtn.innerHTML = '<i class="ph ph-spinner ph-spin"></i> Processing...';
            confirmAddMoneyBtn.style.opacity = '0.8';
            confirmAddMoneyBtn.style.pointerEvents = 'none';

            setTimeout(() => {
                confirmAddMoneyBtn.innerHTML = '<i class="ph ph-check-circle"></i> Success!';
                confirmAddMoneyBtn.style.backgroundColor = '#008F4C';
                confirmAddMoneyBtn.style.color = '#FFF';

                setTimeout(() => {
                    closeAddMoneyModal();
                    // Reset button state
                    setTimeout(() => {
                        confirmAddMoneyBtn.innerHTML = originalText;
                        confirmAddMoneyBtn.style.backgroundColor = '';
                        confirmAddMoneyBtn.style.color = '';
                        confirmAddMoneyBtn.style.opacity = '1';
                        confirmAddMoneyBtn.style.pointerEvents = 'auto';

                        // Optional: update balance here in a real app
                    }, 300);
                }, 1000);
            }, 1000);
        });
    }

    // ==========================================
    // CHART.JS LOGIC (Overview Dashboard)
    // ==========================================
    const chartCanvas = document.getElementById('spendingChart');
    if (chartCanvas) {
        const ctx = chartCanvas.getContext('2d');

        // Gradient for the primary segment
        const gradient1 = ctx.createLinearGradient(0, 0, 0, 400);
        gradient1.addColorStop(0, '#00E57A');
        gradient1.addColorStop(1, '#008F4C');

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Housing', 'Groceries', 'Entertainment'],
                datasets: [{
                    data: [40, 30, 30],
                    backgroundColor: [
                        '#00E57A', // highlight-1
                        '#008F4C', // highlight-2
                        '#244231'  // highlight-3
                    ],
                    borderWidth: 0,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '75%',
                plugins: {
                    legend: {
                        display: false // Custom HTML legend inside Spending Breakdown
                    },
                    tooltip: {
                        backgroundColor: '#111A15',
                        titleColor: '#8FA396',
                        bodyColor: '#FFFFFF',
                        borderColor: 'rgba(0, 229, 122, 0.2)',
                        borderWidth: 1,
                        padding: 12,
                        displayColors: true,
                        callbacks: {
                            label: function (context) {
                                return ` ${context.label}: ${context.parsed}%`;
                            }
                        }
                    }
                },
                animation: {
                    animateScale: true,
                    animateRotate: true
                }
            }
        });
    }
});
