#!/usr/bin/env ruby

input = File.read(ARGV[0])
movement = {
    '>' => lambda { |x, y| return [x + 1, y] },
    '<' => lambda { |x, y| return [x - 1, y] },
    'v' => lambda { |x, y| return [x, y + 1] },
    '^' => lambda { |x, y| return [x, y - 1] }
}

x, y = [0, 0]
present_counter = Hash.new(default=0)
present_counter[[x, y]] += 1

input.each_char { |c|
    x, y = movement[c].call(x, y)
    present_counter[[x, y]] += 1
}

puts "Part 1: #{present_counter.keys.length}"

sx, sy = [0, 0]
rx, ry = [0, 0]
present_counter = Hash.new(default=0)
present_counter[[0, 0]] += 2
santasturn = true

input.each_char { |c|
    if santasturn
        sx, sy = movement[c].call(sx, sy)
        present_counter[[sx, sy]] += 1
    else
        rx, ry = movement[c].call(rx, ry)
        present_counter[[rx, ry]] += 1
    end
    santasturn = !santasturn 
}
puts "Part 2: #{present_counter.keys.length}"
