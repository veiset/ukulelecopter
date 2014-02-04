#!/usr/bin/env node
var arDrone = require('ar-drone');
var client  = arDrone.createClient();
var last_date = Date.now();
var INTERVAL = 1*1000; // 1 second

process.stdin.resume();
process.stdin.setEncoding('UTF-8');
process.stdin.pipe(process.stdout);

process.stdin.on('data', function(data) {
	var now = Date.now();
	if (now > last_date+INTERVAL) {
		if (data === "A") {
			client.land();
		} else if (data === "E") {
			client.clockwise(0.1);
		} else if (data === "C") {
			client.counterClockwise(0.1);
		} else if (data === "G") {
			client.takeoff();
		}
		last_date = now;
	}
});

process.stdin.on('end', function() {
});

setInterval(function() { }, 1e3); // keep alive