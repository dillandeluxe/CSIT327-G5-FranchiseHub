// ==========================================================================
// FranchiseHub Interactive Showcase Engine
// Author: Dillan Ycoy & CSIT327 Group 5
// ==========================================================================

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
    description: "Specialty espresso kiosk concept serving premium Arabica blends, iced cold brews, and fresh artisan pastries with high daily foot traffic margins."
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
    description: "Multi-brand ghost kitchen optimized for GrabFood & Foodpanda delivery. Low overhead, integrated inventory POS, and high order volumes."
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
    description: "Automated keycard-access neighborhood fitness center with commercial-grade strength machines, cardio zones, and recurring membership model."
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
    description: "Trendy Taiwanese boba and fruit tea franchise featuring signature brown sugar pearls, taro cream smoothies, and vibrant aesthetic packaging."
  },
  {
    id: 5,
    name: "TechFix Mobile & Laptop Hub",
    category: "Services & Tech",
    location: "Metro Manila & Cavite Malls",
    investmentMin: 300000,
    investmentMax: 600000,
    royalty: "Zero Royalty 1st Year",
    term: "5 Years",
    floorArea: "12 - 25 sqm",
    roi: "10 - 15 Months",
    image: "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=700&q=80",
    description: "Certified express electronics diagnostics, screen replacement, battery renewal, and mobile accessory retail store with certified technician supply chain."
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
    description: "Farm-to-shelf specialty grocery offering fresh farm produce, organic health pantry essentials, eco-friendly goods, and cold-pressed botanical juices."
  }
];

// Application State
const state = {
  currentView: 'landing',
  searchQuery: '',
  selectedCategory: 'all',
  maxInvestment: 'all',
  favorites: new Set([1, 3]),
  applied: new Map([
    [1, {
      proposedLocation: "Cebu IT Park, Lahug",
      capital: "₱650,000",
      submittedDate: "Sep 24, 2026",
      status: "Under Review"
    }]
  ])
};

// DOM Elements
const views = document.querySelectorAll('.view-panel');
const roleButtons = document.querySelectorAll('.role-btn');
const navButtons = document.querySelectorAll('.nav-link');
const userRoleIndicator = document.getElementById('userRoleIndicator');
const toastEl = document.getElementById('demoToast');
const modal = document.getElementById('detailModal');
const modalContent = document.getElementById('modalContent');
const modalClose = document.getElementById('modalCloseBtn');

const navFavCount = document.getElementById('navFavCount');
const roleFavCount = document.getElementById('roleFavCount');
const navAppCount = document.getElementById('navAppCount');
const roleAppCount = document.getElementById('roleAppCount');

// Helpers
function formatPeso(val) {
  return '₱' + Number(val).toLocaleString();
}

function showToast(msg) {
  if (!toastEl) return;
  toastEl.textContent = msg;
  toastEl.hidden = false;
  clearTimeout(showToast.timer);
  showToast.timer = setTimeout(() => {
    toastEl.hidden = true;
  }, 3200);
}

function updateBadgeCounts() {
  const favCount = state.favorites.size;
  const appCount = state.applied.size;
  if (navFavCount) navFavCount.textContent = favCount;
  if (roleFavCount) roleFavCount.textContent = favCount;
  if (navAppCount) navAppCount.textContent = appCount;
  if (roleAppCount) roleAppCount.textContent = appCount;
}

// Master View Switcher
window.switchView = function(viewName) {
  state.currentView = viewName;

  // Toggle active view panel
  views.forEach(v => {
    v.classList.remove('active');
    if (v.id === `view-${viewName}`) {
      v.classList.add('active');
    }
  });

  // Sync role switcher buttons
  roleButtons.forEach(btn => {
    btn.classList.toggle('active', btn.dataset.targetView === viewName);
  });

  // Sync navbar links
  navButtons.forEach(btn => {
    btn.classList.toggle('active', btn.dataset.nav === viewName);
  });

  // Update role pill indicator
  if (userRoleIndicator) {
    if (viewName === 'landing') {
      userRoleIndicator.textContent = "Public Visitor";
    } else if (viewName === 'franchisor') {
      userRoleIndicator.textContent = "Franchisor: Kape Isla Corp.";
    } else if (viewName === 'admin') {
      userRoleIndicator.textContent = "Platform Admin: Superuser";
    } else {
      userRoleIndicator.textContent = "Franchisee: Dillan Y.";
    }
  }

  // Trigger view-specific re-renders
  if (viewName === 'favorites') {
    renderFavorites();
  } else if (viewName === 'applications') {
    renderApplications();
  } else if (viewName === 'browse') {
    renderFranchises();
  }

  window.scrollTo({ top: 0, behavior: 'smooth' });
};

