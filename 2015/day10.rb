#!/usr/bin/env ruby
input = File.read(ARGV[0])
numiters = ARGV[1].to_i
conways_constant = 1.303577269034296391255709911215255

def look_and_say(sequence)
    out = ""
    cnt = 1
    (1..sequence.length - 1).each do |idx|
        if sequence[idx] != sequence[idx - 1]
            out += "#{cnt}#{sequence[idx - 1]}"
            cnt = 1
        else
            cnt += 1
        end
    end
    if cnt > 0
        out += "#{cnt}#{sequence[sequence.length - 1]}"
    end
    return out
end
orig = input
conway = 0
(1..numiters).each do |i|
    input = look_and_say(input)
end

puts "Part 1: #{conway}"
