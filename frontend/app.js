const API_URL = window.location.hostname === 'localhost' ? 'http://localhost:8000' : '/api';
let allKeywords = [];
let filteredKeywords = [];
let keywordChart = null;

document.getElementById('analyzeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    await analyzeKeywords();
});

document.getElementById('competitorBtn').addEventListener('click', async () => {
    await analyzeCompetitors();
});

// Clear URL button functionality
document.getElementById('clearUrl').addEventListener('click', () => {
    const urlInput = document.getElementById('url');
    urlInput.value = '';
    urlInput.focus();
    toggleClearButton();
});

// Auto-format URL on input change
document.getElementById('url').addEventListener('blur', (e) => {
    const urlInput = e.target;
    const url = urlInput.value.trim();
    
    if (url && !url.startsWith('http://') && !url.startsWith('https://')) {
        urlInput.value = 'https://' + url;
    }
});

// Show/hide clear button based on input content
document.getElementById('url').addEventListener('input', toggleClearButton);

function toggleClearButton() {
    const urlInput = document.getElementById('url');
    const clearButton = document.getElementById('clearUrl');
    
    if (urlInput.value.trim()) {
        clearButton.style.opacity = '1';
        clearButton.style.pointerEvents = 'auto';
    } else {
        clearButton.style.opacity = '0';
        clearButton.style.pointerEvents = 'none';
    }
}

// Initialize clear button state
document.addEventListener('DOMContentLoaded', toggleClearButton);

// Set example URL function
function setExampleUrl(url) {
    const urlInput = document.getElementById('url');
    urlInput.value = url;
    urlInput.focus();
    toggleClearButton();
    
    // Auto-format the URL
    const normalizedUrl = normalizeUrl(url);
    urlInput.value = normalizedUrl;
}

function normalizeUrl(url) {
    url = url.trim();
    if (!url) return '';
    
    // Add https:// if no protocol is specified
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
        url = 'https://' + url;
    }
    
    return url;
}

