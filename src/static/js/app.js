/* ==============================================
   INDIA POPULATION PREDICTION - APP.JS
   ============================================== */

// ============================================
// POPULATION DATA (UN World Population Prospects)
// ============================================
const populationData = {
    // Historical data (in millions)
    historical: {
        years: [1950, 1955, 1960, 1965, 1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025],
        population: [376, 409, 450, 499, 555, 623, 698, 784, 873, 964, 1057, 1148, 1234, 1310, 1380, 1450]
    },
    // Projected data (UN medium variant)
    projected: {
        years: [2025, 2030, 2035, 2040, 2045, 2050, 2055, 2060, 2065, 2070, 2075, 2080, 2085, 2090, 2095, 2100],
        population: [1450, 1515, 1565, 1610, 1645, 1670, 1685, 1695, 1697, 1690, 1675, 1655, 1625, 1590, 1560, 1533]
    },
    // Growth rate data (%)
    growthRate: {
        years: [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020, 2025, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100],
        rate: [1.8, 2.0, 2.2, 2.3, 2.1, 1.8, 1.5, 1.0, 0.9, 0.8, 0.5, 0.3, 0.1, -0.05, -0.15, -0.25, -0.3]
    },
    // World comparison data (population in millions for 2025 & 2050 projected)
    comparison: {
        countries: ['India', 'China', 'USA', 'Indonesia', 'Pakistan', 'Brazil', 'Nigeria'],
        pop2025: [1450, 1410, 340, 280, 240, 215, 230],
        pop2050: [1670, 1310, 375, 315, 370, 230, 400]
    }
};

// Full year-by-year interpolated data
function interpolatePopulation(year) {
    const allYears = [...populationData.historical.years, ...populationData.projected.years.slice(1)];
    const allPops = [...populationData.historical.population, ...populationData.projected.population.slice(1)];

    if (year <= allYears[0]) return allPops[0];
    if (year >= allYears[allYears.length - 1]) return allPops[allPops.length - 1];

    for (let i = 0; i < allYears.length - 1; i++) {
        if (year >= allYears[i] && year <= allYears[i + 1]) {
            const t = (year - allYears[i]) / (allYears[i + 1] - allYears[i]);
            return allPops[i] + t * (allPops[i + 1] - allPops[i]);
        }
    }
    return 0;
}

// ============================================
// CHART SETUP
// ============================================
Chart.defaults.color = '#94a3b8';
Chart.defaults.font.family = "'Inter', sans-serif";
Chart.defaults.borderColor = 'rgba(255,255,255,0.05)';

let populationChart, growthChart, comparisonChart;

