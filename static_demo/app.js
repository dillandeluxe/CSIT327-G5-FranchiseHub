// FranchiseHub Demo Data
const FRANCHISES = [
  {
    id: 1,
    name: "Coffee Corner PH",
    category: "Food & Beverage",
    location: "Metro Manila, Cebu, Davao",
    investmentMin: 250000,
    investmentMax: 500000,
    royalty: "4% of gross sales",
    term: "5 Years (Renewable)",
    floorArea: "15 - 35 sqm (Kiosk / In-line)",
    roi: "10 - 14 Months",
    image: "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?auto=format&fit=crop&w=700&q=80",
    description: "Specialty espresso kiosk concept serving premium Arabica blends, iced cold brews, and fresh artisan pastries with high daily foot traffic margins.",
    favorited: true
  },
  {
    id: 2,
    name: "CloudKitchen Express",
    category: "Food & Beverage",
    location: "Nationwide (Urban Centers)",
    investmentMin: 400000,
    investmentMax: 750000,
    royalty: "5% of delivery sales",
    term: "3 Years",
    floorArea: "25 - 40 sqm (Delivery Hub)",
    roi: "8 - 12 Months",
    image: "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=700&q=80",
    description: "Multi-brand ghost kitchen optimized for GrabFood & Foodpanda delivery. Low overhead, integrated inventory POS, and high order volumes.",
    favorited: false
  },
  {
    id: 3,
    name: "MetroFit 24/7 Gym",
    category: "Health & Fitness",
    location: "Quezon City, Makati, Pasig",
    investmentMin: 1200000,
    investmentMax: 2500000,
    royalty: "₱25,000 / month flat",
    term: "7 Years",
    floorArea: "180 - 350 sqm",
    roi: "18 - 24 Months",
    image: "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=700&q=80",
    description: "Automated keycard-access neighborhood fitness center with commercial-grade strength machines, cardio zones, and recurring membership model.",
    favorited: true
  },
  {
    id: 4,
    name: "Boba Bliss Milk Tea Bar",
    category: "Food & Beverage",
    location: "Cebu City, Iloilo, Bacolod",
    investmentMin: 180000,
    investmentMax: 350000,
    royalty: "3% monthly",
    term: "3 Years",
    floorArea: "10 - 20 sqm",
    roi: "6 - 9 Months",
    image: "https://images.unsplash.com/photo-1558857563-b37cf5a84094?auto=format&fit=crop&w=700&q=80",
    description: "Trendy Taiwanese boba and fruit tea franchise featuring signature brown sugar pearls, taro cream smoothies, and vibrant aesthetic packaging.",
    favorited: false
  },
  {
    id: 5,
    name: "TechFix Mobile & Laptop Hub",
    category: "Services & Tech",
    location: "Metro Manila & Cavite Malls",
    investmentMin: 300000,
    investmentMax: 600000,
    royalty: "Zero Royalty for 1st Year",
    term: "5 Years",
    floorArea: "12 - 25 sqm",
    roi: "10 - 15 Months",
    image: "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=700&q=80",
    description: "Certified express electronics diagnostics, screen replacement, battery renewal, and mobile accessory retail store with certified technician supply chain.",
    favorited: false
  },
  {
    id: 6,
    name: "GreenLeaf Organic Mart",
    category: "Retail",
    location: "Alabang, BGC, Ortigas",
    investmentMin: 500000,
    investmentMax: 1000000,
    royalty: "4% of net revenues",
    term: "5 Years",
    floorArea: "40 - 75 sqm",
    roi: "14 - 18 Months",
    image: "https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=700&q=80",
    description: "Farm-to-shelf specialty grocery offering fresh farm produce, organic health pantry essentials, eco-friendly goods, and cold-pressed botanical juices.",
    favorited: false
  }
];

// App State
let state = {
  currentRole: 'franchisee',
  searchQuery: '',
  selectedCategory: 'all',
  maxInvestment: 'all',
  favorites: new Set([1, 3]),
  applied: new Set([1])
};

// DOM References
const grid = document.getElementById('franchiseGrid');
const visibleCountEl = document.getElementById('visibleCount');
const favCountEl = document.getElementById('favCount');
const appCountEl = document.getElementById('appCount');
const searchInput = document.getElementById('searchInput');
const maxInvestmentSelect = document.getElementById('maxInvestment');
const clearBtn = document.getElementById('clearFiltersBtn');
const categoryRadios = document.querySelectorAll('input[name="category"]');
const roleButtons = document.querySelectorAll('.role-btn');
const viewPanels = document.querySelectorAll('.view-panel');
const userRoleIndicator = document.getElementById('userRoleIndicator');
const modal = document.getElementById('detailModal');
const modalContent = document.getElementById('modalContent');
const modalClose = document.getElementById('modalCloseBtn');
const toast = document.getElementById('demoToast');

