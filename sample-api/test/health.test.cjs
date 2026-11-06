const test=require('node:test');const assert=require('node:assert/strict');
const {HttpRequest}=require('@azure/functions');
const {health}=require('../dist/src/functions/health.js');
const request=()=>new HttpRequest({url:'https://example.invalid/api/health',method:'GET'});
test('actual health handler returns the expected public contract',async()=>{
 const logs=[];const r=await health(request(),{log:x=>logs.push(x)});
 assert.equal(r.status,200);assert.equal(r.jsonBody.status,'ok');assert.equal(r.jsonBody.service,'workforce-api');assert.equal(logs.length,1);
});
test('environment binding and local fallback are explicit',async()=>{
 const previous=process.env.WORKFORCE_ENVIRONMENT;
 try{delete process.env.WORKFORCE_ENVIRONMENT;assert.equal((await health(request(),{log:()=>{}})).jsonBody.environment,'local');process.env.WORKFORCE_ENVIRONMENT='fictional-nonproduction';assert.equal((await health(request(),{log:()=>{}})).jsonBody.environment,'fictional-nonproduction');}
 finally{if(previous===undefined)delete process.env.WORKFORCE_ENVIRONMENT;else process.env.WORKFORCE_ENVIRONMENT=previous;}
});
test('health response has a parseable timestamp and no business payload',async()=>{
 const r=await health(request(),{log:()=>{}});assert.ok(Number.isFinite(Date.parse(r.jsonBody.timestamp)));
 assert.deepEqual(Object.keys(r.jsonBody).sort(),['environment','service','status','timestamp']);
});
