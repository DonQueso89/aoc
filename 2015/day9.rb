#!/usr/bin/env ruby
require('set')

input = File.read(ARGV[0]).split("\n")
input = input.map { |line| line.delete(" ").split("=") } 
distances = Hash.new

input.each do |path, dist|
    a, b = path.split("to")
    distances[[a, b]] = dist.to_i
    distances[[b, a]] = dist.to_i
end

cities = Set.new(distances.keys.map { |a, b| a }).to_a
# search space == !7  == 5040
paths = cities.permutation.map { |perm|
    (0..perm.length - 2).map { |i| distances[[perm[i], perm[i + 1]]] } .reduce(:+)
}
puts "Part 1: #{paths.min}"
puts "Part 2: #{paths.max}"
