export function buildCodexIndex(codex){
  const chapters=[]; const verses=[];
  for(const [book,bookChapters] of Object.entries(codex||{})){
    if(book.startsWith('Info')||!bookChapters||typeof bookChapters!=='object'||Array.isArray(bookChapters)) continue;
    for(const [chapter,units] of Object.entries(bookChapters)){
      if(!units||typeof units!=='object'||Array.isArray(units)) continue;
      const chapterUnits=[];
      for(const [verse,text] of Object.entries(units)) if(typeof text==='string'&&text.trim()){
        const unit={id:`${book}.${chapter}.${verse}`,book,chapter,verse,reference:`${book} ${chapter}:${verse}`,text};
        verses.push(unit); chapterUnits.push(unit);
      }
      if(chapterUnits.length) chapters.push({id:`${book}.${chapter}`,book,chapter,reference:`${book} ${chapter}`,units:chapterUnits});
    }
  }
  return {chapters,verses};
}
export const randomChapter=chapters=>chapters[Math.floor(Math.random()*chapters.length)];
export const chapterText=chapter=>(chapter?.units||[]).map(u=>`${u.reference}: ${u.text}`).join('\n');