// Toggle Favorite Heart
window.toggleFav = function(id, e) {
  if (e) e.stopPropagation();
  if (state.favorites.has(id)) {
    state.favorites.delete(id);
    showToast("Removed from favorites");
  } else {
    state.favorites.add(id);
    showToast("Saved to your favorites ❤️");
  }
  updateBadgeCounts();
  if (state.currentView === 'favorites') {
    renderFavorites();
  } else {
    renderFranchises();
  }
};

// Render Franchise Cards in Browse View
function renderFranchises() {
  const grid = document.getElementById('franchiseGrid');
  const visibleCountEl = document.getElementById('visibleCount');
  if (!grid) return;

  const filtered = FRANCHISES.filter(f => {
    const matchesSearch = !state.searchQuery || 
      f.name.toLowerCase().includes(state.searchQuery.toLowerCase()) ||
      f.location.toLowerCase().includes(state.searchQuery.toLowerCase()) ||
      f.description.toLowerCase().includes(state.searchQuery.toLowerCase());

    const matchesCat = state.selectedCategory === 'all' || f.category === state.selectedCategory;

    let matchesInv = true;
    if (state.maxInvestment !== 'all') {
      matchesInv = f.investmentMin <= Number(state.maxInvestment);
    }

    return matchesSearch && matchesCat && matchesInv;
  });

  if (visibleCountEl) visibleCountEl.textContent = filtered.length;

  if (filtered.length === 0) {
    grid.innerHTML = `
      <div class="empty-state" style="grid-column: 1 / -1;">
        <h3 class="empty-title">No franchise opportunities match your criteria</h3>
        <p class="empty-subtitle">Try adjusting your filters, location, or search keywords.</p>
        <button class="btn-clear-filters" onclick="resetFilters()" style="width: auto; padding: 10px 24px;">Reset Filters</button>
      </div>
    `;
    return;
  }

  grid.innerHTML = filtered.map(f => {
    const isFav = state.favorites.has(f.id);
    const isApplied = state.applied.has(f.id);

    return `
      <article class="franchise-card" onclick="openDetails(${f.id})">
        <div class="card-img-wrap">
          <img src="${f.image}" alt="${f.name}" class="card-img" loading="lazy" />
          <button class="card-fav-btn ${isFav ? 'active' : ''}" onclick="toggleFav(${f.id}, event)" title="${isFav ? 'Remove favorite' : 'Save favorite'}">
            <svg viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd"/>
            </svg>
          </button>
          ${isApplied ? `<span class="card-badge-applied">✓ Applied</span>` : ''}
        </div>
        <div class="card-body">
          <span class="card-cat-badge">${f.category}</span>
          <h3 class="card-title">${f.name}</h3>
          <p class="card-location">📍 ${f.location}</p>
          <p class="card-desc">${f.description}</p>
          <div class="card-footer">
            <div>
              <div class="investment-tag">Est. Investment</div>
              <div class="investment-val">${formatPeso(f.investmentMin)} - ${formatPeso(f.investmentMax)}</div>
            </div>
            <button class="btn-details" onclick="openDetails(${f.id})">Details ↗</button>
          </div>
        </div>
      </article>
    `;
  }).join('');
}

