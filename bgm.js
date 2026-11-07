/* 內頁背景音樂：隨機播安谷的 SUNO 角色歌。要加歌就往 TRACKS 加一行。 */
window.TRACKS=[
 {title:'UN/VEIL',sub:'白鎮 41 號',src:'https://files.catbox.moe/5ky4ir.mp3'},
 {title:'大稻埕迷途',sub:'南街殷賑主題曲',src:'https://files.catbox.moe/qqc6wt.mp3'},
 {title:'狛胡角色歌',sub:'梅花江湖易數算命師',src:'https://files.catbox.moe/skalez.mp3'},
 {title:'南洋一角色歌',sub:'真夜中の心霊なんてない',src:'https://files.catbox.moe/6u3fdq.mp4'}
];
(function(){
  const css=document.createElement('style');css.textContent=`
  .jukebox{position:fixed;left:14px;bottom:14px;z-index:30;display:flex;align-items:center;gap:10px;background:rgba(10,8,9,.94);border:2px solid #8a6d1c;outline:1px solid #c9a227;outline-offset:2px;padding:6px 10px;color:#e8e0d0;font-family:"Noto Serif TC",serif;font-size:13px;box-shadow:4px 4px 0 #000;max-width:calc(100vw - 28px)}
  .jukebox button{background:#141015;border:1px solid #8a6d1c;color:#c9a227;font-family:inherit;font-size:13px;padding:3px 8px;cursor:pointer}
  .jukebox button:hover{background:#6b0f1a;color:#fff}
  .jukebox .ttl{letter-spacing:.1em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:220px}
  .jukebox .ttl small{display:block;color:#9a8f85;font-size:11px}
  .jukebox .disc{width:18px;height:18px;border-radius:50%;flex:none;background:radial-gradient(circle,#c9a227 0 2px,#1a1115 2.5px 4px,#2a2126 4.5px 5px,#1a1115 5.5px 7px,#2a2126 7.5px 8px,#1a1115 8.5px);box-shadow:0 0 0 1px #8a6d1c;position:relative}
  .jukebox .disc::after{content:'';position:absolute;left:8px;top:1px;width:2px;height:5px;background:#e8e0d0;border-radius:1px;opacity:.7}
  .jukebox.playing .disc{animation:spin 2s linear infinite}
  @keyframes spin{to{transform:rotate(360deg)}}
  @media (max-width:640px){.jukebox{left:8px;right:8px;bottom:8px;font-size:12px}.jukebox .ttl{max-width:none;flex:1}}`;
  document.head.appendChild(css);
  const audio=new Audio();audio.volume=0.4;audio.preload='none';
  let order=[],idx=0,on=false;
  try{on=localStorage.getItem('angu_juke')==='1';}catch(e){}
  function shuffle(){order=TRACKS.map((_,i)=>i).sort(()=>Math.random()-.5);idx=0;}
  function load(){const tr=TRACKS[order[idx]];audio.src=tr.src;ttl.innerHTML=tr.title+'<small>'+tr.sub+'</small>';}
  function play(){audio.play().then(()=>{box.classList.add('playing');btn.textContent='❚❚';}).catch(()=>{});}
  function pause(){audio.pause();box.classList.remove('playing');btn.textContent='▶';}
  function next(){idx=(idx+1)%order.length;load();if(on)play();}
  const box=document.createElement('div');box.className='jukebox';
  box.innerHTML='<span class="disc"></span><button class="pp">▶</button><button class="nx">⏭</button><span class="ttl"></span>';
  document.body.appendChild(box);
  const btn=box.querySelector('.pp'),ttl=box.querySelector('.ttl');
  btn.onclick=()=>{on=!on;try{localStorage.setItem('angu_juke',on?'1':'0');}catch(e){}on?play():pause();};
  box.querySelector('.nx').onclick=next;
  audio.addEventListener('ended',next);
  shuffle();load();
  // 瀏覽器要先有互動才准出聲：上次是開的，就等第一次點擊或按鍵再續播
  if(on){const arm=()=>{play();removeEventListener('pointerdown',arm);removeEventListener('keydown',arm);};addEventListener('pointerdown',arm);addEventListener('keydown',arm);btn.textContent='▶';}
})();
