#!/usr/bin/env node
//var client = require('./dronemock.js');
var arDrone = require('ar-drone');
var client  = arDrone.createClient();
var INTERVAL = 800; // ms
var seq = "";

process.stdin.resume();
process.stdin.setEncoding('UTF-8');
process.stdin.pipe(process.stdout);

var patterns = {
	'A'    : { 'cmd' : function() { client.land() } },
	'E'    : { 'cmd' : function() { client.left(0.5) } },
	'D'    : { 'cmd' : function() { client.right(0.5) } },
	'G'    : { 'cmd' : function() { client.takeoff() } },
	'AE'   : { 'cmd' : function() { client.up(0.5) } },
	'EA'   : { 'cmd' : function() { client.down(0.5) } },
	'AGA'  : { 'cmd' : function() { client.animate('flipLeft', 1000); } }
}

var executeSequnce = function() { 
	if (patterns.hasOwnProperty(seq)) {
		var cmd = patterns[seq];
		console.log("\n" + "   CMD: " + seq);
		cmd.cmd();
	} else {
		client.stop(); // stop motion
	}
	seq = "";
};

var delayedExecution = setInterval(executeSequnce, INTERVAL);

process.stdin.on('data', function(data) {
	if (seq.slice(-1) !== data) {
		seq += data;
	}
	clearInterval(delayedExecution);
	delayedExecution = setInterval(executeSequnce, INTERVAL);
});