function createPopulationChart() {
    const ctx = document.getElementById('populationChart').getContext('2d');

    // Combine all years for a smooth line
    const allYears = [...populationData.historical.years, ...populationData.projected.years.slice(1)];
    const allPops = [...populationData.historical.population, ...populationData.projected.population.slice(1)];

    // Historical portion
    const historicalPops = allYears.map((y, i) => y <= 2025 ? allPops[i] : null);
    // Projected portion
    const projectedPops = allYears.map((y, i) => y >= 2025 ? allPops[i] : null);

    // Gradient for historical
    const gradHist = ctx.createLinearGradient(0, 0, 0, 450);
    gradHist.addColorStop(0, 'rgba(255, 107, 53, 0.3)');
    gradHist.addColorStop(1, 'rgba(255, 107, 53, 0.02)');

    // Gradient for projected
    const gradProj = ctx.createLinearGradient(0, 0, 0, 450);
    gradProj.addColorStop(0, 'rgba(27, 156, 133, 0.25)');
    gradProj.addColorStop(1, 'rgba(27, 156, 133, 0.02)');

    populationChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: allYears,
            datasets: [
                {
                    label: 'Historical Population',
                    data: historicalPops,
                    borderColor: '#FF6B35',
                    backgroundColor: gradHist,
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0,
                    pointHoverRadius: 6,
                    pointHoverBackgroundColor: '#FF6B35',
                    pointHoverBorderColor: '#fff',
                    pointHoverBorderWidth: 2,
                    spanGaps: false
                },
                {
                    label: 'Projected Population',
                    data: projectedPops,
                    borderColor: '#1B9C85',
                    backgroundColor: gradProj,
                    borderWidth: 3,
                    borderDash: [8, 4],
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0,
                    pointHoverRadius: 6,
                    pointHoverBackgroundColor: '#1B9C85',
                    pointHoverBorderColor: '#fff',
                    pointHoverBorderWidth: 2,
                    spanGaps: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(10, 14, 26, 0.95)',
                    titleColor: '#f1f5f9',
                    bodyColor: '#94a3b8',
                    borderColor: 'rgba(255,255,255,0.1)',
                    borderWidth: 1,
                    padding: 14,
                    cornerRadius: 12,
                    titleFont: { family: "'Outfit', sans-serif", size: 16, weight: 700 },
                    bodyFont: { size: 14 },
                    displayColors: false,
                    callbacks: {
                        title: (items) => `Year ${items[0].label}`,
                        label: (item) => {
                            if (item.raw === null) return '';
                            return `Population: ${item.raw.toLocaleString()} Million`;
                        }
                    }
                },
                annotation: {
                    annotations: {
                        currentYear: {
                            type: 'line',
                            xMin: '2025',
                            xMax: '2025',
                            borderColor: 'rgba(247, 201, 72, 0.5)',
                            borderWidth: 2,
                            borderDash: [6, 3],
                            label: {
                                display: true,
                                content: '2025',
                                position: 'start',
                                font: { size: 12, weight: 600 },
                                backgroundColor: 'rgba(247, 201, 72, 0.2)',
                                color: '#F7C948',
                                padding: 6,
                                cornerRadius: 6
                            }
                        },
                        peakYear: {
                            type: 'point',
                            xValue: '2065',
                            yValue: 1697,
                            backgroundColor: 'rgba(255,107,53,0.3)',
                            borderColor: '#FF6B35',
                            borderWidth: 2,
                            radius: 8,
                            label: {
                                display: true,
                                content: 'Peak ~1.7B',
                                position: 'start',
                                font: { size: 11, weight: 600 },
                                backgroundColor: 'rgba(255,107,53,0.2)',
                                color: '#FF6B35',
                                padding: 6,
                                cornerRadius: 6,
                                yAdjust: -20
                            }
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: {
                        maxTicksLimit: 10,
                        font: { size: 12 }
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(255,255,255,0.04)',
                        drawBorder: false
                    },
                    ticks: {
                        callback: (v) => v + 'M',
                        font: { size: 12 },
                        maxTicksLimit: 8
                    },
                    beginAtZero: false,
                    min: 200
                }
            }
        }
    });
}

function createGrowthChart() {
    const ctx = document.getElementById('growthChart').getContext('2d');

    const colors = populationData.growthRate.rate.map(r => r >= 0 ? 'rgba(34, 197, 94, 0.8)' : 'rgba(239, 68, 68, 0.8)');
    const borderColors = populationData.growthRate.rate.map(r => r >= 0 ? '#22c55e' : '#ef4444');

    growthChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: populationData.growthRate.years,
            datasets: [{
                label: 'Growth Rate (%)',
                data: populationData.growthRate.rate,
                backgroundColor: colors,
                borderColor: borderColors,
                borderWidth: 1,
                borderRadius: 6,
                borderSkipped: false,
                barPercentage: 0.6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(10, 14, 26, 0.95)',
                    titleColor: '#f1f5f9',
                    bodyColor: '#94a3b8',
                    borderColor: 'rgba(255,255,255,0.1)',
                    borderWidth: 1,
                    padding: 14,
                    cornerRadius: 12,
                    titleFont: { family: "'Outfit', sans-serif", size: 16, weight: 700 },
                    displayColors: false,
                    callbacks: {
                        title: (items) => `Year ${items[0].label}`,
                        label: (item) => `Growth Rate: ${item.raw}%`
                    }
                },
                annotation: {
                    annotations: {
                        zeroLine: {
                            type: 'line',
                            yMin: 0,
                            yMax: 0,
                            borderColor: 'rgba(255,255,255,0.2)',
                            borderWidth: 1,
                            borderDash: [4, 4]
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { font: { size: 12 } }
                },
                y: {
                    grid: {
                        color: 'rgba(255,255,255,0.04)',
                        drawBorder: false
                    },
                    ticks: {
                        callback: (v) => v + '%',
                        font: { size: 12 }
                    }
                }
            }
        }
    });
}

