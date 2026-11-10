/* Delulu 企劃群的朋友：房間裡的人和「書籤」頁共用這一份。
   name 名字、site 網站、line 在房間裡點到時說的話（可以不填，不填用預設招呼）。
   房間裡點到任何一位都會帶去書籤頁（右邊窗戶被擋住了，書籤改從朋友進）。
   書籤頁上有網站的人圖可以點，沒網站的只有圖和名字。
   key 對應 img/sprites/ 裡的圖檔名。 */
window.DELULU={
  dl_cherry:   {name:"櫻桃", site:"https://cherrienoir.neocities.org/", line:""}, // 貓耳髮箍，沙發
  dl_eggplant: {name:"抹茶", site:"https://matcha1642.neocities.org/ME/", line:""}, // 綠髮，沙發
  dl_banana:   {name:"米粒", site:"", line:""}, // 香蕉帽，沙發
  dl_pinkberet:{name:"可可", site:"", line:""}, // 粉髮貝雷帽，沙發
  dl_blueears: {name:"河狗", site:"", line:""}, // 藍色狗狗耳，沙發
  dl_orange:   {name:"布啾", site:"", line:""}, // 橘髮，沙發
  dl_carrot:   {name:"阿湮", site:"", line:""}, // 胡蘿蔔帽，蓋珞普旁看書
  dl_fish:     {name:"魚魚", site:"", line:""}, // 藍衣服，地毯上逗艾倫坡
  dl_cow:      {name:"妮鴿", site:"", line:""}  // 乳牛裝，沙發旁地上
};
/* 書籤頁：全部排出來，有網站的才能點 */
document.addEventListener('DOMContentLoaded',()=>{const box=document.getElementById('delulu-grid');if(!box)return;
  Object.entries(DELULU).filter(([,f])=>f.name).forEach(([id,f])=>{const a=document.createElement(f.site?'a':'div');a.className='pal'+(f.site?'':' nolink');
    if(f.site){a.href=f.site;a.target='_blank';}
    a.innerHTML='<img src="img/sprites/'+id+'.png" alt=""><span>'+f.name+'</span>';box.appendChild(a);});});
