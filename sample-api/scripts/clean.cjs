const fs=require('node:fs');const path=require('node:path');
const root=path.resolve(__dirname,'..');const dist=path.join(root,'dist');
if(path.dirname(dist)!==root||path.basename(dist)!=='dist')throw Error('Unexpected build target');
fs.rmSync(dist,{recursive:true,force:true});