// Render Saved Favorites View
function renderFavorites() {
  const favGrid = document.getElementById('favoritesGrid');
  if (!favGrid) return;

  const favList = FRANCHISES.filter(f => state.favorites.has(f.id));

  if (favList.length === 0) {
    favGrid.innerHTML = `
      <div class="empty-state" style="grid-column: 1 / -1;">
        <div class="empty-icon" style="margin: 0 auto 16px;">
          <svg width="64" height="64" fill="currentColor" viewBox="0 0 20 20" style="color: #cbd5e1;">
            <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd"/>
          </svg>
        </div>
        <h3 class="empty-title">You haven't saved any favorites yet</h3>
        <p class="empty-subtitle">Browse verified franchises and click the heart icon on any opportunity to save it here.</p>
        <button class="btn-details" onclick="switchView('browse')" style="padding: 12px 28px; font-size: 0.95rem;">Browse Opportunities ↗</button>
      </div>
    `;
    return;
  }

  favGrid.innerHTML = favList.map(f => {
    const isApplied = state.applied.has(f.id);
    return `
      <article class="franchise-card" onclick="openDetails(${f.id})">
        <div class="card-img-wrap">
          <img src="${f.image}" alt="${f.name}" class="card-img" loading="lazy" />
          <button class="card-fav-btn active" onclick="toggleFav(${f.id}, event)" title="Remove from favorites">
            <svg viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd"/>
            </svg>
          </button>
          ${isApplied ? `<span class="card-badge-applied">✓ Applied</span>` : ''}
        </div>
        <div class="card-body">
          <span class="card-cat-badge">${f.category}</span>
          <h3 class="card-title">${f.name}</h3>
          <p class="card-location">📍 ${f.location}</p>
          <p class="card-desc">${f.description}</p>
          <div class="card-footer">
            <div>
              <div class="investment-tag">Est. Investment</div>
              <div class="investment-val">${formatPeso(f.investmentMin)} - ${formatPeso(f.investmentMax)}</div>
            </div>
            <button class="btn-details" onclick="openDetails(${f.id})">Details ↗</button>
          </div>
        </div>
      </article>
    `;
  }).join('');
}

// Render Applications View
function renderApplications() {
  const container = document.getElementById('applicationsContainer');
  if (!container) return;

  if (state.applied.size === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <h3 class="empty-title">No franchise applications submitted yet</h3>
        <p class="empty-subtitle">When you apply for a franchise opportunity, you can track your dossier status and franchisor review here.</p>
        <button class="btn-details" onclick="switchView('browse')" style="padding: 12px 28px; font-size: 0.95rem;">Explore Franchises ↗</button>
      </div>
    `;
    return;
  }

  let html = '';
  state.applied.forEach((app, id) => {
    const f = FRANCHISES.find(item => item.id === id);
    if (!f) return;

    html += `
      <div class="app-card">
        <div class="app-info-group">
          <img src="${f.image}" alt="${f.name}" class="app-thumb" />
          <div>
            <h3 class="app-title">${f.name}</h3>
            <div class="app-meta">
              <span>📍 ${app.proposedLocation}</span>
              <span>💰 Capital: <strong>${app.capital}</strong></span>
              <span>📅 Submitted: ${app.submittedDate}</span>
            </div>
          </div>
        </div>
        <div>
          <span class="app-status-badge badge-review">
            ⏳ ${app.status}
          </span>
        </div>
        <div class="app-timeline">
          <div class="timeline-step completed">
            <div class="timeline-dot">✓</div>
            <div class="timeline-label">Application Ingest</div>
          </div>
          <div class="timeline-step current">
            <div class="timeline-dot">2</div>
            <div class="timeline-label">Document Audit</div>
          </div>
          <div class="timeline-step">
            <div class="timeline-dot">3</div>
            <div class="timeline-label">Franchisor Interview</div>
          </div>
          <div class="timeline-step">
            <div class="timeline-dot">4</div>
            <div class="timeline-label">Agreement &amp; Launch</div>
          </div>
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
}

// Open Franchise Detail & Apply Modal
window.openDetails = function(id) {
  const f = FRANCHISES.find(item => item.id === id);
  if (!f || !modalContent) return;

  const isApplied = state.applied.has(f.id);

  modalContent.innerHTML = `
    <img src="${f.image}" alt="${f.name}" class="modal-img" />
    <span class="card-cat-badge">${f.category}</span>
    <h2 style="font-size: 1.6rem; font-weight: 700; margin: 4px 0 8px;">${f.name}</h2>
    <p style="color: var(--text-muted); font-size: 0.88rem; margin-bottom: 12px;">📍 Expansion Markets: <strong>${f.location}</strong></p>
    <p style="font-size: 0.88rem; color: #374151; line-height: 1.6; margin-bottom: 16px;">${f.description}</p>

    <div class="modal-specs-grid">
      <div class="spec-cell">
        <small>Investment Range</small>
        <strong>${formatPeso(f.investmentMin)} - ${formatPeso(f.investmentMax)}</strong>
      </div>
      <div class="spec-cell">
        <small>Royalty Fee</small>
        <strong>${f.royalty}</strong>
      </div>
      <div class="spec-cell">
        <small>Franchise Term</small>
        <strong>${f.term}</strong>
      </div>
      <div class="spec-cell">
        <small>Floor Space Required</small>
        <strong>${f.floorArea}</strong>
      </div>
      <div class="spec-cell" style="grid-column: 1 / -1;">
        <small>Estimated Breakeven / ROI</small>
        <strong style="color: #16a34a;">${f.roi} (Audited Supabase Model)</strong>
      </div>
    </div>

    ${isApplied ? `
      <div style="background: #ecfdf5; border: 1px solid #a7f3d0; color: #065f46; padding: 16px; border-radius: 10px; text-align: center; font-weight: 600; font-size: 0.9rem;">
        ✓ Your application for ${f.name} is currently under evaluation by the franchisor!
      </div>
    ` : `
      <form onsubmit="handleApplySubmit(event, ${f.id})">
        <div style="margin-bottom: 12px;">
          <label style="font-size: 0.8rem; font-weight: 600; display: block; margin-bottom: 4px;">Target Location Proposal:</label>
          <input type="text" id="targetLocInput" required placeholder="e.g. SM Seaside Cebu / BGC High Street" style="width: 100%; padding: 10px 12px; border: 1px solid var(--border); border-radius: 8px; font-family: inherit; font-size: 0.88rem;" />
        </div>
        <div style="margin-bottom: 16px;">
          <label style="font-size: 0.8rem; font-weight: 600; display: block; margin-bottom: 4px;">Verified Liquid Capital:</label>
          <select id="capitalInput" style="width: 100%; padding: 10px 12px; border: 1px solid var(--border); border-radius: 8px; font-family: inherit; font-size: 0.88rem;">
            <option>₱500,000 - ₱1,000,000 (Bank Guarantee)</option>
            <option>₱1,000,000 - ₱2,500,000 (Liquid Assets)</option>
            <option>₱2,500,000+ (Corporate Backed)</option>
          </select>
        </div>
        <button type="submit" class="btn-submit-apply">Submit Franchisee Application 📄</button>
      </form>
    `}
  `;

  modal.hidden = false;
};

// Handle Application Submit
window.handleApplySubmit = function(e, id) {
  e.preventDefault();
  const loc = document.getElementById('targetLocInput')?.value || "Metro Manila Branch";
  const cap = document.getElementById('capitalInput')?.value?.split(' ')[0] || "₱500,000";

  state.applied.set(id, {
    proposedLocation: loc,
    capital: cap,
    submittedDate: "Just now",
    status: "Under Review"
  });

  updateBadgeCounts();
  showToast("Application submitted successfully to Franchisor! 🚀");
  openDetails(id);
  renderFranchises();
};

// Modal Dismiss
if (modalClose) {
  modalClose.addEventListener('click', () => { modal.hidden = true; });
}
if (modal) {
  modal.addEventListener('click', (e) => {
    if (e.target === modal) modal.hidden = true;
  });
}
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && modal && !modal.hidden) modal.hidden = true;
});

