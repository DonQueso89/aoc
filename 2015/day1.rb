#!/usr/bin/env ruby
input = File.read(ARGV[0])
puts "Part 1 " + String(input.count("(") - input.count(")"))

pos = 0
cnt = 1
input.split("").each do |char|
    pos += (char == '(' ? 1 : -1)
    if pos == -1 then
        puts "Part 2 " + String(cnt)
    end
    cnt += 1
end
