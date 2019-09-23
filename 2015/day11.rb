#!/usr/bin/env ruby
def validate(password)
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    doppios_rgx = Regexp.new alphabet.chars.map { |e| "#{e}{2}"  } .join "|"

    result = true
    result &= !password.match(/[iol]+/)
    if result == false
        return result
    end

    result &= (password.length - password.gsub(doppios_rgx, "").length >= 4 &&  password.scan(doppios_rgx).uniq.length >= 2)
    
    if result == false
        return result
    end

    # Increasing straight
    result &= (1..password.length - 2).map { |idx|
        a, b, c = password.slice(idx - 1, 3).chars.map { |x| x.ord }
        [b - a, c - b].sum == 2
    } .any?

    return result
end

def incr(password)
    ascii_vals = password.chars.map { |x| x.ord - 97 } .reverse
    digit = 0

    while true
        ascii_vals[digit] += 1
        ascii_vals[digit] %= 26

        if ascii_vals[digit] == 0
            if digit == ascii_vals.length - 1
                ascii_vals.push(0)
                return ascii_vals.reverse.map { |i| (i + 97).chr } .join("")
            end
            digit += 1
        else
            return ascii_vals.reverse.map { |i| (i + 97).chr } .join("")
        end
    end
end

def incr_at(password, digit)
    ascii_vals = password.chars.map { |x| x.ord - 97 }
    d = password.length - 1
    while d > digit
        ascii_vals[d] = 0
        d -= 1
    end
    ascii_vals[d] += 1
    ascii_vals[d] %= 26
    return ascii_vals.map { |i| (i + 97).chr } .join("")
end
if __FILE__ == $0
    input = File.read(ARGV[0])
    while !validate(input)
        m = input.match(/[iol]/)
        if m != nil
            input = incr_at(input, m.begin(0))
        else
            input = incr(input)
        end
        puts input
    end
    puts "Part 1: #{input}"
end
