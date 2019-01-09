#!/usr/bin/env ruby
input = File.read(ARGV[0])
total = 0
input.split().each do |line|
    l, w, h = line.split("x").map { |s| s.to_i}
    sides = [l * h,  w * l, h * w].map { |i| i * 2 }
    total += (sides.min / 2 + sides.reduce(:+))
end
puts "Part 1: #{total}"

total_ribbon = input.split().map { |line|
    line.split("x").map { |s| s.to_i }.sort
}

total_ribbon = total_ribbon.map { |p| 
    p[0] * 2 + p[1] * 2 + p.reduce(:*)
}
puts "Part 2: #{total_ribbon.reduce(:+)}"