function createComparisonChart() {
    const ctx = document.getElementById('comparisonChart').getContext('2d');

    comparisonChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: populationData.comparison.countries,
            datasets: [
                {
                    label: '2025',
                    data: populationData.comparison.pop2025,
                    backgroundColor: 'rgba(255, 107, 53, 0.7)',
                    borderColor: '#FF6B35',
                    borderWidth: 1,
                    borderRadius: 6,
                    barPercentage: 0.7,
                    categoryPercentage: 0.7
                },
                {
                    label: '2050 (Projected)',
                    data: populationData.comparison.pop2050,
                    backgroundColor: 'rgba(27, 156, 133, 0.7)',
                    borderColor: '#1B9C85',
                    borderWidth: 1,
                    borderRadius: 6,
                    barPercentage: 0.7,
                    categoryPercentage: 0.7
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        color: '#94a3b8',
                        usePointStyle: true,
                        pointStyle: 'rectRounded',
                        padding: 20,
                        font: { size: 13 }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(10, 14, 26, 0.95)',
                    titleColor: '#f1f5f9',
                    bodyColor: '#94a3b8',
                    borderColor: 'rgba(255,255,255,0.1)',
                    borderWidth: 1,
                    padding: 14,
                    cornerRadius: 12,
                    titleFont: { family: "'Outfit', sans-serif", size: 16, weight: 700 },
                    callbacks: {
                        label: (item) => `${item.dataset.label}: ${item.raw}M`
                    }
                }
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { font: { size: 12 } }
                },
                y: {
                    grid: {
                        color: 'rgba(255,255,255,0.04)',
                        drawBorder: false
                    },
                    ticks: {
                        callback: (v) => v + 'M',
                        font: { size: 12 },
                        maxTicksLimit: 8
                    }
                }
            }
        }
    });
}

// ============================================
// CHART TAB SWITCHING
// ============================================
document.querySelectorAll('.chart-tab').forEach(tab => {
    tab.addEventListener('click', () => {
        // Update active tab
        document.querySelectorAll('.chart-tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');

        // Show correct chart
        const chartType = tab.dataset.chart;
        document.querySelectorAll('.chart-container').forEach(c => c.classList.add('hidden'));
        document.getElementById(`chart-${chartType}-container`).classList.remove('hidden');
    });
});

// ============================================
// LIVE COUNTER
// ============================================
function updateLiveCounter() {
    const basePop = 1450000000; // 2025 baseline
    const growthPerSecond = 0.9 / 100 / 365.25 / 24 / 3600 * basePop;
    const startOf2025 = new Date('2025-01-01T00:00:00Z').getTime();
    const now = Date.now();
    const elapsed = (now - startOf2025) / 1000;
    const currentPop = Math.round(basePop + growthPerSecond * elapsed);

    const el = document.getElementById('liveCounter');
    el.textContent = currentPop.toLocaleString('en-IN');
}

setInterval(updateLiveCounter, 1000);
updateLiveCounter();

// ============================================
// POPULATION CALCULATOR / SLIDER
// ============================================
const yearSlider = document.getElementById('yearSlider');
const selectedYearEl = document.getElementById('selectedYear');
const resultPopEl = document.getElementById('resultPop');

yearSlider.addEventListener('input', () => {
    const year = parseInt(yearSlider.value);
    selectedYearEl.textContent = year;

    // Try Flask API first, fallback to client-side interpolation
    fetch(`/api/predict/${year}`)
        .then(res => res.json())
        .then(data => {
            resultPopEl.textContent = data.formatted || data.population.toLocaleString('en-IN');
        })
        .catch(() => {
            // Fallback: client-side interpolation
            const pop = interpolatePopulation(year);
            const populationFull = Math.round(pop * 1000000);
            resultPopEl.textContent = populationFull.toLocaleString('en-IN');
        });
});

