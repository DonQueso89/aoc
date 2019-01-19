#!/usr/bin/env ruby

input = File.read(ARGV[0]).split("\n")

puts "part 1: #{input.map { |i| i.length - eval(i).length } .reduce(:+)}"
puts "part 2: #{input.map { |i| i.inspect.length - i.length } .reduce(:+)}"