// Helpers
function formatPeso(val) {
  return '₱' + Number(val).toLocaleString();
}

function showToast(msg) {
  toast.textContent = msg;
  toast.hidden = false;
  setTimeout(() => {
    toast.hidden = true;
  }, 3200);
}

// Render Franchises
function renderFranchises() {
  const filtered = FRANCHISES.filter(f => {
    // Search filter
    const matchesSearch = !state.searchQuery || 
      f.name.toLowerCase().includes(state.searchQuery.toLowerCase()) ||
      f.location.toLowerCase().includes(state.searchQuery.toLowerCase()) ||
      f.description.toLowerCase().includes(state.searchQuery.toLowerCase());

    // Category filter
    const matchesCat = state.selectedCategory === 'all' || f.category === state.selectedCategory;

    // Investment filter
    let matchesInv = true;
    if (state.maxInvestment !== 'all') {
      matchesInv = f.investmentMin <= Number(state.maxInvestment);
    }

    return matchesSearch && matchesCat && matchesInv;
  });

  visibleCountEl.textContent = filtered.length;

  if (filtered.length === 0) {
    grid.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 48px; background: white; border-radius: 16px; border: 1px dashed var(--border);">
        <h3 style="font-size: 1.1rem; color: var(--text); margin-bottom: 8px;">No matching opportunities found</h3>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 16px;">Try adjusting your search criteria or resetting filters.</p>
        <button onclick="resetFilters()" style="padding: 8px 16px; background: var(--primary); color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;">Reset All Filters</button>
      </div>
    `;
    return;
  }

  grid.innerHTML = filtered.map(f => {
    const isFav = state.favorites.has(f.id);
    const isApplied = state.applied.has(f.id);

    return `
      <article class="franchise-card" data-id="${f.id}">
        <div class="card-img-wrap">
          <img src="${f.image}" alt="${f.name}" loading="lazy" />
          <button class="card-fav-btn ${isFav ? 'favorited' : ''}" onclick="toggleFav(${f.id}, event)" title="${isFav ? 'Remove from favorites' : 'Add to favorites'}">
            <svg width="18" height="18" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd"/>
            </svg>
          </button>
          ${isApplied ? `<span style="position:absolute; bottom:12px; left:12px; background:#10b981; color:white; font-size:0.7rem; font-weight:700; padding:3px 8px; border-radius:6px;">✓ Applied</span>` : ''}
        </div>
        <div class="card-body">
          <span class="card-cat-badge">${f.category}</span>
          <h3 class="card-title">${f.name}</h3>
          <p class="card-loc">📍 ${f.location}</p>
          <p class="card-desc">${f.description}</p>
          <div class="card-meta-row">
            <div class="meta-col">
              <small>Est. Investment</small>
              <div class="meta-val">${formatPeso(f.investmentMin)} - ${formatPeso(f.investmentMax)}</div>
            </div>
            <button class="btn-card-details" onclick="openDetails(${f.id})">Details ↗</button>
          </div>
        </div>
      </article>
    `;
  }).join('');
}

// Toggle Favorite
window.toggleFav = function(id, e) {
  e.stopPropagation();
  if (state.favorites.has(id)) {
    state.favorites.delete(id);
    showToast("Removed from favorites");
  } else {
    state.favorites.add(id);
    showToast("Saved to your favorites ❤️");
  }
  favCountEl.textContent = state.favorites.size;
  renderFranchises();
};

// Open Detail Modal
window.openDetails = function(id) {
  const f = FRANCHISES.find(item => item.id === id);
  if (!f) return;

  const isApplied = state.applied.has(f.id);

  modalContent.innerHTML = `
    <img src="${f.image}" alt="${f.name}" class="modal-img" />
    <span class="card-cat-badge">${f.category}</span>
    <h2 class="modal-title">${f.name}</h2>
    <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 12px;">📍 Locations: <strong>${f.location}</strong></p>
    <p style="font-size: 0.88rem; color: var(--text); line-height: 1.6;">${f.description}</p>

    <div class="modal-grid-specs">
      <div class="spec-item">
        <small>Investment Range</small>
        <strong>${formatPeso(f.investmentMin)} - ${formatPeso(f.investmentMax)}</strong>
      </div>
      <div class="spec-item">
        <small>Royalty Fee</small>
        <strong>${f.royalty}</strong>
      </div>
      <div class="spec-item">
        <small>Franchise Term</small>
        <strong>${f.term}</strong>
      </div>
      <div class="spec-item">
        <small>Required Floor Area</small>
        <strong>${f.floorArea}</strong>
      </div>
      <div class="spec-item" style="grid-column: 1 / -1;">
        <small>Estimated ROI Timeline</small>
        <strong style="color: #16a34a;">${f.roi} based on vetted audited models</strong>
      </div>
    </div>

    ${isApplied ? `
      <div style="background: #ecfdf5; border: 1px solid #a7f3d0; color: #065f46; padding: 14px; border-radius: 10px; text-align: center; font-weight: 600; font-size: 0.9rem;">
        ✓ Your application for ${f.name} has been submitted to the franchisor! Status: <strong>Under Document Verification</strong>.
      </div>
    ` : `
      <form onsubmit="handleApplySubmit(event, ${f.id})">
        <div style="margin-bottom: 12px;">
          <label style="font-size: 0.8rem; font-weight: 600; display: block; margin-bottom: 4px;">Proposed Target Location / Mall:</label>
          <input type="text" required placeholder="e.g. SM Mall of Asia / Ayala Center Cebu" style="width: 100%; padding: 10px; border: 1px solid var(--border); border-radius: 8px; font-family: inherit;" />
        </div>
        <div style="margin-bottom: 16px;">
          <label style="font-size: 0.8rem; font-weight: 600; display: block; margin-bottom: 4px;">Verified Liquid Capital Available:</label>
          <select style="width: 100%; padding: 10px; border: 1px solid var(--border); border-radius: 8px; font-family: inherit;">
            <option>₱500,000 - ₱1,000,000</option>
            <option>₱1,000,000 - ₱2,500,000</option>
            <option>₱2,500,000+</option>
          </select>
        </div>
        <button type="submit" class="btn-submit-apply">Submit Franchisee Application 📄</button>
      </form>
    `}
  `;

  modal.hidden = false;
};

window.handleApplySubmit = function(e, id) {
  e.preventDefault();
  state.applied.add(id);
  appCountEl.textContent = state.applied.size;
  showToast("Application submitted successfully to Franchisor! 🚀");
  openDetails(id);
  renderFranchises();
};

modalClose.addEventListener('click', (e) => {
  e.preventDefault();
  e.stopPropagation();
  modal.hidden = true;
});

modal.addEventListener('click', (e) => {
  if (e.target === modal) modal.hidden = true;
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && !modal.hidden) {
    modal.hidden = true;
  }
});

// Role Switcher
roleButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    roleButtons.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const role = btn.dataset.role;
    state.currentRole = role;

    viewPanels.forEach(panel => {
      panel.classList.remove('active');
    });

    const activePanel = document.getElementById(`view-${role}`);
    if (activePanel) activePanel.classList.add('active');

    if (role === 'franchisee') {
      userRoleIndicator.textContent = "Franchisee: Dillan Y.";
      showToast("Switched to Franchisee Explorer mode");
    } else if (role === 'franchisor') {
      userRoleIndicator.textContent = "Franchisor: Kape Isla Corp.";
      showToast("Switched to Franchisor Partner Portal");
    } else {
      userRoleIndicator.textContent = "Platform Admin: Superuser";
      showToast("Switched to System Administration Panel");
    }
  });
});

// Filter Event Listeners
searchInput.addEventListener('input', (e) => {
  state.searchQuery = e.target.value.trim();
  renderFranchises();
});

categoryRadios.forEach(radio => {
  radio.addEventListener('change', (e) => {
    state.selectedCategory = e.target.value;
    renderFranchises();
  });
});

maxInvestmentSelect.addEventListener('change', (e) => {
  state.maxInvestment = e.target.value;
  renderFranchises();
});

window.resetFilters = function() {
  state.searchQuery = '';
  state.selectedCategory = 'all';
  state.maxInvestment = 'all';
  searchInput.value = '';
  maxInvestmentSelect.value = 'all';
  document.querySelector('input[name="category"][value="all"]').checked = true;
  renderFranchises();
  showToast("Filters reset to default");
};

clearBtn.addEventListener('click', resetFilters);

// Initial Render
renderFranchises();