// ============================================
// SCROLL ANIMATIONS (Intersection Observer)
// ============================================
const observerOptions = {
    threshold: 0.15,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
            // Stagger animation
            const delay = entry.target.dataset.delay || index * 80;
            setTimeout(() => {
                entry.target.classList.add('visible');
            }, delay);
        }
    });
}, observerOptions);

// Observe all animatable elements
document.querySelectorAll('.stat-card, .prediction-card, .state-card, .timeline-item').forEach(el => {
    observer.observe(el);
});

// ============================================
// ANIMATED STAT NUMBERS
// ============================================
function animateNumber(el, target, duration = 2000) {
    const isFloat = target % 1 !== 0;
    let start = 0;
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        // Ease out cubic
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = start + (target - start) * eased;

        if (isFloat) {
            el.textContent = current.toFixed(1);
        } else {
            el.textContent = Math.round(current).toLocaleString('en-IN');
        }

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

const statObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const numEl = entry.target.querySelector('.stat-number');
            const target = parseFloat(numEl.dataset.target);
            animateNumber(numEl, target);
            statObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.3 });

document.querySelectorAll('.stat-card').forEach(card => {
    statObserver.observe(card);
});

// ============================================
// NAVBAR SCROLL EFFECT
// ============================================
let lastScroll = 0;
window.addEventListener('scroll', () => {
    const navbar = document.getElementById('navbar');
    const scrollTop = window.scrollY;

    if (scrollTop > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }

    lastScroll = scrollTop;

    // Update active nav link
    const sections = ['hero', 'stats', 'chart-section', 'predictions', 'states'];
    let currentSection = 'hero';
    sections.forEach(id => {
        const section = document.getElementById(id);
        if (section) {
            const rect = section.getBoundingClientRect();
            if (rect.top <= 120) {
                currentSection = id;
            }
        }
    });

    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${currentSection}`) {
            link.classList.add('active');
        }
    });
});

// ============================================
// MOBILE NAV TOGGLE
// ============================================
const navToggle = document.getElementById('navToggle');
const navLinks = document.querySelector('.nav-links');

navToggle.addEventListener('click', () => {
    navLinks.classList.toggle('open');
});

// Close mobile nav on link click
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('open');
    });
});

// ============================================
// SMOOTH SCROLL FOR NAV LINKS
// ============================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
        e.preventDefault();
        const target = document.querySelector(anchor.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// ============================================
// INITIALIZE CHARTS ON DOM LOAD
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    createPopulationChart();
    createGrowthChart();
    createComparisonChart();
});

// ============================================
// PARTICLE EFFECT ON HERO (subtle)
// ============================================
(function createParticles() {
    const hero = document.getElementById('hero');
    if (!hero) return;

    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.style.cssText = `
            position: absolute;
            width: ${Math.random() * 4 + 2}px;
            height: ${Math.random() * 4 + 2}px;
            background: rgba(255, 107, 53, ${Math.random() * 0.3 + 0.1});
            border-radius: 50%;
            top: ${Math.random() * 100}%;
            left: ${Math.random() * 100}%;
            animation: floatParticle ${Math.random() * 10 + 10}s ease-in-out infinite;
            animation-delay: ${Math.random() * 5}s;
            pointer-events: none;
            z-index: 0;
        `;
        hero.style.position = 'relative';
        hero.appendChild(particle);
    }

    // Add particle animation keyframes
    const style = document.createElement('style');
    style.textContent = `
        @keyframes floatParticle {
            0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.3; }
            25% { transform: translate(${Math.random() * 100 - 50}px, ${Math.random() * 100 - 50}px) scale(1.5); opacity: 0.6; }
            50% { transform: translate(${Math.random() * 100 - 50}px, ${Math.random() * 100 - 50}px) scale(0.8); opacity: 0.2; }
            75% { transform: translate(${Math.random() * 100 - 50}px, ${Math.random() * 100 - 50}px) scale(1.2); opacity: 0.5; }
        }
    `;
    document.head.appendChild(style);
})();

console.log('🇮🇳 India Population Prediction App Loaded Successfully!');
