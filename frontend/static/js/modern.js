// modern.js - UI interaction enhancements

document.addEventListener('DOMContentLoaded', function(){
  // Platform toggles
  document.querySelectorAll('.platform-toggle').forEach(el => {
    el.addEventListener('click', function(e){
      const chk = this.querySelector('input[type=checkbox]');
      chk.checked = !chk.checked;
      this.classList.toggle('active', chk.checked);
    });
    el.addEventListener('keydown', function(e){ if(e.key==='Enter' || e.key===' ') { e.preventDefault(); this.click(); } });
  });

  // Character counters for any textarea with data-counter
  document.querySelectorAll('textarea').forEach(t => {
    if(!t.id) return;
    const counterId = t.id + 'Counter';
    const parent = t.parentElement;
    const counter = document.createElement('div');
    counter.style.textAlign='right'; counter.style.fontSize='12px'; counter.style.color='#6b7280';
    counter.id = counterId; counter.textContent = t.value.length + ' chars';
    parent.appendChild(counter);
    t.addEventListener('input', function(){ document.getElementById(counterId).textContent = this.value.length + ' chars'; });
  });

  // Copy and download buttons
  function copyTextFrom(id){
    const el = document.getElementById(id);
    if(!el) return showToast('Nothing to copy');
    const text = el.innerText || el.textContent;
    navigator.clipboard.writeText(text).then(()=> showToast('Copied to clipboard'));
  }
  function downloadTextFrom(id, filename){
    const el = document.getElementById(id);
    if(!el) return showToast('Nothing to export');
    const text = el.innerText || el.textContent;
    const blob = new Blob([text], {type:'text/plain;charset=utf-8'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = filename; document.body.appendChild(a); a.click(); a.remove();
    URL.revokeObjectURL(a.href);
    showToast('Export started');
  }

  // Attach copy/export handlers
  const copyCampaign = document.getElementById('copyCampaign');
  if(copyCampaign) copyCampaign.addEventListener('click', ()=> copyTextFrom('campaignOutput'));
  const downloadCampaign = document.getElementById('downloadCampaign');
  if(downloadCampaign) downloadCampaign.addEventListener('click', ()=> downloadTextFrom('campaignOutput','campaign.txt'));

  const copyPitch = document.getElementById('copyPitch');
  if(copyPitch) copyPitch.addEventListener('click', ()=> copyTextFrom('pitchOutput'));
  const downloadPitch = document.getElementById('downloadPitch');
  if(downloadPitch) downloadPitch.addEventListener('click', ()=> downloadTextFrom('pitchOutput','pitch.txt'));

  const copyLead = document.getElementById('copyLead');
  if(copyLead) copyLead.addEventListener('click', ()=> copyTextFrom('leadOutput'));
  const downloadLead = document.getElementById('downloadLead');
  if(downloadLead) downloadLead.addEventListener('click', ()=> downloadTextFrom('leadOutput','lead-analysis.txt'));

  // Toast utility
  function showToast(message){
    let t = document.querySelector('.toast');
    if(!t){ t = document.createElement('div'); t.className='toast'; document.body.appendChild(t); }
    t.textContent = message; t.classList.add('show'); setTimeout(()=> t.classList.remove('show'), 3500);
  }

  // Parse numeric score from text and update gauge
  function updateGaugeFromText(text){
    const m = text.match(/(\d{1,3})\s*\/?\s*100|(\d{1,3})(?!.*%)/);
    let num = null;
    if(m){
      num = m[1] ? parseInt(m[1]) : (m[2] ? parseInt(m[2]) : null);
    }
    if(num===null){
      // try percent
      const p = text.match(/(\d{1,3})%/);
      if(p) num = parseInt(p[1]);
    }
    if(num===null) return;
    num = Math.max(0, Math.min(100, num));
    const gauge = document.getElementById('leadGauge');
    const valueEl = document.getElementById('leadScoreValue');
    if(gauge && valueEl){
      valueEl.textContent = num;
      // set background gradient based on score
      const pct = num;
      let color = 'linear-gradient(90deg, #06b6d4, #7c3aed)';
      if(pct>=90) color = 'linear-gradient(90deg, #06b6d4, #10b981)';
      else if(pct>=75) color = 'linear-gradient(90deg, #7c3aed, #5b21b6)';
      else if(pct>=60) color = 'linear-gradient(90deg, #f59e0b, #ffb86b)';
      else color = 'linear-gradient(90deg, #ef4444, #f97316)';
      gauge.style.background = color;
    }
  }

  // Listen for successful AJAX responses to update gauge
  // We will monkey-patch fetch to intercept responses from /api/score-lead and update UI
  const originalFetch = window.fetch;
  window.fetch = async function(resource, init){
    const res = await originalFetch(resource, init);
    try{
      if(resource && resource.toString().includes('/api/score-lead')){
        const clone = res.clone();
        const data = await clone.json();
        if(data && data.result){ updateGaugeFromText(data.result); }
      }
      if(resource && resource.toString().includes('/api/generate-campaign')){
        const clone = res.clone();
        const data = await clone.json();
        if(data && data.result){ showToast('Campaign generated'); }
      }
    }catch(e){ console.warn('modern.js fetch hook error', e); }
    return res;
  };

});
// Dark mode toggle handling (outside DOMContent to ensure functions are available)
document.addEventListener('DOMContentLoaded', function(){
  const toggle = document.getElementById('colorModeToggle');
  const root = document.documentElement;
  function applyDark(dark){
    if(dark){ document.documentElement.classList.add('dark'); toggle.textContent='Light'; toggle.setAttribute('aria-pressed','true'); }
    else { document.documentElement.classList.remove('dark'); toggle.textContent='Dark'; toggle.setAttribute('aria-pressed','false'); }
  }
  // init from localStorage
  const stored = localStorage.getItem('marketai_dark');
  applyDark(stored === '1');
  if(toggle){
    toggle.addEventListener('click', ()=>{ const isDark = document.documentElement.classList.toggle('dark'); applyDark(isDark); localStorage.setItem('marketai_dark', isDark ? '1' : '0'); });
  }
});