async function analyzeKeywords() {
    const urlInput = document.getElementById('url');
    const regionInput = document.getElementById('region');
    
    const rawUrl = urlInput.value.trim();
    if (!rawUrl) {
        alert('Please enter a valid URL');
        urlInput.focus();
        return;
    }
    
    // Normalize the URL
    const normalizedUrl = normalizeUrl(rawUrl);
    urlInput.value = normalizedUrl;
    
    const formData = {
        url: normalizedUrl,
        region: regionInput.value,
        email: document.getElementById('email').value || null
    };
    
    console.log('Analyzing keywords with data:', formData);
    console.log('API URL:', API_URL);
    
    document.getElementById('loadingDiv').classList.remove('hidden');
    document.getElementById('resultsDiv').classList.add('hidden');
    document.getElementById('competitorResultsDiv').classList.add('hidden');
    document.getElementById('analyzeBtn').disabled = true;
    
    try {
        const response = await fetch(`${API_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('Server response:', errorText);
            throw new Error(`HTTP ${response.status}: ${errorText}`);
        }
        
        const data = await response.json();
        displayResults(data);
        
    } catch (error) {
        console.error('Error:', error);
        console.error('Response status:', error.status);
        console.error('Response text:', error.message);
        alert(`Error analyzing website: ${error.message}. Please check the URL and try again.`);
    } finally {
        document.getElementById('loadingDiv').classList.add('hidden');
        document.getElementById('analyzeBtn').disabled = false;
    }
}

async function analyzeCompetitors() {
    const urlInput = document.getElementById('url');
    const regionInput = document.getElementById('region');
    
    const rawUrl = urlInput.value.trim();
    if (!rawUrl) {
        alert('Please enter a valid URL');
        urlInput.focus();
        return;
    }
    
    // Normalize the URL
    const normalizedUrl = normalizeUrl(rawUrl);
    urlInput.value = normalizedUrl;
    
    const formData = {
        url: normalizedUrl,
        region: regionInput.value,
        email: document.getElementById('email').value || null
    };
    
    document.getElementById('loadingDiv').classList.remove('hidden');
    document.getElementById('resultsDiv').classList.add('hidden');
    document.getElementById('competitorResultsDiv').classList.add('hidden');
    document.getElementById('competitorBtn').disabled = true;
    
    try {
        const response = await fetch(`${API_URL}/analyze-competitors`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('Server response:', errorText);
            throw new Error(`HTTP ${response.status}: ${errorText}`);
        }
        
        const data = await response.json();
        displayCompetitorResults(data);
        
    } catch (error) {
        console.error('Error:', error);
        console.error('Response status:', error.status);
        console.error('Response text:', error.message);
        alert(`Error analyzing competitors: ${error.message}. Please check the URL and try again.`);
    } finally {
        document.getElementById('loadingDiv').classList.add('hidden');
        document.getElementById('competitorBtn').disabled = false;
    }
}

function displayResults(data) {
    allKeywords = data.keywords;
    filteredKeywords = allKeywords;
    
    document.getElementById('totalKeywords').textContent = data.keywords_found;
    document.getElementById('totalVolume').textContent = data.total_volume.toLocaleString();
    document.getElementById('avgCPC').textContent = `$${data.avg_cpc}`;
    
    renderKeywordsTable(filteredKeywords);
    renderChart();
    
    document.getElementById('resultsDiv').classList.remove('hidden');
}

function renderKeywordsTable(keywords) {
    const tbody = document.getElementById('keywordsTableBody');
    tbody.innerHTML = '';
    
    keywords.forEach(keyword => {
        const row = tbody.insertRow();
        const competitionColor = keyword.competition === 'High' ? 'red' : 
                                keyword.competition === 'Medium' ? 'yellow' : 'green';
        
        row.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${keyword.keyword}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-semibold">${keyword.volume ? keyword.volume.toLocaleString() : '-'}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-semibold">$${keyword.cpc || '0.00'}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-${competitionColor}-100 text-${competitionColor}-800">
                    ${keyword.competition || '-'}
                </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
                    ${keyword.type}
                </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-purple-100 text-purple-800">
                    ${keyword.intent}
                </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${keyword.trend || '-'}</td>
        `;
    });
}

function filterKeywords(type) {
    if (type === 'all') {
        filteredKeywords = allKeywords;
    } else {
        filteredKeywords = allKeywords.filter(k => k.type === type);
    }
    
    renderKeywordsTable(filteredKeywords);
    
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('bg-blue-600', 'text-white');
        btn.classList.add('bg-gray-200', 'text-gray-700');
    });
    
    event.target.classList.remove('bg-gray-200', 'text-gray-700');
    event.target.classList.add('bg-blue-600', 'text-white');
}

