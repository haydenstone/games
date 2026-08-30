import assert from 'node:assert/strict';
const world={power:false,ride:{running:true}}; world.ride.running=!!world.power; assert.equal(world.ride.running,false); console.log('PASS: generic power dependency stops ride');
