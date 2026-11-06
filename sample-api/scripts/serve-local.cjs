// Direct handler harness, not Azure Functions Core Tools or the Functions host.
const http=require('node:http');
const {HttpRequest,InvocationContext}=require('@azure/functions');
const {health}=require('../dist/src/functions/health.js');
const port=Number(process.env.PORT||8020);
if(!Number.isInteger(port)||port<1024||port>65535)throw Error('Invalid local port');
const expected='127.0.0.1:'+port;
const server=http.createServer(async(req,res)=>{
 res.setHeader('Cache-Control','no-store');res.setHeader('Content-Type','application/json');
 if(req.headers.host!==expected){res.writeHead(403);return res.end('{"error":"Unexpected host"}');}
 if(req.method!=='GET'){res.writeHead(405);return res.end('{"error":"GET required"}');}
 if(req.url!=='/api/health'){res.writeHead(404);return res.end('{"error":"Not found"}');}
 try{const result=await health(new HttpRequest({url:'http://'+expected+'/api/health',method:'GET'}),new InvocationContext({functionName:'health'}));res.writeHead(result.status||200);res.end(JSON.stringify(result.jsonBody));}
 catch{res.writeHead(500);res.end('{"error":"Local handler failed"}');}
});
server.listen(port,'127.0.0.1',()=>console.log('Direct-handler harness: http://'+expected+'/api/health'));
process.on('SIGTERM',()=>server.close(()=>process.exit(0)));