// Top Role Buttons
roleButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    const target = btn.dataset.targetView;
    if (target) switchView(target);
  });
});

// Filters Setup
const searchInput = document.getElementById('searchInput');
const maxInvestmentSelect = document.getElementById('maxInvestment');
const clearBtn = document.getElementById('clearFiltersBtn');
const categoryRadios = document.querySelectorAll('input[name="category"]');

if (searchInput) {
  searchInput.addEventListener('input', (e) => {
    state.searchQuery = e.target.value.trim();
    renderFranchises();
  });
}

if (categoryRadios) {
  categoryRadios.forEach(r => {
    r.addEventListener('change', (e) => {
      state.selectedCategory = e.target.value;
      renderFranchises();
    });
  });
}

if (maxInvestmentSelect) {
  maxInvestmentSelect.addEventListener('change', (e) => {
    state.maxInvestment = e.target.value;
    renderFranchises();
  });
}

window.resetFilters = function() {
  state.searchQuery = '';
  state.selectedCategory = 'all';
  state.maxInvestment = 'all';
  if (searchInput) searchInput.value = '';
  if (maxInvestmentSelect) maxInvestmentSelect.value = 'all';
  const allRadio = document.querySelector('input[name="category"][value="all"]');
  if (allRadio) allRadio.checked = true;
  renderFranchises();
  showToast("Filters reset to default");
};

if (clearBtn) clearBtn.addEventListener('click', resetFilters);

// Boot
updateBadgeCounts();
renderFranchises();
