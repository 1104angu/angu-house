/* 角色卡頁：從安谷的 Google 試算表讀卡片清單。
   ▼ 把試算表「發布到網路」拿到的 CSV 網址貼在下面引號裡（只要貼一次）。 */
window.CARDS_SHEET = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTzhg8zmTb06tJ3RzMnSZ3a-fRKUF_ijFfGYWxs-95QBPNdYFtystnowLxLuuY-d6FC0Vec8pDiGp-T/pub?gid=0&single=true&output=csv";

/* 試算表第一列是欄位名稱，順序隨意：
   上架｜卡名｜封面｜連結｜分類｜簡介
   上架：打勾才會出現（沒有這欄就全部顯示）
   封面：圖片網址；連結：CAVEDUCK 卡片網址（會自動補推薦碼、跟著語言切換）
   分類：可以填好幾個，用「、」或逗號隔開 */
(function(){
  const RC='ku1A1yGuNy';
  function parseCSV(text){const rows=[];let row=[],f='',q=false;
    for(let i=0;i<text.length;i++){const c=text[i];
      if(q){if(c==='"'){if(text[i+1]==='"'){f+='"';i++;}else q=false;}else f+=c;}
      else if(c==='"')q=true;else if(c===','){row.push(f);f='';}
      else if(c==='\n'||c==='\r'){if(c==='\r'&&text[i+1]==='\n')i++;row.push(f);rows.push(row);row=[];f='';}
      else f+=c;}
    if(f||row.length){row.push(f);rows.push(row);}return rows;}
  const esc=s=>String(s||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  function withRc(u){if(!u)return'';try{const x=new URL(u);if(x.hostname.includes('caveduck.io')&&!x.searchParams.get('rc'))x.searchParams.set('rc',RC);return x.toString();}catch(e){return u;}}
  let cards=[],cur='';
  function render(){const grid=document.getElementById('card-grid'),bar=document.getElementById('card-filter');if(!grid)return;
    const cats=[...new Set(cards.flatMap(c=>c.cats))];
    bar.innerHTML=cats.length?['',...cats].map(c=>'<button class="chip'+(c===cur?' on':'')+'" data-c="'+esc(c)+'">'+(c?esc(c):esc(t('cards.all')))+'</button>').join(''):'';
    bar.querySelectorAll('.chip').forEach(b=>b.onclick=()=>{cur=b.dataset.c;render();});
    const list=cards.filter(c=>!cur||c.cats.includes(cur));
    grid.innerHTML=list.map(c=>'<a class="card" href="'+esc(c.url)+'" target="_blank">'+(c.img?'<img src="'+esc(c.img)+'" alt="" loading="lazy">':'')+
      '<h3>'+esc(c.name)+'</h3>'+(c.cats.length?'<div class="tags">'+c.cats.map(x=>'<span>'+esc(x)+'</span>').join('')+'</div>':'')+
      (c.desc?'<p>'+esc(c.desc)+'</p>':'')+'<span class="go" data-i18n="cards.go">'+esc(t('cards.go'))+'</span></a>').join('');
    if(window.applyLang)document.querySelectorAll('#card-grid a[href*="caveduck.io/"]').forEach(a=>{const l=(localStorage.getItem('angu_lang')||'zh');a.href=a.href.replace(/caveduck\.io\/(zh-hant|ja|ko|en|es)\//,'caveduck.io/'+(CAVE_LOCALE[l]||'zh-hant')+'/');});}
  function state(key){const g=document.getElementById('card-grid');if(g)g.innerHTML='<p class="card-state">'+esc(t(key))+'</p>';}
  document.addEventListener('DOMContentLoaded',()=>{
    if(!document.getElementById('card-grid'))return;
    if(!CARDS_SHEET){state('cards.empty');return;}
    state('cards.loading');
    fetch(CARDS_SHEET+(CARDS_SHEET.includes('?')?'&':'?')+'t='+Date.now()).then(r=>r.text()).then(txt=>{
      const rows=parseCSV(txt).filter(r=>r.some(x=>x.trim()));if(rows.length<2){state('cards.empty');return;}
      const H=rows[0].map(h=>h.trim()),col=n=>H.indexOf(n);
      const iOn=col('上架'),iN=col('卡名'),iI=col('封面'),iU=col('連結'),iC=col('分類'),iD=col('簡介');
      cards=rows.slice(1).filter(r=>iOn<0||/^(true|是|v|✓|1|yes)$/i.test((r[iOn]||'').trim())).filter(r=>(r[iN]||'').trim())
        .map(r=>({name:r[iN].trim(),img:(r[iI]||'').trim(),url:withRc((r[iU]||'').trim()),desc:(r[iD]||'').trim(),cats:(r[iC]||'').split(/[、,，\/]/).map(s=>s.trim()).filter(Boolean)}));
      cards.length?render():state('cards.empty');
    }).catch(()=>state('cards.error'));
    document.addEventListener('langchange',render);
  });
})();
