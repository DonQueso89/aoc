#!/usr/bin/env ruby
require('digest')
require('set')

input = File.read(ARGV[0])

ZE_LATIN_ALPHABETTHH = "abcdefghijklmnopqrstuvwxyz"
doppios_rgx = Regexp.new ZE_LATIN_ALPHABETTHH.chars.map { |e| e + e } .join "|"

is_nice = lambda { |s|
    /ab|cd|pq|xy/.match(s) == nil &&
    s.scan(/[aeiou]/).size > 2 &&
    doppios_rgx.match(s) != nil ? 1 : 0
}

puts "Part 1: #{input.split().map { |s| is_nice.call(s) } .sum}"

# scan looks for non-overlapping occurrences
palindromes_rgx = Regexp.new ZE_LATIN_ALPHABETTHH.chars.map { 
    |outer| ZE_LATIN_ALPHABETTHH.tr(outer, "").chars.map { 
        |inner| outer + inner + outer } .join "|" } .join("|")

doppios_rgx = Regexp.new ZE_LATIN_ALPHABETTHH.chars.map { 
    |left| ZE_LATIN_ALPHABETTHH.chars.map { 
        |right| (left + right) + ".*" + (left + right) } .join "|" } .join("|")

is_nice = lambda { |s|
    palindromes_rgx.match(s) != nil &&
        doppios_rgx.match(s) != nil ? 1 : 0
}

puts "Part 2: #{input.split().map { |s| is_nice.call(s) } .sum }"
