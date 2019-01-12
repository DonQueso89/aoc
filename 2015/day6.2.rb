#!/usr/bin/env ruby
# Run time ~1min :(
#
input = File.read(ARGV[0])
rgx = /^(turn off|toggle|turn on) (\d+),(\d+) through (\d+),(\d+)$/

values = {
    "toggle" => lambda { |i| 2 },
    "turn on" => lambda { |i| 1 },
    "turn off" => lambda { |i| i == 0 ? 0 : -1 }
}

brightnesses = Hash.new(default=0)
input.split("\n").each do |instruction|
    func, sx, sy, ex, ey = rgx.match(instruction).captures
    sx, sy, ex, ey = sx.to_i, sy.to_i, ex.to_i, ey.to_i
    (sx..ex).to_a.each do |x|
        (sy..ey).to_a.each do |y|
            brightnesses[[x, y]] += values[func].call(brightnesses[[x, y]])
        end
    end
end 

puts "Part 2: #{brightnesses.values.sum}"
