/* Delulu 企劃群的朋友：房間沙發上的人和「書籤」頁共用這一份。
   名字（name）、網站（site）填好，房間點到他會去他的網站，書籤頁也會出現他的圖和連結。
   沒填網站的人，房間點到會帶去書籤頁。line 是房間裡說的話，可以不填。
   key 對應 img/sprites/ 裡的圖檔名。 */
window.DELULU={
  dl_cherry:   {name:"Cherrie", site:"https://cherrienoir.neocities.org/", line:""},
  dl_banana:   {name:"", site:"", line:""},
  dl_pinkberet:{name:"", site:"", line:""},
  dl_blueears: {name:"", site:"", line:""},
  dl_orange:   {name:"", site:"", line:""},
  dl_eggplant: {name:"抹茶", site:"https://matcha1642.neocities.org/ME/", line:""},
  dl_carrot:   {name:"", site:"", line:""},
  dl_fish:     {name:"", site:"", line:""},
  dl_cow:      {name:"", site:"", line:""}
};
/* 書籤頁：有名字也有網站的才排出來 */
document.addEventListener('DOMContentLoaded',()=>{const box=document.getElementById('delulu-grid');if(!box)return;
  Object.entries(DELULU).filter(([,f])=>f.name&&f.site).forEach(([id,f])=>{const a=document.createElement('a');a.className='pal';a.href=f.site;a.target='_blank';
    a.innerHTML='<img src="img/sprites/'+id+'.png" alt=""><span>'+f.name+'</span>';box.appendChild(a);});});
