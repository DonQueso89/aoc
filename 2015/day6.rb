#!/usr/bin/env ruby
require('set')

# Runtime ~3 min. :(

input = File.read(ARGV[0])
rgx = /^(turn off|toggle|turn on) (\d+),(\d+) through (\d+),(\d+)$/

operations = {
    "turn on" => lambda { |inputset, lights| return inputset + lights },
    "turn off" => lambda { |inputset, lights| return inputset - lights },
    "toggle" =>  lambda { |inputset, lights|
        toggle_off = inputset & lights
        lights -= toggle_off
        inputset -= toggle_off
        return inputset + lights
    }
}

lights_on = Set.new
input.split("\n").each do |instruction|
    func, sx, sy, ex, ey = rgx.match(instruction).captures
    sx, sy, ex, ey = sx.to_i, sy.to_i, ex.to_i, ey.to_i
    lights_hit = Set.new((sx..ex).to_a.product((sy..ey).to_a))
    lights_on = operations[func].call(lights_on, lights_hit)
    puts instruction
end 

puts "Part 1: #{lights_on.size}"
