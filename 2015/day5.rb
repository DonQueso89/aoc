#!/usr/bin/env ruby
require('digest')

input = File.read(ARGV[0])

cnt = 0
rgx = /^00000/

while true
    h = Digest::MD5.hexdigest("#{input}#{cnt}")
    break if rgx.match(h) != nil
    cnt += 1
end
puts "Part 1: #{cnt}"

rgx = /^000000/

while true
    h = Digest::MD5.hexdigest("#{input}#{cnt}")
    break if rgx.match(h) != nil
    cnt += 1
end
puts "Part 2: #{cnt}"