function renderChart() {
    const ctx = document.getElementById('keywordChart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (keywordChart) {
        keywordChart.destroy();
    }
    
    const typeCount = {};
    allKeywords.forEach(k => {
        typeCount[k.type] = (typeCount[k.type] || 0) + 1;
    });
    
    const labels = Object.keys(typeCount);
    const data = Object.values(typeCount);
    
    // Colors for different keyword types
    const colors = [
        'rgba(59, 130, 246, 0.8)',   // Blue for short-tail
        'rgba(16, 185, 129, 0.8)',   // Green for mid-tail  
        'rgba(251, 146, 60, 0.8)',   // Orange for long-tail
        'rgba(147, 51, 234, 0.8)',   // Purple for branded
        'rgba(239, 68, 68, 0.8)',    // Red for additional types
        'rgba(245, 158, 11, 0.8)'    // Yellow for additional types
    ];
    
    const borderColors = [
        'rgba(59, 130, 246, 1)',
        'rgba(16, 185, 129, 1)',
        'rgba(251, 146, 60, 1)',
        'rgba(147, 51, 234, 1)',
        'rgba(239, 68, 68, 1)',
        'rgba(245, 158, 11, 1)'
    ];
    
    keywordChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors.slice(0, labels.length),
                borderColor: borderColors.slice(0, labels.length),
                borderWidth: 2,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true,
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label;
                            const value = context.parsed;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${value} keywords (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

function displayCompetitorResults(data) {
    document.getElementById('competitorsFound').textContent = data.competitors_found;
    document.getElementById('keywordOpportunities').textContent = data.keyword_gaps.length;
    
    const avgTraffic = data.competitors.reduce((sum, comp) => sum + comp.estimated_traffic, 0) / data.competitors.length;
    document.getElementById('avgCompetitorTraffic').textContent = (avgTraffic / 1000000).toFixed(1) + 'M';
    
    // Render competitor cards
    const competitorList = document.getElementById('competitorList');
    competitorList.innerHTML = '';
    
    data.competitors.forEach(competitor => {
        const card = document.createElement('div');
        card.className = 'bg-white border border-gray-200 rounded-lg p-4';
        
        card.innerHTML = `
            <div class="flex justify-between items-start mb-3">
                <div>
                    <h5 class="text-lg font-semibold text-gray-800">${competitor.domain}</h5>
                    <p class="text-sm text-gray-600">Traffic: ${(competitor.estimated_traffic / 1000000).toFixed(1)}M/month</p>
                    <p class="text-sm text-gray-600">Domain Authority: ${competitor.domain_authority}</p>
                </div>
                <div class="text-right">
                    <p class="text-sm font-medium">Keywords: ${competitor.total_keywords}</p>
                    <p class="text-sm text-gray-600">Volume: ${competitor.total_volume.toLocaleString()}</p>
                    <p class="text-sm text-gray-600">Avg CPC: $${competitor.avg_cpc}</p>
                </div>
            </div>
            <div>
                <p class="text-xs text-gray-500 mb-2">Top Keywords:</p>
                <div class="flex flex-wrap gap-1">
                    ${competitor.top_keywords.slice(0, 5).map(kw => 
                        `<span class="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">${kw.keyword}</span>`
                    ).join('')}
                </div>
            </div>
        `;
        
        competitorList.appendChild(card);
    });
    
    // Render keyword gaps table
    const tbody = document.getElementById('keywordGapsTableBody');
    tbody.innerHTML = '';
    
    data.keyword_gaps.forEach(gap => {
        const row = tbody.insertRow();
        row.innerHTML = `
            <td class="px-4 py-2 text-sm font-medium text-gray-900">${gap.keyword}</td>
            <td class="px-4 py-2 text-sm text-gray-600">${gap.volume.toLocaleString()}</td>
            <td class="px-4 py-2 text-sm text-gray-600">$${gap.cpc}</td>
            <td class="px-4 py-2 text-sm">
                <span class="px-2 py-1 text-xs rounded-full ${gap.competition === 'High' ? 'bg-red-100 text-red-800' : 
                    gap.competition === 'Medium' ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800'}">
                    ${gap.competition}
                </span>
            </td>
            <td class="px-4 py-2 text-sm text-gray-600">${gap.competitor_domain}</td>
            <td class="px-4 py-2 text-sm font-semibold text-purple-600">${gap.opportunity_score}/10</td>
        `;
    });
    
    document.getElementById('competitorResultsDiv').classList.remove('hidden');
}

function exportCSV() {
    let csv = 'Keyword,Volume,CPC,Competition,Type,Intent,Trend\n';
    
    filteredKeywords.forEach(k => {
        csv += `"${k.keyword}","${k.volume || 0}","${k.cpc || 0}","${k.competition || ''}","${k.type}","${k.intent}","${k.trend || ''}"\n`;
    });
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'keywords_export.csv';
    a.click();
    window.URL.revokeObjectURL(url);
}